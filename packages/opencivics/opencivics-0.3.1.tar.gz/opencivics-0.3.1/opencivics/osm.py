"""
OpenStreetMap data extraction and analysis functions.

This module provides tools for extracting features from OSM PBF files and 
analyzing them in relation to geographical boundaries.
"""

import osmium
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import re


class FeatureHandler(osmium.SimpleHandler):
    """
    An Osmium handler that extracts features based on a detailed configuration,
    allowing for an object to be counted multiple times if it matches multiple rules.
    """
    def __init__(self, feature_config):
        super().__init__()
        self.features = []
        self.way_nodes = {}
        self.feature_config = feature_config # Use the raw config directly
        # --- Attributes for progress tracking ---
        self.node_count = 0
        self.way_count = 0

    def _add_feature(self, element, geom, category, subcategory):
        """Appends a feature to the results list."""
        self.features.append({
            'osm_id': f"{type(element).__name__.lower()}_{element.id}",
            'category': category,
            'subcategory': subcategory,
            'name': element.tags.get('name'),
            'geometry': geom
        })

    def node(self, n):
        """Processes OSM nodes and reports progress."""
        self.node_count += 1
        if self.node_count % 5_000_000 == 0:
            print(f"      ... processed {self.node_count // 1_000_000} million nodes.", flush=True)

        # Storing all node locations is memory-intensive but necessary for ways.
        if n.location.valid():
            self.way_nodes[n.id] = (n.location.lon, n.location.lat)
        
        # Check this node against every rule in the configuration
        for key, values, category, subcategory in self.feature_config:
            if key in n.tags:
                tag_value = n.tags[key]
                # If rule has specific values, check for a match. If not (None), key existence is enough.
                if values is None or tag_value in values:
                    # Match found, add it. The loop continues to check for other matches.
                    self._add_feature(n, Point(n.location.lon, n.location.lat), category, subcategory)

    def way(self, w):
        """Processes OSM ways and reports progress."""
        self.way_count += 1
        if self.way_count % 1_000_000 == 0:
            print(f"      ... processed {self.way_count // 1_000_000} million ways.", flush=True)

        # Check this way against every rule in the configuration
        for key, values, category, subcategory in self.feature_config:
            if key in w.tags:
                tag_value = w.tags[key]
                if values is None or tag_value in values:
                    # Match found, calculate centroid and add it.
                    coords = [self.way_nodes[node.ref] for node in w.nodes if node.ref in self.way_nodes]
                    if coords:
                        centroid = Point(sum(c[0] for c in coords) / len(coords), sum(c[1] for c in coords) / len(coords))
                        self._add_feature(w, centroid, category, subcategory)


def extract_features_from_pbf(pbf_path, feature_config):
    """Extracts a wide range of features from an OSM PBF file."""
    handler = FeatureHandler(feature_config)
    handler.apply_file(pbf_path, locations=True)
    if not handler.features:
        return gpd.GeoDataFrame()
    return gpd.GeoDataFrame(handler.features, crs="EPSG:4326")


def add_feature_counts_to_boundaries(boundaries_gdf, features_gdf, area_code_col):
    """
    Spatially joins features to boundary areas and calculates counts by subcategory and category.
    """
    if features_gdf.empty:
        print("⚠️ No features found to process.")
        return boundaries_gdf

    geom_col_name = boundaries_gdf.geometry.name
    
    features_in_area = gpd.sjoin(
        features_gdf,
        boundaries_gdf[[area_code_col, geom_col_name]],
        how='inner',
        predicate='within'
    )

    if features_in_area.empty:
        print("⚠️ No features were located within the provided boundaries.")
        return boundaries_gdf

    subcategory_counts = features_in_area.groupby([area_code_col, 'subcategory']).size().unstack(fill_value=0)
    subcategory_counts.columns = [f"{col}_count" for col in subcategory_counts.columns]
    
    category_counts = features_in_area.groupby([area_code_col, 'category']).size().unstack(fill_value=0)
    category_counts.columns = [f"{col}_total_count" for col in category_counts.columns]

    updated_gdf = boundaries_gdf.merge(subcategory_counts, on=area_code_col, how='left')
    updated_gdf = updated_gdf.merge(category_counts, on=area_code_col, how='left')

    count_cols = list(subcategory_counts.columns) + list(category_counts.columns)
    updated_gdf[count_cols] = updated_gdf[count_cols].fillna(0).astype(int)
    
    return updated_gdf


