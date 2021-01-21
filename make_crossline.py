from osgeo import gdal, ogr
import math
import numpy as np
from shapely.geometry import Point, LineString, MultiPoint

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




