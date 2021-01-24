from osgeo import gdal, ogr
import math
import numpy as np
from shapely.geometry import Point, LineString, MultiPoint

def calculate_initial_compass_bearing(pointA, pointB):
    startx,starty,endx,endy=pointA[0],pointA[1],pointB[0],pointB[1]
    angle=math.atan2(endx-startx, endy-starty)
    if angle>=0:
        return math.degrees(angle)
    else:
        return math.degrees((angle+2*math.pi))

def get_point270(pt, bearing, dist):
    angle = bearing + 180
    bearing = math.radians(angle)
    x = pt.x + dist * math.cos(bearing)
    y = pt.y + dist * math.sin(bearing)
    return Point(x, y)
## get the second end point of a tick
def get_point90(pt, bearing, dist):
    bearing = math.radians(bearing)
    x = pt.x + dist * math.cos(bearing)
    y = pt.y + dist * math.sin(bearing)
    return Point(x, y)

def make_crossline(pt, bearing, dist):
   left = get_point270(pt, bearing, (dist/2))
   right = get_point90(pt, bearing, (dist/2))
   return LineString([left, right])

#TODO add center point