def analyze_osm_features(boundaries_gdf, pbf_path, area_code_col, feature_config, custom_metrics=None):
    """
    A complete workflow to extract, categorize, and count a wide range of OSM features.
    """
    print("--- Starting OSM Feature Analysis ---")
    print(f"1. Extracting {len(feature_config)} feature types from {pbf_path}...")
    features_gdf = extract_features_from_pbf(pbf_path, feature_config)
    print(f"✅ Found {len(features_gdf)} total feature instances.")
    
    if features_gdf.empty:
        print("❌ Halting workflow as no features were extracted.")
        return boundaries_gdf
    
    print(f"\n2. Counting features within each '{area_code_col}' boundary...")
    final_gdf = add_feature_counts_to_boundaries(boundaries_gdf, features_gdf, area_code_col)
    print(f"✅ Spatial join and counting complete.")
    
    # Debug: Show available columns before custom metrics
    print(f"\n📊 Available columns before custom metrics: {sorted(final_gdf.columns.tolist())}")
    
    if custom_metrics:
        print("\n3. Calculating custom metrics...")
        
        for metric_name, formula in custom_metrics.items():
            try:
                # Extract column names referenced in the formula using regex
                # This finds variable names (letters, numbers, underscores) in the formula
                referenced_cols = re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', formula)
                
                # Filter out Python keywords and operators that might be captured
                python_keywords = {'and', 'or', 'not', 'in', 'is', 'if', 'else', 'for', 'while', 'def', 'class', 'import', 'from', 'as', 'try', 'except', 'finally', 'with', 'lambda', 'yield', 'return', 'break', 'continue', 'pass', 'global', 'nonlocal', 'assert', 'del', 'raise', 'True', 'False', 'None'}
                referenced_cols = [col for col in referenced_cols if col not in python_keywords]
                
                print(f"   Processing '{metric_name}' with formula: {formula}")
                print(f"   Referenced columns: {referenced_cols}")
                
                # Check if all referenced columns exist, create missing ones with 0
                missing_cols = []
                for col in referenced_cols:
                    if col not in final_gdf.columns:
                        final_gdf[col] = 0
                        missing_cols.append(col)
                
                if missing_cols:
                    print(f"   ⚠️  Created missing columns with value 0: {missing_cols}")
                
                # Calculate the custom metric
                final_gdf[metric_name] = final_gdf.eval(formula, engine='python')
                print(f"   ✅ Calculated '{metric_name}' score.")
                
            except Exception as e:
                print(f"   ❌ Could not calculate metric '{metric_name}': {e}")
                print(f"   Formula was: {formula}")
                # Set the metric to 0 if calculation fails
                final_gdf[metric_name] = 0
    
    print("\n✅ Workflow finished successfully.")
    print(f"📊 Final columns: {sorted(final_gdf.columns.tolist())}")
    
    return final_gdf


# Feature tags configuration for Australian context
FEATURE_TAGS = [
    # Accessibility to Essential Services
    ('amenity', ['school'], 'access', 'school'),
    ('amenity', ['childcare', 'kindergarten', 'music_school'], 'access', 'childcare'),
    ('amenity', ['doctors', 'clinic'], 'access', 'health_clinic'),
    ('amenity', ['hospital'], 'access', 'hospital'),
    ('amenity', ['social_facility', 'nursing_home'], 'access', 'aged_care'),
    
    # retail
    ('shop', ['supermarket', 'convenience', 'bakery', 'department_store', 'greengrocer', 'butcher', 'chemist', 'pharmacy', 'clothes', 'shoes', 'electronics', 
                'furniture', 'hardware', 'books', 'toys', 'sports', 'jewelry', 'mobile_phone', 'computer', 'bicycle', 'car', 'motorcycle'], 'retail', 'retail'),
    ('landuse', ['retail'], 'retail', 'retail_landuse'),

    # Commercial Services 
    ('landuse', ['commercial'], 'commercial', 'commercial_landuse'),
    ('amenity', ['bank', 'post_office', 'fuel'], 'commercial', 'services'),
    ('office', ['government', 'ngo', 'association', 'company'], 'commercial', 'institutions'),
    ('amenity', ['university', 'research_institute', 'college'], 'commercial', 'university'),
    ('craft', ['carpenter', 'electrician', 'plumber', 'painter', 'tiler', 'roofer'], 'commercial', 'blue_collar_services'),
    ('office', ['architect', 'consultant', 'design', 'lawyer', 'insurance', 'estate_agent', 'accountant'], 'commercial', 'professional_services'),

    # Green & Recreational Spaces
    ('leisure', ['park', 'playground', 'pitch', 'nature_reserve', 'dog_park', 'recreation_ground', 'golf_course'], 'recreation', 'green_space'),
    ('leisure', ['fitness_centre', 'sports_centre', 'swimming_pool'], 'recreation', 'mass_health_activities'),
    ('leisure', ['stadium'], 'recreation', 'stadium'),

    # Safety & Security
    ('amenity', ['police', 'fire_station', 'ambulance_station'], 'safety', 'emergency_services'),

    # Social & Cultural Infrastructure
    ('amenity', ['community_centre', 'library', 'arts_centre', 'studio', 'cinema', 'theatre', 'concert_hall', 'bowling_alley', 'miniature_golf'], 'social', 'community_cultural'),
    ('historic', None, 'social', 'historic'),
    ('tourism', ['attraction', 'museum', 'gallery', 'viewpoint', 'picnic_site', 'artwork'], 'social', 'tourism'),

    # Nightlife & Eating Out
    ('amenity', ['pub', 'bar', 'nightclub', 'casino', 'restaurant', 'cafe', 'fast_food', 'cafe', 'adult_gaming_centre', 'karaoke_box', 'discotheque'], 'fun_nightlife', 'fun_nightlife'),
]