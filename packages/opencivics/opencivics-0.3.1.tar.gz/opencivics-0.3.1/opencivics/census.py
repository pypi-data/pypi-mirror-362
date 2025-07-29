"""
Census and Australian Bureau of Statistics (ABS) boundary data functions.

This module provides functions for downloading, loading, and processing Australian
statistical geography data including suburbs (SAL) and local government areas (LGA).
"""

import os
import zipfile
import requests
import pandas as pd
import geopandas as gpd
from pathlib import Path


def download_aus_boundary_files(download_dir="aus_boundaries"):
    """
    Download Australian Statistical Geography Standard boundary files
    """
    
    # Create download directory
    Path(download_dir).mkdir(exist_ok=True)
    
    # ABS Digital Boundary Files URLs (these are the current ASGS Edition 3 2021)
    boundary_urls = {
        'SAL': 'https://www.abs.gov.au/statistics/standards/australian-statistical-geography-standard-asgs-edition-3/jul2021-jun2026/access-and-downloads/digital-boundary-files/SAL_2021_AUST_GDA2020_SHP.zip',
        'LGA': 'https://www.abs.gov.au/statistics/standards/australian-statistical-geography-standard-asgs-edition-3/jul2021-jun2026/access-and-downloads/digital-boundary-files/LGA_2021_AUST_GDA2020_SHP.zip'
    }
    
    downloaded_files = {}
    
    for boundary_type, url in boundary_urls.items():
        zip_path = os.path.join(download_dir, f"{boundary_type}_2021_AUST.zip")
        extract_path = os.path.join(download_dir, boundary_type)
        
        if not os.path.exists(zip_path):
            print(f"📥 Downloading {boundary_type} boundaries...")
            try:
                response = requests.get(url, stream=True)
                response.raise_for_status()
                
                with open(zip_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                print(f"✅ Downloaded {boundary_type} boundaries")
                
            except Exception as e:
                print(f"❌ Failed to download {boundary_type}: {e}")
                continue
        
        # Extract if not already extracted
        if not os.path.exists(extract_path):
            print(f"📂 Extracting {boundary_type} boundaries...")
            try:
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_path)
                print(f"✅ Extracted {boundary_type} boundaries")
            except Exception as e:
                print(f"❌ Failed to extract {boundary_type}: {e}")
                continue
        
        # Find the shapefile
        shp_files = list(Path(extract_path).glob("*.shp"))
        if shp_files:
            downloaded_files[boundary_type] = str(shp_files[0])
        
    return downloaded_files


def load_abs_boundaries(boundary_files, boundary_type, state_filter=None):
    """
    Loads Australian Bureau of Statistics (ABS) boundary shapefiles.

    Args:
        boundary_files (dict): A dictionary with paths to the shapefiles, keyed by type (e.g., 'SAL', 'LGA').
        boundary_type (str): The type of boundary to load ('SAL' or 'LGA').
        state_filter (list, optional): A list of states to filter the boundaries by.

    Returns:
        geopandas.GeoDataFrame: A GeoDataFrame with the specified boundaries or None if an error occurs.
    """
    if boundary_type not in boundary_files:
        print(f"❌ {boundary_type} boundary file not found in the provided dictionary.")
        return None

    # Define the column names for different boundary types
    # This allows the function to adapt to either SAL or LGA data.
    col_map = {
        'SAL': {'code': 'SAL_CODE21', 'name': 'SAL_NAME21', 'state': 'STE_NAME21'},
        'LGA': {'code': 'LGA_CODE21', 'name': 'LGA_NAME21', 'state': 'STE_NAME21'}
    }
    
    # Select the correct column names for the specified boundary type
    cols = col_map.get(boundary_type)
    if not cols:
        print(f"❌ Column mapping for '{boundary_type}' is not defined.")
        return None

    # Load the shapefile into a GeoDataFrame
    gdf = gpd.read_file(boundary_files[boundary_type])

    # Filter by state if a filter is provided
    if state_filter and cols['state'] in gdf.columns:
        gdf = gdf[gdf[cols['state']].isin(state_filter)].copy()

    # Rename columns to a consistent, generic format
    rename_dict = {
        cols['code']: 'area_code',
        cols['name']: 'area_name',
        cols['state']: 'state'
    }
    gdf.rename(columns={k: v for k, v in rename_dict.items() if k in gdf.columns}, inplace=True)
    
    return gdf


