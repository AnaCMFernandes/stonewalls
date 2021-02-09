#%%
import geopandas as gpd
import time
import sys; sys.path.append('..'); sys.path.append('../lib')
from lib.core import init

path_to_stonewalls = '../data/stonewalls/aeroe/Stonewalls_AEROE.shp'

start = time.time()

gdf = gpd.read_file(path_to_stonewalls)
gdf = gdf.to_crs(epsg=25832)
dtm = '../data/DTM/DTM_AEROE/DTM_AEROE.vrt'
# sub_gdf = gdf[10:11]

out_gdf = init(gdf, dtm)

out_gdf.to_file("/data/profiles/completed_cross_sections_2.geojson", driver="GeoJSON")

finish = time.time()

print("Time Taken is {0}s".format(finish - start))

# %%
