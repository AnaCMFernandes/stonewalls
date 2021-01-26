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
import wall_score

from matplotlib import pyplot as plt

import time

start = time.time()

gdf = gpd.read_file(LOCAL_VARS.STONEWALLS)
gdf = gdf.to_crs(epsg=25832)

DTM = LOCAL_VARS.DTM
length = len(gdf.index)

object_ids = []
elevations = []
geoms = []
lr_scores = []

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

        cross_section_line = mkcross.make_crossline(vert, bearing, 20.0)
        cross_points = mkcross.redistribute_vertices(cross_section_line, 0.4)
        cross_elevations = mkcross.get_heights(cross_points, DTM)
        lr_score = wall_score.linear_regression_score(cross_elevations)

        object_ids.append("{0}-{1}".format(DigeID, i))
        geoms.append(cross_section_line)
        elevations.append(cross_elevations)
        lr_scores.append(lr_score)
      

data = {'OBJECTID': object_ids, 'elevations': elevations, 'lr_score': lr_scores, 'geometry': geoms}
out_gdf = gpd.GeoDataFrame(data, crs="EPSG:25832")
out_gdf.to_file("./data/aeroe_cross_sections.geojson", driver="GeoJSON")

finish = time.time()

print("Time Taken is {0}s".format(finish - start))

#%%
### 3D
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
import wall_score

from matplotlib import pyplot as plt

import time

start = time.time()

gdf = gpd.read_file(LOCAL_VARS.STONEWALLS)
gdf = gdf.to_crs(epsg=25832)

DTM = LOCAL_VARS.DTM
length = len(gdf.index)

object_ids = []
elevations = []
geoms = []
lr_scores = []

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

        cross_section_line = mkcross.make_crossline(vert, bearing, 20.0)
        cross_points = mkcross.redistribute_vertices(cross_section_line, 0.4)
        cross_elevations = mkcross.get_heights3D(cross_points, DTM)
        lr_score = wall_score.linear_regression_score3D(cross_elevations)

        object_ids.append("{0}-{1}".format(DigeID, i))
        geoms.append(cross_elevations)
        lr_scores.append(lr_score)
            

data = {'OBJECTID': object_ids, 'elevations': elevations, 'lr_score': lr_scores, 'geometry': geoms}
out_gdf = gpd.GeoDataFrame(data, crs="EPSG:25832")
out_gdf.to_file("3D_cross_sections.geojson", driver="GeoJSON")

finish = time.time()

print("Time Taken is {0}s".format(finish - start))






















# %%

#### trying to get elevations to import / export properly into json/geojson


# out_gdf

# strings = []

# for i in out_gdf['elevations']:
#     strings.append(str(i))

# strings = [str(x) for x in out_gdf['elevations']]

# in_gdf3 = gpd.read_file('cross_sections_str.shp', crs="EPSG:25832")

# def df_to_geojson(df, properties):
#     geojson = {'type':'FeatureCollection', 'features':[]}
#     for _, row in df.iterrows():
#         feature = {'type':'Feature',
#                    'properties':{},
#                    'geometry':{'type':'LineString',
#                                'coordinates':[]}}
#         feature['geometry']['coordinates'] = [row['geometry'].coords[0],row['geometry'].coords[1]]
#         for prop in properties:
#             feature['properties'][prop] = row[prop]
#         geojson['features'].append(feature)
#     return geojson


# cols = ['OBJECTID', 'lr_score', 'elevations']
# geojson = df_to_geojson(out_gdf, cols)


# output_filename = 'dataset.js'
# with open(output_filename, 'wb') as output_file:
#     json.dump(geojson, output_file, indent=2) 

# geojson.to_file('gjsondataset.geojson', driver='GeoJSON')

# import json
# with open('data.json', 'w') as f:
#     json.dump(str(geojson), f)
# %%
