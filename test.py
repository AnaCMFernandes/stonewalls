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



