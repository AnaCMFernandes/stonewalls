#%%
from osgeo import gdal, ogr
import os
import math
import numpy as np
import geopandas as gpd
from osgeo import gdal, ogr
import sys, math
import numpy as np
from shapely.geometry import Point, LineString, MultiPoint
import geopandas as gpd
import matplotlib.pyplot as plt
import LOCAL_VARS
import make_crossline as mkcross

from matplotlib import pyplot as plt

import time

start = time.time()

gdf = gpd.read_file(LOCAL_VARS.STONEWALLS)
gdf = gdf.to_crs(epsg=25832)

DTM = LOCAL_VARS.DTM
length = len(gdf.index)

object_ids = []
geoms = []
#%%
for index, row in gdf.iterrows():
    print(round(index / length * 100, 2))
    geometry = row["geometry"]
    linestring = mkcross.redistribute_vertices(geometry, 5)
    coords = list(linestring.coords)

    DigeID = row["DigeID"]

    for i, p in enumerate(coords):
        ## every point except for the last point will use the next point to create bearing
        if i < len(coords) - 1:
            vert = Point(p)
            next_vert = Point(coords[i + 1])
            bearing = mkcross.calculate_initial_compass_bearing(
                vert.coords[0], next_vert.coords[0]
            )
        ## the last point will use the previous point to create bearing and #TODO switch bearing 180
        if i == len(coords) - 1:
            vert = Point(p)
            previous_vert = Point(coords[i - 1])
            bearing = mkcross.calculate_initial_compass_bearing(
                previous_vert.coords[0], vert.coords[0]
            )

        cross = mkcross.make_crossline(vert, bearing, 15.0)
        object_ids.append("{0}-{1}".format(DigeID, i))
        geoms.append(cross)

        # print(cross)
        cross_points = mkcross.redistribute_vertices(cross, 0.4)
        # print(cross_points)
        heights = mkcross.get_heights(cross_points, DTM)

data = {"OBJECTID": object_ids, "geometry": geoms}
out_gdf = gpd.GeoDataFrame(data, crs="EPSG:25832")
out_gdf.to_file("cross_sections_all_data.geojson", driver="GeoJSON")

finish = time.time()

print("Time Taken is {0}s".format(finish - start))
# %%
