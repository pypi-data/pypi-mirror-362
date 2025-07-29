"""
Interactive map creation and visualization functions.

This module provides tools for creating interactive Folium maps with 
Australian city configurations and multi-layer visualizations.
"""

import folium
from folium import plugins
from folium.plugins import Search
import pandas as pd
import numpy as np
import geopandas as gpd
from shapely.geometry import box
from branca.colormap import linear
from branca.element import Element


# Australian cities configuration with bounds and map settings
AUSTRALIAN_CITIES = {
    'Sydney': {
        'location': [-33.8688, 151.2093],
        'bounds': (150.0, -34.6, 152.0, -33.0),
        'zoom_start': 12,
        'min_zoom': 8,
        'max_zoom': 16
    },
    'Melbourne': {
        'location': [-37.8136, 144.9631],
        'bounds': (144.0, -38.5, 146.0, -37.0),
        'zoom_start': 11,
        'min_zoom': 8,
        'max_zoom': 16
    },
    'Brisbane': {
        'location': [-27.4698, 153.0251],
        'bounds': (152.0, -28.2, 154.0, -26.5),
        'zoom_start': 11,
        'min_zoom': 8,
        'max_zoom': 16
    },
    'Perth': {
        'location': [-31.9505, 115.8605],
        'bounds': (115.0, -32.7, 116.5, -31.3),
        'zoom_start': 10,
        'min_zoom': 8,
        'max_zoom': 16
    },
    'Adelaide': {
        'location': [-34.9285, 138.6007],
        'bounds': (138.0, -35.5, 139.5, -34.0),
        'zoom_start': 12,
        'min_zoom': 8,
        'max_zoom': 16
    },
    'Canberra': {
        'location': [-35.2809, 149.1300],
        'bounds': (148.5, -35.9, 149.5, -35.0),
        'zoom_start': 11,
        'min_zoom': 9,
        'max_zoom': 16
    },
    'Darwin': {
        'location': [-12.4634, 130.8456],
        'bounds': (130.5, -13.0, 131.5, -12.0),
        'zoom_start': 12,
        'min_zoom': 9,
        'max_zoom': 16
    },
    'Hobart': {
        'location': [-42.8821, 147.3272],
        'bounds': (146.5, -43.5, 148.0, -42.5),
        'zoom_start': 12,
        'min_zoom': 9,
        'max_zoom': 16
    },
    'Gold Coast': {
        'location': [-28.0167, 153.4000],
        'bounds': (153.0, -28.5, 154.0, -27.5),
        'zoom_start': 12,
        'min_zoom': 9,
        'max_zoom': 16
    },
    'Newcastle': {
        'location': [-32.9267, 151.7789],
        'bounds': (151.0, -33.5, 152.5, -32.0),
        'zoom_start': 12,
        'min_zoom': 9,
        'max_zoom': 16
    },
    'Wollongong': {
        'location': [-34.4278, 150.8931],
        'bounds': (150.0, -35.0, 151.5, -34.0),
        'zoom_start': 12,
        'min_zoom': 9,
        'max_zoom': 16
    },
    'Geelong': {
        'location': [-38.1499, 144.3617],
        'bounds': (144.0, -38.5, 145.0, -37.5),
        'zoom_start': 12,
        'min_zoom': 9,
        'max_zoom': 16
    },
    'Townsville': {
        'location': [-19.2590, 146.8169],
        'bounds': (146.0, -19.8, 147.5, -18.5),
        'zoom_start': 12,
        'min_zoom': 9,
        'max_zoom': 16
    },
    'Cairns': {
        'location': [-16.9203, 145.7781],
        'bounds': (145.0, -17.5, 146.5, -16.0),
        'zoom_start': 12,
        'min_zoom': 9,
        'max_zoom': 16
    }
}


