#%%
from osgeo import gdal, ogr
import sys, math
import numpy as np
from shapely.geometry import Point, LineString, MultiPoint
import geopandas as gpd
import matplotlib.pyplot as plt
import LOCAL_VARS 
from getHeights import getHeights
from crossSection import redistribute_vertices
import make_crossline as mkcross

#%%
# Stonewalls
layer = gpd.read_file(LOCAL_VARS.STONEWALLS)
layer = layer.to_crs(epsg=25832)

# Elevation data
DTM = LOCAL_VARS.DTM
UTM32 = '+proj=utm +zone=32 +ellps=GRS80 +units=m +no_defs'

#%%
line = layer['geometry'][0]
linestring = redistribute_vertices(line, 10.0)
coords = list(linestring.coords)

for i, p in enumerate(coords):
    vert = Point(p)
    pd = linestring.project(Point(p))
    dist = pd+0.5
    bearing_point = linestring.interpolate(dist)
    bearing = mkcross.calculate_initial_compass_bearing(vert.coords[0], bearing_point.coords[0])
    #print(bearing)
    cross = mkcross.make_crossline(vert, bearing, 10.0)
    #print(cross)
    cross_points = redistribute_vertices(cross, 0.5)
    # print(cross_points)
    heights = getHeights(cross_points, DTM)
    print(heights)
# %%
