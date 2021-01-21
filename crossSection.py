#%%
from osgeo import gdal, ogr
import os
import numpy as np
import geopandas as gpd
import shapely
from shapely.geometry import Point, LineString, MultiPoint
from shapely.ops import unary_union, substring
import matplotlib.pyplot as plt
import sys, math
from LOCAL_VARS import DTM, STONEWALLS

#%%
# Elevation data
theDTM = DTM
UTM32 = '+proj=utm +zone=32 +ellps=GRS80 +units=m +no_defs'

# %%
# Stonewalls

layer = gpd.read_file(STONEWALLS)
layer = layer.to_crs(epsg=25832)

layer['length'] = layer.geometry.length

#%%
#Attempt of function, stored in the dataframe:

def redistribute_vertices(geom, distance):
    if geom.geom_type == 'LineString':
        num_vert = int(round(geom.length / distance))
        if num_vert == 0:
            num_vert = 1
        return LineString(
            [geom.interpolate(float(n) / num_vert, normalized=True)
             for n in range(num_vert + 1)])
    elif geom.geom_type == 'MultiLineString':
        parts = [redistribute_vertices(part, distance)
                 for part in geom]
        return type(geom)([p for p in parts if not p.is_empty])
    else:
        raise ValueError('unhandled geometry %s', (geom.geom_type,))


# %%
#updating the geometry of each linestring
gdf_line = layer[0:5]  

gdf_line_interpolate = gdf_line.copy()
gdf_line_interpolate.geometry = gdf_line.geometry.apply(redistribute_vertices,distance=15)
gdf_line_interpolate['nverts'] = gdf_line_interpolate.geometry.apply(lambda x: len(x.coords))

#%%
#or just adding the attribute column:
gdf_line_interpolate = gdf_line.copy()
gdf_line_interpolate['nverts'] = gdf_line.geometry.apply(redistribute_vertices,distance=15).apply(lambda x: len(x.coords))


#%%
##function attempt to insert points at defined equidistance along each LineString - wroking partially
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
##another way of doing, simple extraction

mp = shapely.geometry.MultiPoint()
line = layer['geometry'][0]
sampleCount = 10.0
stepLength = line.length / (sampleCount - 1)

for i in  np.arange(0, line.length, stepLength):
    s = substring(line, i, i+stepLength)
    mp = mp.union(s.boundary)