def simplify_geometry(geom, capital_bounds):
    """Simplify geometry based on area and location."""
    if geom is None or geom.is_empty:
        return geom
    area = geom.area
    in_capital = any(geom.within(bounds) for bounds in capital_bounds.values())
    tolerance = (
        (0.004 if area > 1 else 0.0004 if area > 0.1 else 0.0004 if area > 0.01 else 0.0004)
        if in_capital else
        (0.004 if area > 1 else 0.0004 if area > 0.1 else 0.0004 if area > 0.01 else 0.0004)
    )
    return geom.simplify(tolerance, preserve_topology=True)


def filter_gdf_by_city(gdf, city_name, buffer_factor=0.1):
    """
    Filter GeoDataFrame to only include features within or near a specific city.
    
    Parameters:
    -----------
    gdf : GeoDataFrame
        Input geospatial data
    city_name : str
        Name of the city (must be in AUSTRALIAN_CITIES)
    buffer_factor : float
        Buffer factor to expand city bounds (default: 0.1 = 10% buffer)
    
    Returns:
    --------
    GeoDataFrame: Filtered data for the specific city
    """
    if city_name not in AUSTRALIAN_CITIES:
        raise ValueError(f"City '{city_name}' not found. Available cities: {list(AUSTRALIAN_CITIES.keys())}")
    
    city_config = AUSTRALIAN_CITIES[city_name]
    bounds = city_config['bounds']
    
    # Create buffered bounds
    width = bounds[2] - bounds[0]
    height = bounds[3] - bounds[1]
    buffer_x = width * buffer_factor
    buffer_y = height * buffer_factor
    
    buffered_bounds = (
        bounds[0] - buffer_x,  # min_x
        bounds[1] - buffer_y,  # min_y
        bounds[2] + buffer_x,  # max_x
        bounds[3] + buffer_y   # max_y
    )
    
    # Create bounding box
    city_bbox = box(*buffered_bounds)
    
    # Filter GeoDataFrame
    filtered_gdf = gdf[gdf.geometry.intersects(city_bbox)].copy()
    
    if len(filtered_gdf) == 0:
        print(f"⚠️ No features found for {city_name}. You may need to adjust the buffer_factor or check your data coverage.")
    else:
        print(f"✅ Found {len(filtered_gdf)} features for {city_name}")
    
    return filtered_gdf


def setup_base_map(location=[-37.8136, 144.9631], zoom_start=6, min_zoom=5, max_zoom=12, basemap_name="Light Basemap"):
    """Create a base Folium map with CartoDB tiles and custom basemap name."""
    # Create map without default tiles
    m = folium.Map(
        location=location, zoom_start=zoom_start, min_zoom=min_zoom, max_zoom=max_zoom,
        tiles=None,  # No default tiles
        prefer_canvas=True
    )
    
    # Add OpenStreetMap as alternative basemap
    folium.TileLayer(
        tiles="OpenStreetMap",
        name="Street Map",
        control=True,
        overlay=False
    ).add_to(m)

    # Add CartoDB Light tiles with custom name
    folium.TileLayer(
        tiles="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png",
        attr="© CartoDB",
        name=basemap_name,
        control=True,
        overlay=False
    ).add_to(m)
    
    # Hide attribution
    m.get_root().html.add_child(Element(
        "<style>.leaflet-control-attribution {display: none !important;}</style>"
    ))
    return m


def create_style_function(value_column, colormap):
    """Create a style function for GeoJSON layer."""
    def style_function(feature):
        try:
            score = feature['properties'][value_column]
            color = "#cccccc" if pd.isna(score) or not np.isfinite(score) else colormap(score)
            return {"fillColor": color, "color": color, "weight": 1.5, "fillOpacity": 0.7, "opacity": 0.7}
        except Exception:
            return {"fillColor": "#cccccc", "color": "#cccccc", "weight": 1.5, "fillOpacity": 0.7, "opacity": 0.7}
    return style_function