def merge_with_boundaries(data_df, boundary_files, boundary_type, merge_on_col, state_filter=None):
    """
    Merges a DataFrame with ABS boundary data and calculates centroids.

    Args:
        data_df (pd.DataFrame): Your DataFrame containing census or other data.
        boundary_files (dict): Dictionary with paths to boundary shapefiles.
        boundary_type (str): The type of boundary to merge with ('SAL' or 'LGA').
        merge_on_col (str): The name of the column in your data_df that contains the area codes.
        state_filter (list, optional): A list of states to filter by.

    Returns:
        geopandas.GeoDataFrame: A GeoDataFrame with the merged data and geometry.
    """
    # Load the corresponding boundary geometries
    boundaries_gdf = load_abs_boundaries(boundary_files, boundary_type, state_filter)
    if boundaries_gdf is None:
        return None # Exit if boundaries couldn't be loaded

    df_clean = data_df.copy()
    
    # Clean the merge key by removing the text prefix (e.g., 'SAL' from 'SAL12345')
    # This makes the user's code compatible with the numeric code in the shapefile.
    boundaries_gdf['area_code'] = boundaries_gdf['area_code'].astype(str)
    df_clean[merge_on_col] = df_clean[merge_on_col].astype(str).str.replace(boundary_type, '', regex=False)

    # Merge the user's data with the geographic boundaries
    merged_gdf = boundaries_gdf.merge(
        df_clean,
        left_on='area_code',
        right_on=merge_on_col,
        how='inner'
    )
    
    print(f"✅ Merged {len(merged_gdf)} records with {boundary_type} boundaries.")

    # Calculate centroids for mapping or routing applications
    # A projected CRS (like EPSG:3577) is used for accurate geometric calculations
    projected_centroids = merged_gdf.to_crs('EPSG:3577').geometry.centroid
    
    # Convert centroids back to standard lat/lon (WGS84)
    merged_gdf['centroid'] = projected_centroids.to_crs('EPSG:4326')
    
    # Extract coordinates, handling any invalid geometries gracefully
    merged_gdf['coord'] = merged_gdf['centroid'].apply(lambda pt: (pt.x, pt.y) if pd.notna(pt) else None)
    
    # Filter out any rows that failed to produce valid coordinates
    valid_coords = merged_gdf['coord'].notna()
    if not valid_coords.all():
        print(f"⚠️ Warning: {(~valid_coords).sum()} records have invalid geometries and were excluded.")
        merged_gdf = merged_gdf[valid_coords].copy()
        
    return merged_gdf


def get_population_with_boundaries(census_csv_path, index_excel_path, boundary_files_path, state_filter=None):
    """
    Process census population data and merge with geographical boundaries.
    
    Parameters:
    -----------
    census_csv_path : str
        Path to the census CSV file (e.g., '2021Census_G01_AUST_SAL.csv')
    index_excel_path : str
        Path to the index Excel file (e.g., 'id_index.xlsx')
    boundary_files_path : str
        Path to the directory containing boundary files
    state_filter : list or None, optional
        List of state codes to filter by, or None for all states
    
    Returns:
    --------
    geopandas.GeoDataFrame
        Merged dataframe with population data and geographical boundaries
    """
    
    # Define state mapping
    sal_index = {
        1: "New South Wales",
        2: "Victoria", 
        3: "Queensland",
        4: "South Australia",
        5: "Western Australia",
        6: "Tasmania",
        7: "Northern Territory",
        8: "Australian Capital Territory",
        9: "Other territories"
    }
    
    # Read population data
    locations_census = pd.read_csv(census_csv_path)
    locations_index = pd.read_excel(index_excel_path, sheet_name='2021_ASGS_Non_ABS_Structures')
    
    # Filter for SAL (Suburbs and Localities) data
    df1 = locations_index.loc[locations_index["ASGS_Structure"] == "SAL", 
                             ['Census_Code_2021', 'Census_Name_2021']]
    df2 = locations_census.loc[:,["SAL_CODE_2021","Tot_P_P"]]
    
    # Merge census data with location index
    master_df = pd.merge(df1, df2, left_on='Census_Code_2021', right_on='SAL_CODE_2021').copy()
    master_df.drop(columns=['Census_Code_2021'], inplace=True)
    
    # Add state column
    master_df.insert(
        1, # Position after suburbs index
        'State',
        master_df['SAL_CODE_2021'].str.extract(r'SAL(\d)')[0].astype(int).map(sal_index)
    )
    
    # Add cleaned suburb column
    master_df.insert(
        1, # Position after suburbs index
        'Suburb_clean',
        master_df['Census_Name_2021'].str.replace(r"\s*\(.*?\)", "", regex=True).str.strip()
    )
    
    # Rename suburb column and clean SAL codes
    master_df = master_df.rename(columns={'Census_Name_2021': 'Suburb'})
    master_df['SAL_CODE_2021'] = master_df['SAL_CODE_2021'].astype(str).str.replace('SAL', '', regex=False)
    
    # Get shape files for geography
    boundary_files = download_aus_boundary_files(boundary_files_path)
    boundaries_gdf = load_abs_boundaries(boundary_files, boundary_type='SAL', state_filter=state_filter)
    merged_gdf = merge_with_boundaries(master_df, boundary_files, boundary_type='SAL', 
                                     merge_on_col='SAL_CODE_2021', state_filter=state_filter)
    
    # Clean up columns
    merged_gdf = merged_gdf.drop(columns=['area_name', 'STE_CODE21', 'AUS_CODE21', 'state'])
    merged_gdf = merged_gdf.rename(columns={'Suburb': 'Location', 'Suburb_clean': 'Location_clean'})
    
    return merged_gdf