#%%
import os
import math
import numpy as np
import sys, math
import geopandas as gpd
from shapely.geometry import Polygon, Point, LineString
from shapely.affinity import translate
from osgeo import gdal, ogr
import matplotlib.pyplot as plt
import make_crossline_absence as amkcross
import wall_score

import time

path_to_file = 'data/stonewalls/aeroe/Stonewalls_AEROE.shp'

stonewalls = gpd.read_file(path_to_file)

# %%
f = stonewalls[['OBJECTID', 'DigeID', 'geometry']].copy()

f['geometry'] = f['geometry'].translate(xoff=20.0, yoff=-50.0)

absence_walls = gpd.GeoDataFrame(f, crs="EPSG:25832")

absence_walls.to_file("data/duplicated_stonewalls.geojson", driver="GeoJSON")

#%%
start = time.time()

gdf2 = absence_walls
gdf2 = absence_walls.to_crs(epsg=25832)

out_gdf2 = amkcross.init(gdf2)

out_gdf2.to_file("data/3D_ABSENCE_cross_sections.geojson", driver="GeoJSON")

finish = time.time()

print("Time Taken is {0}s".format(finish - start))