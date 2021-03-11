#%%
import geopandas as gpd
import time
import sys; sys.path.append('/home/ezra/stonewalls/lib')

from core import create_profiles

start = time.time() 

path_to_stonewalls = '/home/ezra/stonewalls/data/stonewalls/Stonewalls_AEROE.shp'
dtm = '/home/ezra/stonewalls/data/DTM/DTM_AEROE/DTM_AEROE.vrt'
output_folder = '/home/ezra/stonewalls/data/profiles/geojson/'

gdf = gpd.read_file(path_to_stonewalls)
gdf = gdf.to_crs(epsg=25832)

#sub_gdf = gdf[20:70]

profiles, walls = create_profiles(gdf, dtm)

profiles.to_file(output_folder + "all_profiles_110321.geojson", driver="GeoJSON")
walls.to_file(output_folder + "all_walls_110321.geojson", driver="GeoJSON")

finish = time.time()

print("Time Taken is {0}s".format(finish - start))

# %%
