#%%

###creation of 3D multipoint instead of exporting line and geometry separately 

from osgeo import gdal, ogr
import sys, math
import numpy as np
from shapely.geometry import Point, LineString, MultiPoint
import geopandas as gpd
import matplotlib.pyplot as plt
import LOCAL_VARS
import make_crossline as mkcross
from matplotlib import pyplot as plt

import wall_score

import time



# Stonewalls
gdf = gpd.read_file(LOCAL_VARS.STONEWALLS)
gdf = gdf.to_crs(epsg=25832)

# Elevation data
DTM = LOCAL_VARS.DTM
UTM32 = "+proj=utm +zone=32 +ellps=GRS80 +units=m +no_defs"

## stonewall of interest
# in_gdf = gdf.loc[gdf['OBJECTID']==38305]
in_gdf = gdf[5:10]
out_gdf = mkcross.init(in_gdf)


















# %%
# line = gdf["geometry"][0]
# line = wall38305["geometry"]

# line = [i for i in wall38305.geometry][0]

# linestring = mkcross.redistribute_vertices(line, 10.0)
# coords = list(linestring.coords)

# object_ids = []
# geoms = []
# lr_scores = []

# start = time.time()

# for i, p in enumerate(coords):
#     ## every point except for the last point will use the next point to create bearing
#     if (i < len(coords) - 1):
#         vert = Point(p)
#         next_vert = Point(coords[i + 1])
#         bearing = mkcross.calculate_initial_compass_bearing(vert.coords[0], next_vert.coords[0])
#     ## the last point will use the previous point to create bearing and #TODO switch bearing 180
#     if (i == len(coords) - 1):
#         vert = Point(p)
#         previous_vert = Point(coords[i - 1])
#         bearing = mkcross.calculate_initial_compass_bearing(previous_vert.coords[0], vert.coords[0])
  
#     cross_section_line = mkcross.make_crossline(vert, bearing, 20.0)
#     cross_points = mkcross.redistribute_vertices(cross_section_line, 0.4)
#     cross_elevations = mkcross.get_heights3D(cross_points, DTM)
#     lr_score = wall_score.linear_regression_score3D(cross_elevations)

#     object_ids.append(i)
#     geoms.append(cross_elevations)
#     # elevations.append(cross_elevations)
#     lr_scores.append(lr_score)

#     # # TODO add back to geometry
    
# plt.show

# finish = time.time()

# print(finish - start)

# data = {'OBJECTID': object_ids, 'lr_score': lr_scores, 'geometry': geoms}
# out_gdf = gpd.GeoDataFrame(data, crs="EPSG:25832")