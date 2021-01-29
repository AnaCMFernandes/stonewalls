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


gdf = gpd.read_file('data/3D_cross_sections.geojson')

##%
# %%
sbst_gdf = gdf[:500]

for _,row in sbst_gdf.iterrows():
   elevs = [p.z for p in row['geometry']]
   average = sum(elevs) / len(elevs)
   nrml_elevs = [(p - average) for p in elevs]

   x = np.arange(len(nrml_elevs))
   y = np.array(nrml_elevs)

   plt.figure()
   plt.scatter(x,y)
   plt.yticks(np.arange(-0.6,.6, step=0.1))
   plt.show()



# %%
