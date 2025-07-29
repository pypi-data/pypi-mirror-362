# OpenCivics Python Package

A comprehensive Python package for analyzing Australian geospatial data, including census data, OpenStreetMap features, and interactive map visualization.

## Features

### 🏛️ Census & ABS Data (`census` module)
- Download Australian Statistical Geography Standard (ASGS) boundary files
- Load and process Suburbs and Localities (SAL) and Local Government Areas (LGA) data
- Merge census data with geographical boundaries
- Calculate centroids for mapping applications

### 🗺️ Location Data Extraction 
**PBF-based (`osm` module):**
- Extract features from large OSM PBF files using configurable tag rules
- Spatial analysis of amenities, services, and infrastructure
- Built-in feature configurations for Australian contexts
- Custom metrics calculation for urban analysis

**API-based (`api_extractor` module):**
- **OpenStreetMap Overpass API**: Free, no API key required
- **Google Maps Places API**: Commercial data with ratings and reviews
- No need to download large PBF files
- Automatic chunking for large areas
- Concurrent processing for faster extraction
- Same feature configuration system as PBF extraction

### 📊 Interactive Mapping (`mapping` module)
- Create interactive Folium maps with Australian city presets
- Multi-layer visualizations with custom styling
- Automated popup generation from analysis data
- City-specific zoom levels and bounds for major Australian cities

## Installation

```bash
pip install -e .
```

For development:
```bash
pip install -e ".[dev]"
```

## Quick Start

### Option 1: Using OpenStreetMap Overpass API (Free)

```python
import opencivics

# Download and load ABS boundary data
boundary_files = opencivics.download_aus_boundary_files("boundaries/")
boundaries = opencivics.load_abs_boundaries(boundary_files, "SAL", state_filter=["Victoria"])

# Extract OSM features using Overpass API (no PBF file needed!)
analysis_result = opencivics.analyze_osm_features_api(
    boundaries_gdf=boundaries,
    area_code_col='area_code',
    feature_config=opencivics.FEATURE_TAGS,
    api_type="overpass",  # Free OpenStreetMap data
    max_workers=3
)

# Create an interactive map for Melbourne
map_config = {
    'Schools': {'column': 'school_count', 'caption': 'Number of Schools', 'default': True},
    'Retail': {'column': 'retail_count', 'caption': 'Retail Outlets'}
}

melbourne_map = opencivics.create_city_map(
    analysis_result, 
    'Melbourne', 
    map_config, 
    output_filename='melbourne_analysis.html'
)
```

### Option 2: Using Google Maps API (Commercial)

```python
import opencivics

# Same boundary setup as above...

# Extract features using Google Maps API (requires API key)
analysis_result = opencivics.analyze_osm_features_api(
    boundaries_gdf=boundaries,
    area_code_col='area_code',
    feature_config=opencivics.FEATURE_TAGS,
    api_type="google",
    google_api_key="YOUR_GOOGLE_API_KEY",
    max_workers=2  # Be conservative with commercial API
)

# Same mapping code as above...
```

### Option 3: Using PBF Files (For large-scale analysis)

```python
import opencivics

# Download and load ABS boundary data
boundary_files = opencivics.download_aus_boundary_files("boundaries/")
boundaries = opencivics.load_abs_boundaries(boundary_files, "SAL", state_filter=["Victoria"])

# Extract OSM features from PBF file
analysis_result = opencivics.analyze_osm_features(
    boundaries, "australia.osm.pbf", "area_code", opencivics.FEATURE_TAGS
)

# Same mapping code as above...
```

## Supported Australian Cities

The package includes predefined configurations for:
- Sydney, Melbourne, Brisbane, Perth, Adelaide
- Canberra, Darwin, Hobart
- Gold Coast, Newcastle, Wollongong, Geelong, Townsville, Cairns

## Dependencies

- pandas, geopandas, shapely
- requests (for downloading ABS data)
- folium, branca (for interactive maps)
- osmium (for OSM data processing)
- numpy, openpyxl

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions welcome! Please read our contributing guidelines and submit pull requests.