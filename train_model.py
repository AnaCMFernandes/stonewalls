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
from scipy import signal
from shapely import affinity
import scipy
from sklearn import linear_model as LinearRegression
from sklearn.utils.extmath import safe_sparse_dot


gdf = gpd.read_file('data/3D_cross_sections.geojson')

#%%
def earthwall_test(geom):
   ##elevations
   z = [p.z for p in geom]
   ## steps in x direction
   x = list(np.arange(0, 20.01, step=0.4))

   ## make x, z coords
   coords = []
   for i in range(len(z)):
      coord = (x[i], z[i])
      coords.append(coord)

   wall_score.only_plot(MultiPoint(coords), 'original', 'green')

   #### calculate rotations and transformation
   rise, intercept = wall_score.linear_regression_score3D(geom)

   origin = (0,intercept)

   run = 0.4

   rotation = wall_score.rise_run_to_angle(rise, run)

   new_geom = affinity.rotate(MultiPoint(coords), -rotation, origin = origin)

   wall_score.only_plot(new_geom, 'rotate', 'red')
   # new_x = np.array([p.x for p in new_geom])
   # new_y = np.array([p.y for p in new_geom])

   return True

sub_gdf = gdf[
    :200]

ids = []
geometries = []
types = []

for _, row in sub_gdf.iterrows():

   obj_id = row['OBJECTID']
   geometry = row['geometry']
   earthwall_test(geometry)
  

# %%
