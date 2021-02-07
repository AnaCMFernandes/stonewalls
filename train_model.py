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


gdf = gpd.read_file('data/3D_cross_sections.geojson')

##%
# %%
# sbst_gdf = gdf[:500]

# for _,row in sbst_gdf.iterrows():
#    elevs = [p.z for p in row['geometry']]
#    average = sum(elevs) / len(elevs)
#    nrml_elevs = [(p - average) for p in elevs]

#    x = np.arange(len(nrml_elevs))
#    y = np.array(nrml_elevs)

#    peaks = signal.find_peaks(y, height=0.2)
#    print('---peaks----')
#    print(peaks)

#    plt.figure()
#    plt.scatter(x,y)
#    plt.yticks(np.arange(-0.6,.6, step=0.1))
   plt.show()

# scipy.signal.find_peaks(x, height=None, threshold=None, distance=None, prominence=None, width=None, wlen=None, rel_height=0.5, plateau_size=None)



# %%
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


gdf = gpd.read_file('data/3D_cross_sections.geojson')
#%%
from shapely import affinity
import scipy
from sklearn import linear_model as LinearRegression
from sklearn.utils.extmath import safe_sparse_dot

sub_gdf = gdf[
    :200]


def linear_regression_score3D(multipoint):

   elevs = [p.z for p in multipoint]

   x = np.arange(len(elevs))
   y = np.array(elevs)

   xr = x.reshape(-1, 1)

   LR = LinearRegression.LinearRegression()
   LR.fit(xr, y)

   score = LR.score(xr, y)

   prediction = LR.predict(xr)

   # return safe_sparse_dot(xr, LR.coef_.T, dense_output=True) + LR.intercept_
   return (LR.coef_, LR.intercept_)

### uses math 
def pnt_from_rtn_arnd_orgn(point, origin, angle):

   p = {'x': point[0], 'y':point[1]}
   o = {'x': origin[0], 'y':origin[1]}

   # if (p['x'] == o['x'] & p['y'] == o['y']): return point

   cos = math.cos(angle)
   sin = math.sin(angle)

   dx = p['x'] - o['x']
   dy = p['y'] - o['y']

   nx = (cos * dx) + (sin * dy) + o['x']
   ny = (cos * dy) - (sin * dx) + o['y']

   return [nx, ny]


def rise_run_to_angle(rise, run):
   return math.degrees(math.atan(rise/run))

for _, row in sub_gdf.iterrows():
   geometry = row['geometry']
   elevs = [x.z for x in geometry]
   steps = list(np.arange(0, 20.01, step=0.4))
   profile_coords = []
   for i in range(len(elevs)):
      pair = (steps[i], elevs[i])
      profile_coords.append(pair)
   # scipy.signal.find_peaks(x, height=None, threshold=None, distance=None, prominence=None, width=None, wlen=None, rel_height=0.5, plateau_size=None)
   peaks, _ = scipy.signal.find_peaks(elevs, prominence=0.17)

   if len(peaks) != 1: wall_score.plot(geometry)

   #### calculate rotations and transformation
   formula = linear_regression_score3D(geometry)
   
   rise = formula[0][0]
   step = 0.4

   rotation = rise_run_to_angle(rise, step)
  
   new_geom = affinity.rotate(MultiPoint(profile_coords), -rotation, origin = origin)

   new_x = np.array([p.x for p in new_geom])
   new_y = np.array([p.y for p in new_geom])
  
   if len(peaks) != 1: 
      print(len(peaks))
      plt.figure()
      plt.scatter(new_x, new_y)

      LR1 = LinearRegression.LinearRegression()

      new_xr = new_x.reshape(-1, 1)

      LR1.fit(new_xr, new_y)
      prediction = LR1.predict(new_xr)
      plt.plot(new_xr, prediction)
      plt.show()
      
      

# %%

# from osgeo import gdal, ogr
# import os
# import math
# import numpy as np
# import geopandas as gpd
# from osgeo import gdal, ogr
# import sys, math
# import numpy as np
# from shapely.geometry import Point, LineString, MultiPoint
# import geopandas as gpd
# import matplotlib.pyplot as plt
# import LOCAL_VARS
# import make_crossline as mkcross
# import wall_score
# from scipy import signal

# import scipy
# from sklearn import linear_model as LinearRegression
# from sklearn.utils.extmath import safe_sparse_dot

# from shapely import affinity


# x = np.array([0,1, 2, 3, 4, 5])
# y = np.array([0,1, 2, 3, 4, 5])
# plt.figure()
# plt.scatter(x, y)

# coords = []
# for i in range(len(y)):
#    pair = (x[i], y[i])
#    coords.append(pair)

# xr = x.reshape(-1, 1)

# LR = LinearRegression.LinearRegression()
# LR.fit(xr, y)

#    #### calculate rotations and transformation
# formula = (LR.coef_, LR.intercept_)
 
# print(formula)
# origin = (0, formula[1])
# point2 = (step, formula[1] + (step * formula[0][0]))
# rotation = angle(origin, point2)

# print(origin, point2)

# # new_elevs = [pnt_from_rtn_arnd_orgn(x, origin, rotation) for x in coords]
# my_geom = MultiPoint(coords)
# rotation = math.degrees(rotation)
# rotated_geom = affinity.rotate(my_geom, -rotation, origin=origin)
# print('rotation', rotation)
# print(my_geom)
# print(rotated_geom)
# new_x = [p.x for p in rotated_geom]
# new_y = [p.y for p in rotated_geom]
# plt.figure()
# plt.scatter(new_x, new_y)
# LR1 = LinearRegression.LinearRegression()
# new_xr = x.reshape(-1, 1)
# LR1.fit(new_xr, new_y)
# prediction = LR1.predict(new_xr)
# plt.plot(prediction, y)
# plt.show()
# # %%
# coords
# rotated = rotate(my_geom, 90)
# new_x = [p.x for p in rotated]
# new_y = [p.y for p in rotated]
# plt.figure()
# plt.scatter(new_x, new_y)
# plt.show()
# # %%

if test1 promincence 1.7 catch big stonewalls 1

if test2 promincence 0.5 catch small stonewalls small

if test3 rotate and find peaks caetch jorddige

else  not