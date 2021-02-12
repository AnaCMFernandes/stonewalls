#%%
import geopandas as gpd
import time
import os
import sys; sys.path.append('..'); sys.path.append('../lib')
from lib.core import init

start = time.time() 

path_to_stonewalls = '../../Data/BES_STEN_JORDDIGER_SHAPE/Stonewalls_AEROE.shp'

gdf = gpd.read_file(path_to_stonewalls)
gdf = gdf.to_crs(epsg=25832)
dtm = '../../Data/DTM/DTM_AEROE.vrt'

#sub_gdf = gdf[20:70]

out_gdf = init(gdf, dtm)

out_gdf.to_file("cross_sections_50_test_diff.geojson", driver="GeoJSON")

finish = time.time()

print("Time Taken is {0}s".format(finish - start))

# %%
