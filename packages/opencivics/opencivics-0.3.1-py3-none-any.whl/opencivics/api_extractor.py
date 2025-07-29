"""
API-based OpenStreetMap and Google Maps feature extraction.

This module provides alternatives to PBF file processing by using web APIs
to extract location features. Supports both OpenStreetMap Overpass API and
Google Maps Places API for comprehensive location data extraction.
"""

import pandas as pd
import geopandas as gpd
import requests
import time
from typing import Optional, Dict, Any, List, Tuple, Union
from shapely.geometry import Point, box
import json
import concurrent.futures
from functools import partial
import warnings
import re
from abc import ABC, abstractmethod


class BaseAPIExtractor(ABC):
    """Abstract base class for API extractors."""
    
    @abstractmethod
    def extract_features_from_bbox(self, bbox, feature_config):
        """Extract features from a bounding box."""
        pass


class OverpassAPIExtractor(BaseAPIExtractor):
    """
    Extracts OSM features using the Overpass API.
    """
    
    def __init__(self, base_url="https://overpass-api.de/api/interpreter"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'OSM-Feature-Extractor/1.0 (Python)'
        })
    
    def build_overpass_query(self, bbox, feature_config, timeout=300):
        """Build an Overpass query for the given bounding box and feature configuration."""
        min_lon, min_lat, max_lon, max_lat = bbox
        
        # Start the query
        query = f'[out:json][timeout:{timeout}];\n(\n'
        
        # Add queries for each feature type
        for key, values, category, subcategory in feature_config:
            if values is None:
                # Any value for this key
                query += f'  node["{key}"]({min_lat},{min_lon},{max_lat},{max_lon});\n'
                query += f'  way["{key}"]({min_lat},{min_lon},{max_lat},{max_lon});\n'
            else:
                # Specific values for this key
                for value in values:
                    query += f'  node["{key}"="{value}"]({min_lat},{min_lon},{max_lat},{max_lon});\n'
                    query += f'  way["{key}"="{value}"]({min_lat},{min_lon},{max_lat},{max_lon});\n'
        
        query += ');\nout center meta;\n'
        return query
    
    def execute_query(self, query, max_retries=3, retry_delay=5):
        """Execute an Overpass query with retry logic."""
        for attempt in range(max_retries):
            try:
                response = self.session.post(
                    self.base_url,
                    data=query,
                    timeout=600  # 10 minute timeout
                )
                response.raise_for_status()
                return response.json()
            
            except requests.exceptions.RequestException as e:
                if attempt == max_retries - 1:
                    raise e
                print(f"   ⚠️  Attempt {attempt + 1} failed: {e}. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
    
    def extract_features_from_bbox(self, bbox, feature_config):
        """Extract features from a bounding box using the Overpass API."""
        query = self.build_overpass_query(bbox, feature_config)
        
        try:
            data = self.execute_query(query)
            features = []
            
            # Create a lookup for feature categories
            feature_lookup = {}
            for key, values, category, subcategory in feature_config:
                if key not in feature_lookup:
                    feature_lookup[key] = []
                feature_lookup[key].append((values, category, subcategory))
            
            # Process elements
            for element in data.get('elements', []):
                tags = element.get('tags', {})
                
                # Check each tag against our feature config
                for tag_key, tag_value in tags.items():
                    if tag_key in feature_lookup:
                        for values, category, subcategory in feature_lookup[tag_key]:
                            if values is None or tag_value in values:
                                # Get geometry
                                if element['type'] == 'node':
                                    geom = Point(element['lon'], element['lat'])
                                elif element['type'] == 'way':
                                    # Use centroid for ways
                                    center = element.get('center', {})
                                    if center:
                                        geom = Point(center['lon'], center['lat'])
                                    else:
                                        continue
                                else:
                                    continue
                                
                                features.append({
                                    'osm_id': f"{element['type']}_{element['id']}",
                                    'category': category,
                                    'subcategory': subcategory,
                                    'name': tags.get('name'),
                                    'geometry': geom,
                                    'source': 'overpass'
                                })
            
            return features
            
        except Exception as e:
            print(f"   ❌ Error extracting features for bbox {bbox}: {e}")
            return []


class GoogleMapsAPIExtractor(BaseAPIExtractor):
    """
    Extracts features using Google Maps Places API.
    """
    
    def __init__(self, api_key):
        if not api_key:
            raise ValueError("Google Maps API key is required")
        self.api_key = api_key
        self.session = requests.Session()
        self.base_url = "https://maps.googleapis.com/maps/api/place"
        
        # Mapping from OSM feature config to Google Places types
        self.google_type_mapping = {
            # Access services
            ('amenity', ['school']): ['school', 'primary_school', 'secondary_school'],
            ('amenity', ['childcare', 'kindergarten']): ['school'],
            ('amenity', ['doctors', 'clinic']): ['doctor', 'hospital'],
            ('amenity', ['hospital']): ['hospital'],
            ('amenity', ['social_facility', 'nursing_home']): ['health'],
            
            # Retail
            ('shop', ['supermarket']): ['supermarket', 'grocery_or_supermarket'],
            ('shop', ['convenience']): ['convenience_store'],
            ('shop', ['bakery']): ['bakery'],
            ('shop', ['department_store']): ['department_store'],
            ('shop', ['pharmacy', 'chemist']): ['pharmacy'],
            ('shop', ['clothes']): ['clothing_store'],
            ('shop', ['shoes']): ['shoe_store'],
            ('shop', ['electronics']): ['electronics_store'],
            ('shop', ['furniture']): ['furniture_store', 'home_goods_store'],
            ('shop', ['hardware']): ['hardware_store'],
            ('shop', ['books']): ['book_store'],
            ('shop', ['jewelry']): ['jewelry_store'],
            ('shop', ['bicycle']): ['bicycle_store'],
            ('shop', ['car']): ['car_dealer'],
            
            # Commercial services
            ('amenity', ['bank']): ['bank'],
            ('amenity', ['post_office']): ['post_office'],
            ('amenity', ['fuel']): ['gas_station'],
            ('amenity', ['university', 'college']): ['university'],
            
            # Recreation
            ('leisure', ['park']): ['park'],
            ('leisure', ['fitness_centre', 'sports_centre']): ['gym'],
            ('leisure', ['stadium']): ['stadium'],
            
            # Safety
            ('amenity', ['police']): ['police'],
            ('amenity', ['fire_station']): ['fire_station'],
            
            # Social & Cultural
            ('amenity', ['library']): ['library'],
            ('amenity', ['cinema']): ['movie_theater'],
            ('tourism', ['museum']): ['museum'],
            
            # Food & Nightlife
            ('amenity', ['restaurant']): ['restaurant'],
            ('amenity', ['cafe']): ['cafe'],
            ('amenity', ['fast_food']): ['meal_takeaway'],
            ('amenity', ['bar', 'pub']): ['bar'],
            ('amenity', ['nightclub']): ['night_club'],
        }
    
    def get_google_types_for_config(self, feature_config):
        """Convert OSM feature config to Google Places types."""
        google_searches = []
        
        for key, values, category, subcategory in feature_config:
            if values is None:
                # Handle keys without specific values (like 'historic')
                if key == 'historic':
                    google_searches.append((['tourist_attraction'], category, subcategory))
                elif key == 'office':
                    google_searches.append((['real_estate_agency', 'lawyer', 'insurance_agency'], category, subcategory))
                continue
            
            # Try to find matching Google types
            found_mapping = False
            for osm_key_values, google_types in self.google_type_mapping.items():
                osm_key, osm_values = osm_key_values
                if key == osm_key and any(v in osm_values for v in values):
                    google_searches.append((google_types, category, subcategory))
                    found_mapping = True
                    break
            
            # If no direct mapping, use generic establishment search
            if not found_mapping:
                google_searches.append((['establishment'], category, subcategory))
        
        return google_searches
    
    def search_nearby_places(self, location, radius, place_type, max_retries=3):
        """Search for places near a location using Google Places API."""
        url = f"{self.base_url}/nearbysearch/json"
        
        params = {
            'location': f"{location[1]},{location[0]}",  # lat,lng format for Google
            'radius': radius,
            'type': place_type,
            'key': self.api_key
        }
        
        for attempt in range(max_retries):
            try:
                response = self.session.get(url, params=params, timeout=30)
                response.raise_for_status()
                data = response.json()
                
                if data.get('status') == 'OK':
                    return data.get('results', [])
                elif data.get('status') == 'ZERO_RESULTS':
                    return []
                else:
                    print(f"   ⚠️  Google API error: {data.get('status')}")
                    return []
                    
            except requests.exceptions.RequestException as e:
                if attempt == max_retries - 1:
                    print(f"   ❌ Failed to query Google API: {e}")
                    return []
                time.sleep(1)  # Brief delay before retry
        
        return []
    
    def extract_features_from_bbox(self, bbox, feature_config):
        """Extract features from a bounding box using Google Places API."""
        min_lon, min_lat, max_lon, max_lat = bbox
        
        # Calculate center point and radius
        center_lat = (min_lat + max_lat) / 2
        center_lon = (min_lon + max_lon) / 2
        
        # Calculate radius (approximate distance from center to corner)
        import math
        lat_diff = (max_lat - min_lat) / 2
        lon_diff = (max_lon - min_lon) / 2
        radius = int(math.sqrt(lat_diff**2 + lon_diff**2) * 111000)  # Convert to meters
        radius = min(radius, 50000)  # Google API max radius is 50km
        
        google_searches = self.get_google_types_for_config(feature_config)
        all_features = []
        seen_place_ids = set()  # Avoid duplicates
        
        for google_types, category, subcategory in google_searches:
            for place_type in google_types:
                try:
                    places = self.search_nearby_places(
                        (center_lon, center_lat), radius, place_type
                    )
                    
                    for place in places:
                        place_id = place.get('place_id')
                        if place_id in seen_place_ids:
                            continue
                        seen_place_ids.add(place_id)
                        
                        location = place.get('geometry', {}).get('location', {})
                        if not location:
                            continue
                        
                        # Check if the place is actually within our bbox
                        lat, lng = location['lat'], location['lng']
                        if not (min_lat <= lat <= max_lat and min_lon <= lng <= max_lon):
                            continue
                        
                        all_features.append({
                            'osm_id': f"google_{place_id}",
                            'category': category,
                            'subcategory': subcategory,
                            'name': place.get('name'),
                            'geometry': Point(lng, lat),
                            'source': 'google',
                            'rating': place.get('rating'),
                            'price_level': place.get('price_level')
                        })
                    
                    # Respect API rate limits
                    time.sleep(0.1)
                    
                except Exception as e:
                    print(f"   ⚠️  Error searching for {place_type}: {e}")
                    continue
        
        return all_features


def get_boundary_bbox(geometry):
    """Get bounding box from a geometry."""
    bounds = geometry.bounds
    return (bounds[0], bounds[1], bounds[2], bounds[3])  # min_lon, min_lat, max_lon, max_lat


def split_large_bbox(bbox, max_area=1.0):
    """
    Split large bounding boxes into smaller ones to avoid API limits.
    
    Parameters:
    -----------
    bbox : tuple
        (min_lon, min_lat, max_lon, max_lat)
    max_area : float
        Maximum area in square degrees
    
    Returns:
    --------
    list
        List of smaller bounding boxes
    """
    min_lon, min_lat, max_lon, max_lat = bbox
    width = max_lon - min_lon
    height = max_lat - min_lat
    area = width * height
    
    if area <= max_area:
        return [bbox]
    
    # Split into quarters
    mid_lon = (min_lon + max_lon) / 2
    mid_lat = (min_lat + max_lat) / 2
    
    quadrants = [
        (min_lon, min_lat, mid_lon, mid_lat),  # Bottom-left
        (mid_lon, min_lat, max_lon, mid_lat),  # Bottom-right
        (min_lon, mid_lat, mid_lon, max_lat),  # Top-left
        (mid_lon, mid_lat, max_lon, max_lat)   # Top-right
    ]
    
    # Recursively split if still too large
    result = []
    for quad in quadrants:
        result.extend(split_large_bbox(quad, max_area))
    
    return result


def extract_features_for_boundaries(boundaries_gdf, feature_config, area_code_col, 
                                   api_type="overpass", google_api_key=None, max_workers=5):
    """
    Extract features for all boundaries using either Overpass API or Google Maps API.
    
    Parameters:
    -----------
    boundaries_gdf : GeoDataFrame
        Boundaries to extract features for
    feature_config : list
        List of (key, values, category, subcategory) tuples
    area_code_col : str
        Column name for area codes
    api_type : str
        Either "overpass" or "google"
    google_api_key : str, optional
        Required if using Google Maps API
    max_workers : int
        Maximum number of concurrent API requests
    
    Returns:
    --------
    GeoDataFrame
        Features with area codes
    """
    
    if api_type.lower() == "google":
        if not google_api_key:
            raise ValueError("Google API key is required when using api_type='google'")
        extractor = GoogleMapsAPIExtractor(google_api_key)
        print("🌐 Extracting features using Google Maps Places API...")
        max_area = 0.1  # Smaller chunks for Google API due to radius limits
        max_workers = min(max_workers, 3)  # Be more conservative with Google API
    elif api_type.lower() == "overpass":
        extractor = OverpassAPIExtractor()
        print("🌐 Extracting features using OpenStreetMap Overpass API...")
        max_area = 0.5  # Larger chunks OK for Overpass
    else:
        raise ValueError("api_type must be either 'overpass' or 'google'")
    
    # Get overall bounding box
    total_bounds = boundaries_gdf.total_bounds
    overall_bbox = (total_bounds[0], total_bounds[1], total_bounds[2], total_bounds[3])
    
    # Split large areas into smaller chunks
    bbox_chunks = split_large_bbox(overall_bbox, max_area=max_area)
    
    print(f"   📦 Split area into {len(bbox_chunks)} chunks for efficient processing")
    
    # Extract features from each chunk
    all_features = []
    
    def extract_chunk(bbox_chunk):
        print(f"   🔍 Processing chunk: {bbox_chunk}")
        return extractor.extract_features_from_bbox(bbox_chunk, feature_config)
    
    # Use ThreadPoolExecutor for concurrent requests
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        chunk_results = list(executor.map(extract_chunk, bbox_chunks))
    
    # Combine results
    for chunk_features in chunk_results:
        all_features.extend(chunk_features)
    
    print(f"   ✅ Extracted {len(all_features)} total features")
    
    if not all_features:
        return gpd.GeoDataFrame()
    
    # Create GeoDataFrame
    features_gdf = gpd.GeoDataFrame(all_features, crs="EPSG:4326")
    
    # Spatially join with boundaries to get area codes
    print("   🔗 Matching features to boundaries...")
    
    geom_col_name = boundaries_gdf.geometry.name
    features_with_areas = gpd.sjoin(
        features_gdf,
        boundaries_gdf[[area_code_col, geom_col_name]],
        how='inner',
        predicate='within'
    )
    
    print(f"   ✅ {len(features_with_areas)} features matched to boundaries")
    
    return features_with_areas


def add_api_feature_counts_to_boundaries(boundaries_gdf, features_gdf, area_code_col):
    """
    Calculate feature counts by subcategory and category for each boundary area.
    
    Parameters:
    -----------
    boundaries_gdf : GeoDataFrame
        Boundary areas
    features_gdf : GeoDataFrame
        Features extracted from API
    area_code_col : str
        Column name for area codes
    
    Returns:
    --------
    GeoDataFrame
        Boundaries with feature counts added
    """
    if features_gdf.empty:
        print("⚠️ No features found to process.")
        return boundaries_gdf
    
    # Count by subcategory
    subcategory_counts = features_gdf.groupby([area_code_col, 'subcategory']).size().unstack(fill_value=0)
    subcategory_counts.columns = [f"{col}_count" for col in subcategory_counts.columns]
    
    # Count by category
    category_counts = features_gdf.groupby([area_code_col, 'category']).size().unstack(fill_value=0)
    category_counts.columns = [f"{col}_total_count" for col in category_counts.columns]
    
    # Merge with boundaries
    updated_gdf = boundaries_gdf.merge(subcategory_counts, on=area_code_col, how='left')
    updated_gdf = updated_gdf.merge(category_counts, on=area_code_col, how='left')
    
    # Fill NaN values with 0
    count_cols = list(subcategory_counts.columns) + list(category_counts.columns)
    updated_gdf[count_cols] = updated_gdf[count_cols].fillna(0).astype(int)
    
    return updated_gdf


def analyze_osm_features_api(boundaries_gdf, area_code_col, feature_config, 
                           custom_metrics=None, api_type="overpass", 
                           google_api_key=None, max_workers=5):
    """
    Complete workflow to extract, categorize, and count features using either API.
    
    Parameters:
    -----------
    boundaries_gdf : GeoDataFrame
        Boundaries to analyze
    area_code_col : str
        Column name for area codes
    feature_config : list
        List of (key, values, category, subcategory) tuples
    custom_metrics : dict, optional
        Custom metric formulas
    api_type : str
        Either "overpass" or "google"
    google_api_key : str, optional
        Required if using Google Maps API
    max_workers : int
        Maximum concurrent API requests
    
    Returns:
    --------
    GeoDataFrame
        Boundaries with feature counts and custom metrics
    """
    print(f"--- Starting Feature Analysis ({api_type.upper()} API) ---")
    
    # Extract features using selected API
    features_gdf = extract_features_for_boundaries(
        boundaries_gdf, feature_config, area_code_col, 
        api_type, google_api_key, max_workers
    )
    
    if features_gdf.empty:
        print("❌ No features extracted from API.")
        return boundaries_gdf
    
    # Add feature counts to boundaries
    print("📊 Calculating feature counts...")
    final_gdf = add_api_feature_counts_to_boundaries(boundaries_gdf, features_gdf, area_code_col)
    
    # Calculate custom metrics
    if custom_metrics:
        print("🧮 Calculating custom metrics...")
        
        for metric_name, formula in custom_metrics.items():
            try:
                # Extract column names from formula
                referenced_cols = re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', formula)
                python_keywords = {'and', 'or', 'not', 'in', 'is', 'if', 'else', 'for', 'while', 'def', 'class', 'import', 'from', 'as', 'try', 'except', 'finally', 'with', 'lambda', 'yield', 'return', 'break', 'continue', 'pass', 'global', 'nonlocal', 'assert', 'del', 'raise', 'True', 'False', 'None'}
                referenced_cols = [col for col in referenced_cols if col not in python_keywords]
                
                print(f"   Processing '{metric_name}' with formula: {formula}")
                
                # Create missing columns with 0
                missing_cols = []
                for col in referenced_cols:
                    if col not in final_gdf.columns:
                        final_gdf[col] = 0
                        missing_cols.append(col)
                
                if missing_cols:
                    print(f"   ⚠️  Created missing columns with value 0: {missing_cols}")
                
                # Calculate metric
                final_gdf[metric_name] = final_gdf.eval(formula, engine='python')
                print(f"   ✅ Calculated '{metric_name}' score.")
                
            except Exception as e:
                print(f"   ❌ Could not calculate metric '{metric_name}': {e}")
                final_gdf[metric_name] = 0
    
    print("✅ Analysis complete!")
    print(f"📊 Final dataset has {len(final_gdf)} areas with {len([c for c in final_gdf.columns if c.endswith('_count') or c.endswith('_total_count')])} feature count columns")
    
    return final_gdf