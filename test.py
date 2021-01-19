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


#%%
layer = gpd.read_file('/mnt/c/Users/EZRA/OneDrive - NIRAS/thesis/Data/Aeroe/Stonewalls')
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
def getHeights(input):

   def pixelCoords(arr):
      return [
         math.floor((arr[0] - xOrigin) / pixelWidth),
         math.floor((yOrigin - arr[1]) / pixelHeight),
      ]   

   DTM = '/mnt/c/Users/EZRA/OneDrive - NIRAS/thesis/Data/Aeroe/DTM_AEROE/DTM_AEROE.vrt'
   UTM32 = '+proj=utm +zone=32 +ellps=GRS80 +units=m +no_defs'
   # samples = input.data
   # options = input.options

   samples = input

   dataset = gdal.Open(DTM, gdal.GA_ReadOnly)
   band = dataset.GetRasterBand(1)

   transform = dataset.GetGeoTransform()
   pixelWidth = abs(transform[1])
   pixelHeight = abs(transform[5])
   xOrigin = transform[0]
   yOrigin = transform[3]

   transformer = Transformer.from_crs('EPSG:4326', UTM32)
   for i in samples: 
      currFeature = samples[i]
      currCoords = currFeature.geometry.coordinates
      heights = []
      import pdb; pdb.set_trace()
      
      for j in currCoords: 
         pixCoords = pixelCoords(transformer.itransform(currCoords[j]))

         heights = band.pixels.get(pixCoords[0], pixCoords[1])
         heights.append(round(height, 4))


         currFeature.geometry.coordinates = [
         currFeature.geometry.coordinates[0],
         currFeature.geometry.coordinates[currCoords.length - 1],
         ]
         currFeature.properties.profile = heights.toString()
         currFeature.properties.stepLength = options.stepLength


   return samples
result = getHeights(sections)
#%%
