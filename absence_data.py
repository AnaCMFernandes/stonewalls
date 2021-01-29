#%%
import os
import math
import numpy as np
import sys, math
import LOCAL_VARS
import geopandas as gpd
from shapely.geometry import Polygon, Point, LineString
from shapely.affinity import translate
from osgeo import gdal, ogr
import matplotlib.pyplot as plt
import make_crossline as mkcross
import wall_score

import time

stonewalls = gpd.read_file(LOCAL_VARS.STONEWALLS)


# %%
f = stonewalls[['OBJECTID', 'DigeID', 'geometry']].copy()

f['geometry'] = f['geometry'].translate(xoff=10.0, yoff=10.0)

absence_walls = gpd.GeoDataFrame(f, crs="EPSG:25832")

absence_walls.to_file("data/duplicated_stonewalls.geojson", driver="GeoJSON")

# %%

dups = gpd.read_file('data/duplicated_stonewalls.geojson')

stone3d = gpd.read_file('3D_cross_sections.geojson')

#%%
start = time.time()

gdf2 = absence_walls
gdf2 = absence_walls.to_crs(epsg=25832)

DTM = LOCAL_VARS.DTM
length = len(gdf2.index)

object_ids = []
elevations = []
geoms = []
lr_scores = []

for index, row in gdf2.iterrows():
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

        cross_section_line = mkcross.make_crossline(vert, bearing, 20.0)
        cross_points = mkcross.redistribute_vertices(cross_section_line, 0.4)
        cross_elevations = mkcross.get_heights3D(cross_points, DTM)
        lr_score = wall_score.linear_regression_score3D(cross_elevations)

        object_ids.append("{0}-{1}".format(DigeID, i))
        geoms.append(cross_elevations)
        lr_scores.append(lr_score)
            

data = {'OBJECTID': object_ids, 'elevations': cross_elevations, 'lr_score': lr_scores, 'geometry': geoms}

#%%

out_gdf2 = gpd.GeoDataFrame(data, crs="EPSG:25832")

out_gdf2.to_file("3D_ABSENCE_cross_sections.geojson", driver="GeoJSON")

finish = time.time()

print("Time Taken is {0}s".format(finish - start))
# %%
