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

## get the second end point of a tick
def offset_point(pt, bearing, angle, dist):
    bearing = math.radians(bearing + angle)
    x = pt.x + dist * math.sin(bearing)
    y = pt.y + dist * math.cos(bearing)
    return Point(x, y)

def make_crossline(pt, bearing, dist):
   left = offset_point(pt, bearing, 270, (dist/2))
   right = offset_point(pt, bearing, 90, (dist/2))
   return LineString([left, right])




