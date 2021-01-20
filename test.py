#%%
from osgeo import gdal, ogr
import os
import math
import numpy as np
import geopandas as gpd
import shapely
from shapely.geometry import Point, LineString, MultiPoint
from shapely.ops import unary_union, substring
import matplotlib.pyplot as plt
from pyproj import Transformer
import LOCAL_VARS


#%%
layer = gpd.read_file(LOCAL_VARS.STONEWALLS)
layer = layer.to_crs(epsg=25832)

layer['length'] = layer.geometry.length

#%%
##function to insert points at defined equidistance along each LineString
def insertPoint(lineString, sampleCount):
   crossSections = []
   for index, row in lineString.iterrows():
      line = row['geometry']
      stepLength = line.length / (sampleCount - 1)
      distances = np.arange(0, line.length, stepLength)
      points = [line.interpolate(distance) for distance in distances]
      multipoint = unary_union(points)
      crossSections.append(multipoint)
   return crossSections

selection = layer[0:5]    
sections = insertPoint(selection, 10.0)
# print(sample)
# %%
def getHeights(points, DTM):
   dataset = gdal.Open(DTM, gdal.GA_ReadOnly)
   band = dataset.GetRasterBand(1)

   transform = dataset.GetGeoTransform()
   pixelWidth = abs(transform[1])
   pixelHeight = abs(transform[5])

   xOrigin = transform[0]
   yOrigin = transform[3]

   elevation = []
   for point in points:

      px = int((point.x - xOrigin) / pixelWidth)
      py = int((yOrigin - point.y) / pixelHeight)

      
      data = band.ReadAsArray(px, py, 1, 1)
      elevation.append(data[0][0])
      # data = band.ReadAsArray(xOrigin + 100 , yOrigin + 100, 1, 1)
      
      # elevation.append(data[0][0])
      # print(elevation)



      # for j in currCoords: 
      #    pixCoords = pixelCoords(transformer.itransform(currCoords[j]))

      #    heights = band.pixels.get(pixCoords[0], pixCoords[1])
      #    heights.append(round(height, 4))


      #    currFeature.geometry.coordinates = [
      #    currFeature.geometry.coordinates[0],
      #    currFeature.geometry.coordinates[currCoords.length - 1],
      #    ]
      #    currFeature.properties.profile = heights.toString()
      #    currFeature.properties.stepLength = options.stepLength


   return elevation
#%%
from shapely.geometry import MultiPoint
points = MultiPoint([(586214.1795694472, 6080202.035042746), (586236.0934224499, 6080181.825884934) , (586257.8189973006, 6080161.415198896), (586300.7968858992, 6080120.096076963), (586322.1894320849, 6080099.335885251)])

result = getHeights(points, LOCAL_VARS.DTM)
print(result)
# print(list(points.geoms))

