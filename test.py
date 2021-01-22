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

import crossSection

# 

# for coord in tmp.coords:
#    print(coord)

# tmp = MultiPoint([(10,22), (25, 25), (30, 30), (44, 55)])

# for coord in tmp:
#    print(coord.coords[0])
# %%
import math
import time
def getPoint90(pt, bearing, dist):
    angle = bearing + 180
    bearing = math.radians(angle)
    x = pt.x + dist * math.cos(bearing)
    y = pt.y + dist * math.sin(bearing)
    return Point(x, y)
## get the second end point of a tick
def getPoint270(pt, bearing, dist):
    bearing = math.radians(bearing)
    x = pt.x + dist * math.cos(bearing)
    y = pt.y + dist * math.sin(bearing)
    return Point(x, y)

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

point = Point(5,5)

left = getPoint90(point, 0, 5)
right = getPoint270(point, 0, 5)

line = LineString([left, right])

cross = redistribute_vertices(line, 1)

from getHeights import getHeights

elevs = getHeights(cross, LOCAL_VARS.DTM)
# %%
a = (1,2)
b = (3,4)

def calculate_initial_compass_bearing(pointA, pointB):
    """
    Calculates the bearing between two points.
    The formulae used is the following:
        θ = atan2(sin(Δlong).cos(lat2),
                  cos(lat1).sin(lat2) − sin(lat1).cos(lat2).cos(Δlong))
    :Parameters:
      - `pointA: The tuple representing the latitude/longitude for the
        first point. Latitude and longitude must be in decimal degrees
      - `pointB: The tuple representing the latitude/longitude for the
        second point. Latitude and longitude must be in decimal degrees
    :Returns:
      The bearing in degrees
    :Returns Type:
      float
    """
    if (type(pointA) != tuple) or (type(pointB) != tuple):
        raise TypeError("Only tuples are supported as arguments")

    lat1 = math.radians(pointA[0])
    lat2 = math.radians(pointB[0])

    diffLong = math.radians(pointB[1] - pointA[1])

    x = math.sin(diffLong) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
            * math.cos(lat2) * math.cos(diffLong))

    initial_bearing = math.atan2(x, y)

    # Now we have the initial bearing but math.atan2 return values
    # from -180° to + 180° which is not what we want for a compass bearing
    # The solution is to normalize the initial bearing as shown below
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing

bearing = calculate_initial_compass_bearing(a, b)

#%%
def calculate_initial_compass_bearing2(pointA, pointB):
    startx,starty,endx,endy=pointA[0],pointA[1],pointB[0],pointB[1]
    angle=math.atan2(endy-starty, endx-startx)
    if angle>=0:
        return math.degrees(angle)
    else:
        return math.degrees((angle+2*math.pi))

bearing2 = calculate_initial_compass_bearing2(a, b)



# %%
