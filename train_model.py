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
import scipy
from sklearn import linear_model as LinearRegression
from sklearn.utils.extmath import safe_sparse_dot

sub_gdf = gdf[
    :10]


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


def angle(point1, point2):
   p1 = {'x': point1[0], 'y': point1[1]}
   p2 = {'x': point2[0],'y': point2[1]}
   dx = p2['x'] - p1['x']
   dy = p2['y'] - p1['y']

   return math.atan2(dy, dx)

for _, row in sub_gdf.iterrows():
   geometry = row['geometry']
   elevs = [x.z for x in geometry]
   steps = list(np.arange(0, 20.01, step=0.4))
   profile_coords = []
   for i in range(len(elevs)):
      pair = (steps[i], elevs[i])
      profile_coords.append(pair)
   # scipy.signal.find_peaks(x, height=None, threshold=None, distance=None, prominence=None, width=None, wlen=None, rel_height=0.5, plateau_size=None)
   # peaks, _ = scipy.signal.find_peaks(elevs, prominence=0.17)

   # print(peaks)    
   # if len(peaks) != 1: wall_score.plot(geometry)
   wall_score.plot(geometry)

   #### calculate rotations and transformation
   formula = linear_regression_score3D(geometry)
   step = 0.4
   origin = (0, formula[1])
   point2 = (step, formula[1] + (step * formula[0][0]))
   rotation = angle(origin, point2)

   new_elevs = [pnt_from_rtn_arnd_orgn(x, origin, rotation) for x in profile_coords]
  
   new_x = [p[0] for p in new_elevs]
   new_y = [p[1] for p in new_elevs]
   plt.figure()
   plt.scatter(new_x, new_y)
   plt.show()

   
# %%
# def radian_angle(vector_1, vector_2):
#    unit_vector_1 = vector_1 / np.linalg.norm(vector_1)
#    unit_vector_2 = vector_2 / np.linalg.norm(vector_2)
#    dot_product = np.dot(unit_vector_1, unit_vector_2)
#    angle = np.arccos(dot_product)
#    return angle

vector1 = (0, 1)
vector2 = (1, 0)

radian_angle(origin, point2)


# %%
