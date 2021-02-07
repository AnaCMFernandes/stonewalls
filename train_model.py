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


sub_gdf = gdf[
    :200]

ids = []
geometries = []
types = []

for _, row in sub_gdf.iterrows():

   obj_id = row['OBJECTID']
   geometry = row['geometry']

   walltype = wall_score.wall_tests(geometry)
   wall_score.only_plot(geometry, walltype)


  

# %%
