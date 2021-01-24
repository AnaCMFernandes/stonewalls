#%%
from osgeo import gdal, ogr
import sys, math
import numpy as np
from shapely.geometry import Point, LineString, MultiPoint
import geopandas as gpd
import matplotlib.pyplot as plt
import LOCAL_VARS
from getHeights import getHeights
from crossSection import redistribute_vertices
import make_crossline as mkcross

from matplotlib import pyplot as plt

import time

#%%
# Stonewalls
gdf = gpd.read_file(LOCAL_VARS.STONEWALLS)
gdf = gdf.to_crs(epsg=25832)

# Elevation data
DTM = LOCAL_VARS.DTM
UTM32 = "+proj=utm +zone=32 +ellps=GRS80 +units=m +no_defs"

## stonewall of interest
wall38305 = gdf.loc[gdf['OBJECTID']==38305]

# line = gdf["geometry"][0]
# line = wall38305["geometry"]

line = [i for i in wall38305.geometry][0]

linestring = redistribute_vertices(line, 10.0)
coords = list(linestring.coords)

object_ids = []
geoms = []

for i, p in enumerate(coords):
    ## every point except for the last point will use the next point to create bearing
    if (i < len(coords) - 1):
        vert = Point(p)
        next_vert = Point(coords[i + 1])
        bearing = mkcross.calculate_initial_compass_bearing(vert.coords[0], next_vert.coords[0])
    ## the last point will use the previous point to create bearing and #TODO switch bearing 180
    if (i == len(coords) - 1):
        vert = Point(p)
        previous_vert = Point(coords[i - 1])
        bearing = mkcross.calculate_initial_compass_bearing(previous_vert.coords[0], vert.coords[0])


    ## rejected idea that bearing will be made from point created 0.5m from current point on line
    # pd = linestring.project(Point(p))
    # dist = pd + 0.5
    # bearing_point = linestring.interpolate(dist)
  
    cross = mkcross.make_crossline(vert, bearing, 10.0)

    object_ids.append(i)
    geoms.append(cross)

    # print(cross)
    cross_points = redistribute_vertices(cross, 0.4)
    # print(cross_points)
    heights = getHeights(cross_points, DTM)


    # # TODO add back to geometry
    
    plt.figure()
    plt.scatter(x=np.arange(len(heights)), y=heights)
plt.show
data = {'OBJECTID': object_ids, 'geometry': geoms}
out_gdf = gpd.GeoDataFrame(data, crs="EPSG:25832")
out_gdf.to_file("cross_sections.geojson", driver='GeoJSON')

# %%
elev = [59.123,59.1248,59.1069,59.115,59.1393,59.1641,59.1859,59.1773,59.2114,59.3088,59.3231,59.4345,59.5144,59.6234,59.6362,59.5922,59.5899,59.5941,59.6432,59.6467,59.6219,59.5434,59.5554,59.5973,59.5965]

plt.scatter(x=np.arange(len(elev)), y=elev)
plt.show()
# %%