def add_analysis_data_to_gdf(gdf, analysis_data, name_column):
    """
    Automatically add all analysis data to GeoDataFrame by detecting available fields.
    Returns empty popup config if no analysis data provided.
    """
    gdf = gdf.copy()
    
    # Handle case where no analysis data is provided
    if analysis_data is None or len(analysis_data) == 0:
        print("No analysis data provided - popups will be disabled")
        return gdf, {'fields': [], 'aliases': []}
    
    # Auto-detect available fields from the first location in analysis_data
    sample_location = next(iter(analysis_data.values()))
    available_fields = {}
    
    def extract_fields(data, prefix=""):
        """Recursively extract all fields from nested dictionaries while preserving order"""
        fields = {}
        for key, value in data.items():  # This preserves dictionary order (Python 3.7+)
            field_name = f"{prefix}{key}" if prefix else key
            if isinstance(value, dict):
                # Recursively handle nested dictionaries
                nested_fields = extract_fields(value, f"{field_name}_")
                fields.update(nested_fields)
            else:
                # This is a leaf value, add it as a field
                fields[f"analysis_{field_name}"] = key
        return fields
    
    available_fields = extract_fields(sample_location)
    
    # Initialize columns for all detected fields
    for col_name in available_fields.keys():
        if col_name not in gdf.columns:
            gdf[col_name] = "N/A"
    
    # Add analysis data to each row
    for idx, row in gdf.iterrows():
        location_name = str(row[name_column])
        
        if location_name in analysis_data:
            location_data = analysis_data[location_name]
            
            def set_values(data, prefix=""):
                """Recursively set values for nested data"""
                for key, value in data.items():
                    field_name = f"{prefix}{key}" if prefix else key
                    col_name = f"analysis_{field_name}"
                    
                    if isinstance(value, dict):
                        # Recursively handle nested dictionaries
                        set_values(value, f"{field_name}_")
                    else:
                        # Set the leaf value
                        if col_name in gdf.columns:
                            gdf.loc[idx, col_name] = value
            
            set_values(location_data)
    
    # Create popup configuration automatically
    popup_fields = []  # Don't include location name since it's already the popup title
    popup_aliases = []
    
    # Add all analysis fields with clean aliases (preserving original order)
    for col_name in available_fields.keys():  # This maintains the original dictionary order
        popup_fields.append(col_name)
        # Create clean alias by removing 'analysis_' prefix and replacing underscores
        clean_alias = col_name.replace('analysis_', '').replace('_', ' ').title()
        popup_aliases.append(clean_alias)
    
    popup_config = {
        'fields': popup_fields,
        'aliases': popup_aliases
    }
    
    return gdf, popup_config


def create_city_map(
    gdf, city_name, overlays, analysis_data=None, name_column='Location', 
    output_filename=None, buffer_factor=0.1, basemap_name=None, **kwargs
):
    """
    Create a map specifically for a single Australian city.
    
    Parameters:
    -----------
    gdf : GeoDataFrame
        Input geospatial data
    city_name : str
        Name of the city (must be in AUSTRALIAN_CITIES)
    overlays : dict
        Dictionary of layer configurations with column names and properties
    analysis_data : dict or None
        Pre-calculated analysis data (optional)
    name_column : str
        Column name for area labels (default: 'Location')
    output_filename : str
        Output HTML file name (default: auto-generated)
    buffer_factor : float
        Buffer factor to expand city bounds (default: 0.1)
    basemap_name : str
        Custom basemap name (default: city-specific)
    **kwargs : additional arguments passed to create_multi_layer_map_with_analysis
    
    Returns:
    --------
    Folium map object
    """
    if city_name not in AUSTRALIAN_CITIES:
        raise ValueError(f"City '{city_name}' not found. Available cities: {list(AUSTRALIAN_CITIES.keys())}")
    
    # Get city configuration
    city_config = AUSTRALIAN_CITIES[city_name]
    
    # Filter data for the specific city
    city_gdf = filter_gdf_by_city(gdf, city_name, buffer_factor)
    
    if len(city_gdf) == 0:
        print(f"❌ No data found for {city_name}")
        return None
    
    # Set default filename if not provided
    if output_filename is None:
        output_filename = f"{city_name.lower().replace(' ', '_')}_map.html"
    
    # Set default basemap name if not provided
    if basemap_name is None:
        basemap_name = f"{city_name} Light Theme"
    
    # Create the map with city-specific settings
    # Pass the city_config to the main function
    return create_multi_layer_map_with_analysis(
        gdf=city_gdf,
        overlays=overlays,
        analysis_data=analysis_data,
        name_column=name_column,
        output_filename=output_filename,
        min_zoom=city_config['min_zoom'],
        max_zoom=city_config['max_zoom'],
        basemap_name=basemap_name,
        city_config=city_config,  # Pass city config here
        **kwargs
    )


