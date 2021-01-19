#%%
from osgeo import gdal, ogr
import os
import numpy as np
import geopandas as gpd
import shapely
from shapely.geometry import Point, LineString, MultiPoint
from shapely.ops import unary_union, substring
import matplotlib.pyplot as plt

#%%
# Elevation data
DTM = '/mnt/c/Users/AFER/Documents/Projects/StoneWalls/Data/DTM/DTM_AEROE.vrt'
UTM32 = '+proj=utm +zone=32 +ellps=GRS80 +units=m +no_defs'

# %%
# Stonewalls

layer = gpd.read_file('/mnt/c/Users/EZRA/OneDrive - NIRAS/thesis/Data/Aeroe/Stonewalls')
layer = layer.to_crs(epsg=25832)

layer['length'] = layer.geometry.length

#%%
##function to insert points at defined equidistance along each LineString
def insertPoint(lineString, sampleCount):
    for index, row in lineString.iterrows():
        line = row['geometry']
        stepLength = line.length / (sampleCount - 1)
        distances = np.arange(0, line.length, stepLength)
        points = [line.interpolate(distance) for distance in distances]
        multipoint = unary_union(points)
        print(multipoint)
        

selection = layer[0:5]    
insertPoint(selection, 10.0)
# print(sample)

#%%
#Another way of doing it

mp = shapely.geometry.MultiPoint()
 
for i in  np.arange(0, line.length, stepLength):
    s = substring(line, i, i+stepLength)
    mp = mp.union(s.boundary)

