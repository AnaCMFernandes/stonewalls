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

layer = gpd.read_file('/mnt/c/Users/AFER/Documents/Projects/StoneWalls/Data/BES_STEN_JORDDIGER_SHAPE/Stonewalls_AEROE.shp')
layer = layer.to_crs(epsg=25832)

layer['length'] = layer.geometry.length
#%%


#%%
#Divides the line in the number of steps 
line = layer['geometry'][0]
sampleCount = 10.0
stepLength = line.length / (sampleCount - 1)

distances = np.arange(0, line.length, stepLength)
points = [line.interpolate(distance) for distance in distances]
multipoint = unary_union(points)

#%%
##function to insert points at defined equidistance along each LineString
def insertPoint(lineString, sampleCount):
    for index, row in lineString.iterrows():
        line = row['geometry']
        stepLength = line.length / (sampleCount - 1)
        distances = np.arange(0, line.length, stepLength)
        points = [line.interpolate(distance) for distance in distances]
        multipoint = unary_union(points)
        return multipoint

selection = layer[0:5]    
sample = insertPoint(selection, 10.0)
print(sample)


#%%
#Another way of doing it
 mp = shapely.geometry.MultiPoint()
 for i in  np.arange(0, line.length, stepLength):
     s = substring(line, i, i+stepLength)
     mp = mp.union(s.boundary)

#%%
#test - cuts line on specific distance

def cutLine(line, distance):
    if distance <= 0.0 or distance >= line.length:
        return [LineString(line)]
    coords = list(line.coords)
    for i, p in enumerate(coords):
        pd = line.project(Point(p))
        if pd == distance:
            return [
                LineString(coords[:i+1]),
                LineString(coords[i:])]
        if pd > distance:
            cp = line.interpolate(distance)
            return [
                LineString(coords[:i] + [(cp.x, cp.y)]),
                LineString([(cp.x, cp.y)] + coords[i:])
            ]


print([list(x.coords) for x in cutLine(line, 10.0)])

#%%
#Divides the line in the number of steps 
line = layer['geometry'][0]
sampleCount = 10.0
stepLength = line.length / (sampleCount - 1)

distances = np.arange(0, line.length, stepLength)
points = [line.interpolate(distance) for distance in distances]
multipoint = unary_union(points)

currDists = np.arange(0, line.length, stepLength)
bearing = [line.interpolate(currDist+0.1) for currDist in currDists]
multibearing = unary_union(bearing)

direction

    
#%%

length = layer['length']

x = []
y = []
z = []

dista = []

for currentdistance in range(0, length, 10):
    point = layer.interpolate(currentdistance)
    xp,yp = point.x, point.y
    x.append(xp)
    y.append(yp)
    dista.append(currentdistance)



# %%