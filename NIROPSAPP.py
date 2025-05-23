# import streamlit as st
# import geopandas as gpd
# import tempfile
# import requests
# import zipfile
# import folium
# from streamlit_folium import st_folium

# # --- GitHub ZIP download URL (must contain all SHP components)
# ZIP_URL = "https://github.com/ShayneGeo/NIROPS/raw/main/Data/WA-OWF-000453_SchneiderSprings.zip"

# st.title("🔥 Displaying NIROPS Shapefile on a Map")

# @st.cache_data
# def load_shapefile_from_zip(zip_url):
#     response = requests.get(zip_url)
#     response.raise_for_status()

#     with tempfile.TemporaryDirectory() as tmpdir:
#         zip_path = f"{tmpdir}/file.zip"
#         with open(zip_path, "wb") as f:
#             f.write(response.content)

#         with zipfile.ZipFile(zip_path, "r") as zip_ref:
#             zip_ref.extractall(tmpdir)

#         shp_files = [f for f in zip_ref.namelist() if f.endswith(".shp")]
#         if not shp_files:
#             raise FileNotFoundError("No .shp file found in ZIP.")
        
#         shp_path = f"{tmpdir}/{shp_files[0]}"
#         gdf = gpd.read_file(shp_path)
#         return gdf

# # Load shapefile
# try:
#     gdf = load_shapefile_from_zip(ZIP_URL)
#     st.success("Shapefile loaded successfully!")

#     # Create a Folium map centered on the shapefile
#     center = gdf.geometry.centroid.iloc[0].coords[0][::-1]  # (lat, lon)
#     m = folium.Map(location=center, zoom_start=10)
#     #folium.GeoJson(gdf).add_to(m)
#     # Convert Timestamp columns to string
#     gdf_clean = gdf.copy()
#     for col in gdf_clean.columns:
#         if gdf_clean[col].dtype.name == "datetime64[ns]":
#             gdf_clean[col] = gdf_clean[col].astype(str)
    
#     folium.GeoJson(gdf_clean).add_to(m)


#     # Display the map
#     st_folium(m, width=700, height=500)

#     # Show attribute table
#     if st.checkbox("Show attribute table"):
#         st.dataframe(gdf)

# except Exception as e:
#     st.error(f"Failed to load shapefile: {e}")



import streamlit as st
import geopandas as gpd
import pandas as pd
import tempfile
import requests
import zipfile
import folium
from streamlit_folium import st_folium

ZIP_URL = "https://github.com/ShayneGeo/NIROPS/raw/main/Data/WA-OWF-000453_SchneiderSprings.zip"

st.title("🔥 Displaying NIROPS Shapefile on a Map")

@st.cache_data
def load_shapefile_from_zip(zip_url):
    response = requests.get(zip_url)
    response.raise_for_status()
    with tempfile.TemporaryDirectory() as tmpdir:
        zip_path = f"{tmpdir}/file.zip"
        with open(zip_path, "wb") as f:
            f.write(response.content)
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(tmpdir)
        shp_files = [f for f in zip_ref.namelist() if f.endswith(".shp")]
        if not shp_files:
            raise FileNotFoundError("No .shp file found in ZIP.")
        shp_path = f"{tmpdir}/{shp_files[0]}"
        return gpd.read_file(shp_path)

try:
    gdf = load_shapefile_from_zip(ZIP_URL)
    st.success("Shapefile loaded successfully!")
    center = gdf.geometry.centroid.iloc[0].coords[0][::-1]
    m = folium.Map(location=center, zoom_start=10)
    gdf_clean = gdf.copy()
    for col in gdf_clean.columns:
        if pd.api.types.is_datetime64_any_dtype(gdf_clean[col]):
            gdf_clean[col] = gdf_clean[col].astype(str)
        gdf_clean[col] = gdf_clean[col].map(lambda x: x.isoformat() if isinstance(x, pd.Timestamp) else x)
    folium.GeoJson(gdf_clean).add_to(m)
    st_folium(m, width=700, height=500)
    if st.checkbox("Show attribute table"):
        st.dataframe(gdf)
except Exception as e:
    st.error(f"Failed to load shapefile: {e}")




