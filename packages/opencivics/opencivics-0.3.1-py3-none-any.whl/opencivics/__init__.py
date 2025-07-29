"""
OpenCivics Python Package

A comprehensive package for analyzing Australian geospatial data, including:
- Census and ABS boundary data processing
- OpenStreetMap feature extraction (PBF files and API-based)
- Interactive map visualization

Main modules:
- census: Functions for downloading and processing Australian Bureau of Statistics data
- osm: OpenStreetMap data extraction and analysis tools (PBF-based)
- api_extractor: OpenStreetMap data extraction using Overpass API
- mapping: Interactive map creation and visualization functions
"""

from .census import (
    download_aus_boundary_files,
    load_abs_boundaries,
    merge_with_boundaries,
    get_population_with_boundaries
)

from .osm import (
    FeatureHandler,
    extract_features_from_pbf,
    add_feature_counts_to_boundaries,
    analyze_osm_features,
    FEATURE_TAGS
)

from .api_extractor import (
    BaseAPIExtractor,
    OverpassAPIExtractor,
    GoogleMapsAPIExtractor,
    get_boundary_bbox,
    split_large_bbox,
    extract_features_for_boundaries,
    add_api_feature_counts_to_boundaries,
    analyze_osm_features_api
)

from .mapping import (
    AUSTRALIAN_CITIES,
    filter_gdf_by_city,
    setup_base_map,
    create_city_map,
    create_multi_layer_map_with_analysis
)

__version__ = "0.3.1"
__author__ = "Alexander Tashevski"
__all__ = [
    # Census functions
    'download_aus_boundary_files',
    'load_abs_boundaries', 
    'merge_with_boundaries',
    'get_population_with_boundaries',
    
    # OSM functions (PBF-based)
    'FeatureHandler',
    'extract_features_from_pbf',
    'add_feature_counts_to_boundaries',
    'analyze_osm_features',
    'FEATURE_TAGS',
    
    # API extractor functions
    'BaseAPIExtractor',
    'OverpassAPIExtractor',
    'GoogleMapsAPIExtractor',
    'get_boundary_bbox',
    'split_large_bbox',
    'extract_features_for_boundaries',
    'add_api_feature_counts_to_boundaries',
    'analyze_osm_features_api',
    
    # Mapping functions
    'AUSTRALIAN_CITIES',
    'filter_gdf_by_city',
    'setup_base_map',
    'create_city_map',
    'create_multi_layer_map_with_analysis'
]