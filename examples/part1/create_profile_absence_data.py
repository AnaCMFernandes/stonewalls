#%%
import geopandas as gpd
import time
import os
import sys; sys.path.append('..'); sys.path.append('../lib') 
from lib.core import init

start = time.time() 

path_to_stonewalls = '../../Data/BES_STEN_JORDDIGER_SHAPE/Stonewalls_AEROE.shp'
dtm = '../../Data/DTM/DTM_AEROE.vrt'

stonewalls = gpd.read_file(path_to_stonewalls)

f = stonewalls[['OBJECTID', 'DigeID', 'geometry']].copy()
f['geometry'] = f['geometry'].translate(xoff=20.0, yoff=-50.0)

absence_walls = gpd.GeoDataFrame(f, crs="EPSG:25832")
absence_walls.to_file("data/duplicated_stonewalls.geojson", driver="GeoJSON")

#%%

gdf_a = absence_walls
gdf_a = absence_walls.to_crs(epsg=25832)

out_gdf_a = init(gdf_a, dtm)

out_gdf_a.to_file("data/profiles/ABSENCE_cross_sections.geojson", driver="GeoJSON")

finish = time.time()

print("Time Taken is {0}s".format(finish - start))