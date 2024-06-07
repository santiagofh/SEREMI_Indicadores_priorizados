#%%
import geopandas as gpd
comunas_rm = gpd.read_file('data_raw/DPA_RM.geojson')
comunas_rm.to_file('data_clean/Comunas_RM.geojson', driver='GeoJSON')
# %%