def create_multi_layer_map_with_analysis(
    gdf, overlays, analysis_data=None, name_column='Location', output_filename='multi_layer_map.html',
    min_zoom=5, max_zoom=12, popup_config=None, basemap_name="Light Theme", city_config=None
):
    """
    Create a multi-layer map using pre-calculated analysis data for popups.
    
    Parameters:
    -----------
    gdf : GeoDataFrame
        Input geospatial data
    overlays : dict
        Dictionary of layer configurations with column names and properties
    analysis_data : dict or None
        Pre-calculated analysis data from analyze_service_areas_and_markets() (optional)
    name_column : str
        Column name for area labels (default: 'Location')
    output_filename : str
        Output HTML file name (default: 'multi_layer_map.html')
    min_zoom : int
        Minimum zoom level (default: 5)
    max_zoom : int
        Maximum zoom level (default: 12)
    popup_config : dict or None
        Custom popup configuration (optional)
    basemap_name : str
        Custom basemap name (default: "Light Theme")
    city_config : dict or None
        City configuration from AUSTRALIAN_CITIES (optional)
    
    Returns:
    --------
    Folium map object
    """
    gdf = gdf.copy()
    
    # STEP 1: Aggressively fix duplicate columns FIRST
    print(f"Initial columns: {len(gdf.columns)}")
    print(f"Unique columns: {gdf.columns.is_unique}")
    
    if not gdf.columns.is_unique:
        print("Fixing duplicate columns...")
        gdf = gdf.loc[:, ~gdf.columns.duplicated(keep='first')]
        print(f"After removing duplicates: {len(gdf.columns)} columns")
        
        if not gdf.columns.is_unique:
            print("Still have duplicates, forcing unique names...")
            new_columns = []
            seen = set()
            for col in gdf.columns:
                if col in seen:
                    counter = 1
                    new_col = f"{col}_dup_{counter}"
                    while new_col in seen:
                        counter += 1
                        new_col = f"{col}_dup_{counter}"
                    new_columns.append(new_col)
                    seen.add(new_col)
                else:
                    new_columns.append(col)
                    seen.add(col)
            gdf.columns = new_columns
            print(f"Final unique columns: {gdf.columns.is_unique}")
    
    # STEP 2: Add analysis data to GDF and auto-generate popup config
    gdf, auto_popup_config = add_analysis_data_to_gdf(gdf, analysis_data, name_column)
    
    # Use provided popup_config or auto-generated one
    if popup_config is None:
        popup_config = auto_popup_config
    
    # STEP 3: Final duplicate check after adding analysis data
    if not gdf.columns.is_unique:
        print("Duplicates found after adding analysis data, fixing...")
        gdf = gdf.loc[:, ~gdf.columns.duplicated(keep='first')]
    
    popup_fields = popup_config['fields']
    popup_aliases = popup_config['aliases']
    
    # Check if popups should be enabled
    enable_popups = len(popup_fields) > 0 and analysis_data is not None
    
    # Validate overlays
    valid_overlays = {}
    required_cols = [name_column, 'geometry']
    if enable_popups:
        required_cols.extend(popup_fields)
    
    for layer_name, config in overlays.items():
        col = config['column']
        if col in gdf.columns and len(gdf[col].dropna()) > 0 and gdf[col].dropna().nunique() > 1:
            gdf[col] = gdf[col].astype(float)
            valid_overlays[layer_name] = config
            required_cols.append(col)
        else:
            print(f"⚠️ Skipping '{layer_name}' - invalid data or column")
    
    if not valid_overlays:
        raise ValueError("No valid overlays found")
    
    # Keep only required columns
    available_cols = [col for col in required_cols if col in gdf.columns]
    unique_cols = []
    seen = set()
    for col in available_cols:
        if col not in seen:
            unique_cols.append(col)
            seen.add(col)
    
    gdf = gdf[unique_cols].copy()
    
    # Final safety check
    if not gdf.columns.is_unique:
        print("FINAL duplicate removal...")
        gdf = gdf.loc[:, ~gdf.columns.duplicated(keep='first')]
    
    print(f"Final GDF has {len(gdf.columns)} unique columns: {gdf.columns.is_unique}")
    print(f"Popups enabled: {enable_popups}")
    
    # Set default layer
    default_layer = next((name for name, config in valid_overlays.items() if config.get('default')), 
                        list(valid_overlays.keys())[0])
    default_value_column = valid_overlays[default_layer]['column']
    gdf = gdf[gdf[default_value_column].notna() & gdf.geometry.notnull() & gdf.geometry.is_valid]
    
    # FIXED: Determine map center - use city config if available, otherwise calculate from bounds
    if city_config is not None:
        # Use predefined city location and zoom settings
        location = city_config['location']
        zoom_start = city_config['zoom_start']
        print(f"Using predefined location for city: {location}")
    else:
        # Calculate center from data bounds (original behavior for non-city maps)
        if len(gdf) > 0:
            bounds = gdf.total_bounds
            center_lat = (bounds[1] + bounds[3]) / 2
            center_lon = (bounds[0] + bounds[2]) / 2
            location = [center_lat, center_lon]
            zoom_start = 12
        else:
            location = [-37.8136, 144.9631]  # Default to Melbourne
            zoom_start = 12
        print(f"Using calculated location from data bounds: {location}")
    
    # Simplify geometries
    capital_bounds = {
        city: box(*coords['bounds']) for city, coords in AUSTRALIAN_CITIES.items()
    }
    gdf.geometry = gdf.geometry.apply(lambda g: simplify_geometry(g, capital_bounds))
    
    # Setup map with custom basemap name and proper location/zoom
    map_obj = setup_base_map(
        location=location, 
        zoom_start=zoom_start,  # Use city-specific or calculated zoom
        min_zoom=min_zoom, 
        max_zoom=max_zoom, 
        basemap_name=basemap_name
    )
    
    # Create layers
    colormap_options = {
        'YlOrRd_09': linear.YlOrRd_09, 'Blues_09': linear.Blues_09, 'Reds_09': linear.Reds_09,
        'Greens_09': linear.Greens_09, 'Purples_09': linear.Purples_09, 'Oranges_09': linear.Oranges_09,
        'BuPu_09': linear.BuPu_09, 'RdYlBu_11': linear.RdYlBu_11, 'viridis': linear.viridis, 'plasma': linear.plasma,
    }
    
    geojson_layers = {}
    legend_html = (
        '<style>#custom-legend {position: fixed; top: 70px; right: 10px; background-color: white; '
        'border: 2px solid rgba(0,0,0,0.2); border-radius: 4px; padding: 8px; font-size: 12px; z-index: 1000;}'
        '.legend-item {margin-bottom: 5px;}.legend-title {font-weight: bold; margin-bottom: 3px; font-size: 12px;}'
        '.legend-scale {display: flex; align-items: center; margin-bottom: 2px;}'
        '.legend-bar {width: 120px; height: 12px; margin-right: 5px;}'
        '.legend-labels {display: flex; justify-content: space-between; width: 120px; font-size: 10px;}</style>'
        '<div id="custom-legend">'
    )
    
    for i, (layer_name, config) in enumerate(valid_overlays.items()):
        value_column = config['column']
        caption = config['caption']
        colormap_name = config.get('colormap', 'YlOrRd_09')
        max_value = config.get('max_value')
        
        min_val, max_val = gdf[value_column].min(), gdf[value_column].max()
        if max_value is not None:
            max_val = max_value
        
        colormap = colormap_options.get(colormap_name, linear.YlOrRd_09).scale(min_val, max_val)
        colormap.caption = caption
        
        # Create GeoJSON layer with conditional popup/tooltip
        geojson_kwargs = {
            'data': gdf,
            'name': layer_name,
            'style_function': create_style_function(value_column, colormap)
        }
        
        # Add popup only if analysis data is available
        if enable_popups:
            geojson_kwargs['popup'] = folium.GeoJsonPopup(
                fields=popup_fields, 
                aliases=popup_aliases, 
                max_width=350,
                labels=True, 
                style="font-family: Arial, sans-serif; font-size: 12px;"
            )
        
        # Add tooltip (always show basic info)
        tooltip_fields = [name_column, value_column]
        tooltip_aliases = ["Area", caption]
        geojson_kwargs['tooltip'] = folium.GeoJsonTooltip(
            fields=tooltip_fields,
            aliases=tooltip_aliases,
            localize=True,
            sticky=True
        )
        
        geojson_layer = folium.GeoJson(**geojson_kwargs)
        
        fg = folium.FeatureGroup(name=layer_name, show=layer_name == default_layer)
        geojson_layer.add_to(fg)
        fg.add_to(map_obj)
        geojson_layers[layer_name] = geojson_layer
        
        # Add legend
        stops = [f"{colormap(min_val + (max_val - min_val) * j / 8)} {j * 12.5}%" for j in range(9)]
        gradient = f"linear-gradient(to right, {', '.join(stops)})"
        labels = (
            [f"{v:.2f}" for v in [min_val, (min_val + max_val) / 2, max_val]] if max_val < 1 else
            [f"{int(v)}" for v in [min_val, (min_val + max_val) / 2, max_val]]
        )
        legend_html += (
            f'<div class="legend-item"><div class="legend-title">{layer_name}</div>'
            f'<div class="legend-scale"><div class="legend-bar" style="background: {gradient};"></div></div>'
            f'<div class="legend-labels"><span>{labels[0]}</span><span>{labels[1]}</span><span>{labels[2]}</span></div></div>'
        )
        if i < len(valid_overlays) - 1:
            legend_html += '<hr style="margin: 5px 0; border: 0; border-top: 1px solid #ddd;">'
    
    legend_html += '</div>'
    map_obj.get_root().html.add_child(Element(legend_html))
    
    # Add custom popup styling only if popups are enabled
    if enable_popups:
        popup_css = """
        <style>
        .leaflet-popup-content {
            padding: 8px !important;
            margin: 0 !important;
        }
        .leaflet-popup-content table {
            border-collapse: separate !important;
            border-spacing: 15px 4px !important;
            margin: 0 !important;
        }
        .leaflet-popup-content table td:first-child {
            padding-right: 20px !important;
            font-weight: bold !important;
            text-align: left !important;
            vertical-align: top !important;
            min-width: 120px !important;
        }
        .leaflet-popup-content table td:last-child {
            text-align: left !important;
            vertical-align: top !important;
            word-wrap: break-word !important;
            max-width: 200px !important;
        }
        .leaflet-popup-content table tr {
            margin-bottom: 6px !important;
        }
        </style>
        """
        map_obj.get_root().html.add_child(Element(popup_css))
    
    map_obj.get_root().html.add_child(Element(
        "<style>.leaflet-control-container .leaflet-bottom.leaflet-right {display: none !important;}</style>"
    ))
    
    # Add search and layer control
    if default_layer in geojson_layers:
        Search(geojson_layers[default_layer], geom_type='Polygon', search_label=name_column,
               placeholder='Search for an area...', collapsed=False).add_to(map_obj)
        map_obj.get_root().header.add_child(Element(
            "<style>.leaflet-control-search {transform: translate(45px, -73px) !important;}</style>"
        ))
    
    folium.LayerControl().add_to(map_obj)
    map_obj.save(output_filename)
    
    if enable_popups:
        print(f"✅ Multi-layer map with popups saved as {output_filename}")
    else:
        print(f"✅ Multi-layer map (tooltips only) saved as {output_filename}")
    
    return map_obj