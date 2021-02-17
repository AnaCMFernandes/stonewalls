#%%
from osgeo import gdal, ogr
import os
import numpy as np
import geopandas as gpd
import shapely
from shapely.geometry import Point, LineString, MultiPoint
from shapely.ops import unary_union, substring
import matplotlib.pyplot as plt
import sys, math
from LOCAL_VARS import DTM, STONEWALLS
import make_crossline as mkcross

import time


#%%
# Elevation data
theDTM = DTM
UTM32 = '+proj=utm +zone=32 +ellps=GRS80 +units=m +no_defs'

# %%
# Stonewalls

gdf = gpd.read_file(STONEWALLS)
gdf = gdf.to_crs(epsg=25832)

#layer['length'] = layer.geometry.length


#%%
#Divides the line in the number of steps 
line = layer['geometry'][0]
sampleCount = 10.0
stepLength = line.length / (sampleCount - 1)

distances = np.arange(0, line.length, stepLength)
points = [line.interpolate(distance) for distance in distances]
multipoint = unary_union(points)

#%%
##function to insert points at defined equidistance along each LineString
def insertPoint(lineString, sampleCount):
    for index, row in lineString.iterrows():
        line = row['geometry']
        stepLength = line.length / (sampleCount - 1)
        distances = np.arange(0, line.length, stepLength)
        points = [line.interpolate(distance) for distance in distances]
        multipoint = unary_union(points)
        return multipoint

selection = layer[0:5]    
sample = insertPoint(selection, 10.0)
print(sample)


#%%
#Another way of doing it
mp = shapely.geometry.MultiPoint()
for i in  np.arange(0, line.length, stepLength):
    s = substring(line, i, i+stepLength)
    mp = mp.union(s.boundary)


#%%
#test - cuts line on specific distance

def cutLine(line, distance):
    if distance <= 0.0 or distance >= line.length:
        return [LineString(line)]
    coords = list(line.coords)
    for i, p in enumerate(coords):
        pd = line.project(Point(p))
        if pd == distance:
            return [
                LineString(coords[:i+1]),
                LineString(coords[i:])]
        if pd > distance:
            cp = line.interpolate(distance)
            return [
                LineString(coords[:i] + [(cp.x, cp.y)]),
                LineString([(cp.x, cp.y)] + coords[i:])
            ]


print([list(x.coords) for x in cutLine(line, 10.0)])

#%%
#Divides the line in the number of steps 
line = layer['geometry'][0]
sampleCount = 10.0
stepLength = line.length / (sampleCount - 1)

distances = np.arange(0, line.length, stepLength)
points = [line.interpolate(distance) for distance in distances]
multipoint = unary_union(points)

currDists = np.arange(0, line.length, stepLength)
bearing = [line.interpolate(currDist+0.1) for currDist in currDists]
multibearing = unary_union(bearing)

#%%
selection = layer['geometry'][0:5]  
sampleCount = 10.0
stepLength = selection.length / (sampleCount - 1)

x = []
y = []
z = []

dista = []

for currentdistance in np.arange(0, selection.length, stepLength):
    point = selection.interpolate(currentdistance)
    xp,yp = point.x, point.y
    x.append(xp)
    y.append(yp)
    dista.append(currentdistance)



# %%

def redistribute_vertices(geom, distance):
    if geom.geom_type == 'LineString':
        num_vert = int(round(geom.length / distance))
        if num_vert == 0:
            num_vert = 1
        return LineString(
            [geom.interpolate(float(n) / num_vert, normalized=True)
             for n in range(num_vert + 1)])
    elif geom.geom_type == 'MultiLineString':
        parts = [redistribute_vertices(part, distance)
                 for part in geom]
        return type(geom)([p for p in parts if not p.is_empty])
    else:
        raise ValueError('unhandled geometry %s', (geom.geom_type,))


# %%

gdf_line = layer[0:5]  

gdf_line_interpolate = gdf_line.copy()
gdf_line_interpolate.geometry = gdf_line.geometry.apply(redistribute_vertices,distance=10)
gdf_line_interpolate['nverts'] = gdf_line_interpolate.geometry.apply(lambda x: len(x.coords))

gdf_line_interpolate['bearpoint'] = gdf_line_interpolate.geometry.apply(lambda x: len(x.coords))

# %%
line = layer['geometry'][0]
linestring = redistribute_vertices(line, 10.0)
#%%
x = []
y = []
bear_points = []

coords = list(linestring.coords)
for i, p in enumerate(coords):
    pd = linestring.project(Point(p))
    #print(pd)
    dist = pd+0.5
    bearing_point = linestring.interpolate(dist)
    print(bearing_point)
    xp,yp = bearing_point.x, bearing_point.y
    x.append(xp)
    y.append(yp)
    bear_points.append(dist)

bearing_points = unary_union(bearing_point)

#%%
#line1 = linestring.interpolate([line.coords[0],(point.x, point.y)])+0.5)

def pairs(lst):
    for i in range(1, len(lst)):
        yield lst[i-1], lst[i]

line = layer['geometry'][0]

for pair in pairs(list(line.coords)):
    if LineString([pair[0],pair[1]]).contains(point):
        print(LineString([pair[0],pair[1]]))


#%%
#bearing = [linestring.interpolate(vert[0]+0.5) for vert in linestring.coords]
#multibearing = unary_union(bearing)
x = []
y = []
dista = []

for vert in linestring.coords:
    point = linestring.interpolate(vert[0]+0.5)
    xp,yp = point.x, point.y
    x.append(xp)
    y.append(yp)
    dista.append(bearing)
    
# %%
line = layer['geometry'][0]
sampleCount = 10.0
stepLength = line.length / (sampleCount - 1)

currDists = np.arange(0, line.length, stepLength)
bearing = [line.interpolate(currDist+0.1) for currDist in currDists]
multibearing = unary_union(bearing)
# %%
def calculate_initial_compass_bearing(pointA, pointB):
    startx,starty,endx,endy=pointA[0],pointA[1],pointB[0],pointB[1]
    angle=math.atan2(endy-starty, endx-startx)
    if angle>=0:
        return math.degrees(angle)
    else:
        return math.degrees((angle+2*math.pi))

def get_point270(pt, bearing, dist):
    angle = bearing + 180
    bearing = math.radians(angle)
    x = pt.x + dist * math.cos(bearing)
    y = pt.y + dist * math.sin(bearing)
    return Point(x, y)
## get the second end point of a tick
def get_point90(pt, bearing, dist):
    bearing = math.radians(bearing)
    x = pt.x + dist * math.cos(bearing)
    y = pt.y + dist * math.sin(bearing)
    return Point(x, y)

def make_crossline(pt, bearing, dist):
   left = get_point270(pt, bearing, (dist/2))
   right = get_point90(pt, bearing, (dist/2))
   return LineString([left, right])

#%%
line = layer['geometry'][0]
linestring = redistribute_vertices(line, 10.0)
coords = list(linestring.coords)

for i, p in enumerate(coords):
    vert = Point(p)
    pd = linestring.project(Point(p))
    dist = pd+0.5
    bearing_point = linestring.interpolate(dist)
    bearing = calculate_initial_compass_bearing(vert.coords[0], bearing_point.coords[0])
    #print(bearing)
    cross = make_crossline(verts, bearing, 10.0)
    #print(cross)
    cross_points = redistribute_vertices(cross, 0.5)
    # print(cross_points)
    heights = getHeights(cross_points, theDTM)
    print(heights)

#pointAlong = bearing_point.apply(lambda p: p.x)
#pointAlat = bearing_point.apply(lambda p: p.y)

# %%
calculate_initial_compass_bearing(line.coords[0], line.coords[1])
# %%
# %%
wall38305 = layer.loc[layer['OBJECTID']==38305]
line = wall38305["geometry"][0]
# %%
line1 = layer['geometry'][0]
# %%
elev = [26.7561,26.7687,26.7331,26.7933,26.7933,26.8555,26.8673,26.8988,26.9217,27.0133,27.0859,27.1682,27.368,27.4514,27.5056,27.4988,27.278,27.0249,26.7724,26.624,26.4655,26.3781,26.3067,26.2866,26.2436]
 
plt.scatter(x=np.arange(len(elev)), y=elev)
plt.show()
# %%
## stonewall of interest
wall38305 = gdf.loc[gdf["OBJECTID"] == 38305]

# line = gdf["geometry"][0]
# line = wall38305["geometry"]

line = [i for i in wall38305.geometry][0]


linestring = redistribute_vertices(line, 10.0)
coords = list(linestring.coords)

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
    print(bearing)


    ## rejected idea that bearing will be made from point created 0.5m from current point on line
    # pd = linestring.project(Point(p))
    # dist = pd + 0.5
    # bearing_point = linestring.interpolate(dist)

    cross = mkcross.make_crossline(vert, bearing, 10.0)

    
    # print(cross)
    cross_points = redistribute_vertices(cross, 0.4)
    # print(cross_points)
    plt.figure()
    plt.scatter(x=cross_points, y=cross_points)

    heights = getHeights(cross_points, DTM)

    # # TODO add back to geometry

    #plt.figure()
    #plt.scatter(x=[i for i in range(len(heights))], y=heights)
plt.show

#%%
gdf.columns
##%
# %%
wall38305 = gdf.loc[gdf["OBJECTID"] == 38305]

# line = gdf["geometry"][0]
line = wall38305["geometry"]
print(line)
line = gdf["geometry"][0]
print(line)
linestring = redistribute_vertices(line, 10.0)

mkcross.calculate_initial_compass_bearing((0,1), (0,2))
# %%
def calculate_initial_compass_bearing(pointA, pointB):
    startx,starty,endx,endy=pointA[0],pointA[1],pointB[0],pointB[1]
    angle=math.atan2(endx-startx, endy-starty)
    if angle>=0:
        return math.degrees(angle)
    else:
        return math.degrees((angle+2*math.pi))
 
## get the second end point of a tick
def offset_point(pt, bearing, angle, dist):
    bearing = math.radians(bearing + angle)
    x = pt.x + dist * math.sin(bearing)
    y = pt.y + dist * math.cos(bearing)
    return Point(x, y)
 
def make_crossline(pt, bearing, dist):
   left = offset_point(pt, bearing, 270, (dist/2))
   right = offset_point(pt, bearing, 90, (dist/2))
   return LineString([left, right])

## stonewall of interest
wall38305 = gdf.loc[gdf["OBJECTID"] == 38305]

# line = gdf["geometry"][0]
# line = wall38305["geometry"]

line = [i for i in wall38305.geometry][0]


linestring = redistribute_vertices(line, 10.0)
coords = list(linestring.coords)  

object_ids = []
geoms = [] 


for i, p in enumerate(coords):
    ## every point except for the last point will use the next point to create bearing
    if i < len(coords) - 1:
        vert = Point(p)
        next_vert = Point(coords[i + 1])
        bearing = calculate_initial_compass_bearing(
            vert.coords[0], next_vert.coords[0]
        )
    ## the last point will use the previous point to create bearing and #TODO switch bearing 180
    if i == len(coords) - 1:
        vert = Point(p)
        previous_vert = Point(coords[i - 1])
        bearing = calculate_initial_compass_bearing(
            previous_vert.coords[0], vert.coords[0]
        )
    #print(bearing)


    ## rejected idea that bearing will be made from point created 0.5m from current point on line
    # pd = linestring.project(Point(p))
    # dist = pd + 0.5
    # bearing_point = linestring.interpolate(dist)

    cross = make_crossline(vert, bearing, 10.0)

    object_ids.append(i)
    geoms.append(cross)
    # print(cross)
    cross_points = redistribute_vertices(cross, 0.4)
    # print(cross_points)
    #plt.figure()
    #plt.scatter(x=cross_points, y=cross_points)

    heights = getHeights(cross_points, DTM)
    plt.figure()
    plt.scatter(x=cross_points, y=cross_points)
    # # TODO add back to geometry

    #plt.figure()
    #plt.scatter(x=[i for i in range(len(heights))], y=heights)
plt.show

data = {'OBJECTID': object_ids, 'geometry': geoms}
out_gdf = gpd.GeoDataFrame(data, crs="EPSG:25832")
out_gdf.to_file("cross_sections_test.geojson", driver='GeoJSON')
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
from shapely import affinity
import scipy
from sklearn import linear_model as LinearRegression
from sklearn.utils.extmath import safe_sparse_dot

gdf = gpd.read_file('data/3D_cross_sections.geojson')

#%%


sub_gdf = gdf[
    100:200]

ids = []
geometries = []
types = []
# count = 0
for _, row in gdf.iterrows():

    obj_id = row['OBJECTID']
    geometry = row['geometry']

    result = wall_tests(geometry)

    ids.append(obj_id)
    geometries.append(geometry)
    types.append(result)

    # print(result)
    # if result == 'large_stonewall':
    #     just_plot(geometry, color='green')
    # if result == 'small_stonewall':
    #     just_plot(geometry, color='yellow')
    # if result == 'no_wall':
    #     just_plot(geometry, color='blue')
    # if result == 'earthwall':
    #     just_plot(geometry, color='orange')





# %%
data = {'OBJECTID': ids, 'type': types, 'geometry': geometries}
out_gdf = gpd.GeoDataFrame(data, crs="EPSG:25832")
out_gdf.to_file("complete_classified_cross_sections.geojson", driver="GeoJSON")

#%%
from osgeo import gdal, ogr
import os
import geopandas as gpd
import sys, math
import numpy as np
from shapely.geometry import Point, LineString, MultiPoint
import geopandas as gpd
import matplotlib.pyplot as plt
from scipy import signal
from shapely import affinity
import scipy
from sklearn import linear_model as LinearRegression
from sklearn.utils.extmath import safe_sparse_dot
import sys; sys.path.append('..'); sys.path.append('../lib')
import lib.core
import lib.helpers


#%%
path = "../cross_sections_test14_50.geojson"
profiles = gpd.read_file(path)

sub_profiles = profiles[0:2]

def peaks_finder(geom):
    z = [p.z for p in geom]
    ### TODO change here for adjustment
    peaks, properties = signal.find_peaks(z, prominence=0.17, height=(None, None))
    return peaks, properties

def find_peak_score(geom):
    just_peaks, properties = peaks_finder(geom)
    if (len(just_peaks) > 0):
        #print(just_peaks)
        #print(properties)
        return (just_peaks, properties, '1')
    return ([], [], '0')



for _, row in sub_profiles.iterrows():   
    z = [p.z for p in row['geometry']]
    peak, properties, wall_score = find_peak_score(row['geometry'])
    ideal_mid = 25
    prominences = signal.peak_prominences(z, peak, wlen=3.1)
    print(prominences)
    print(z)
    if (len(peak) > 1):
        curr_closest = -1
        closest_value = 50
        for peak in peak:
            pks = [x.z for x in row['geometry'] if x > 0.5]
            if len(pks) > 0:
                print('I am a stonewall!')
                diff = abs(peak - ideal_mid)
                low_diff = diff.min()
                print("--> ", low_diff)
                if (low_diff <= closest_value):
                    closest_value = low_diff
                    print("closest ", closest_value)
                    curr_closest = peak
                    print("curr ", curr_closest)
            else: print("too low")
        peak = curr_closest
        print("peak is ", peak)
    elif (len(peak) == 0): peak = ideal_mid

    correction = ideal_mid - peak
    print("the correction is: ", correction)

# %%
path_file = "cross_sections_50_tests.geojson"
profile_corrected = gpd.read_file(path_file)
# %%
from lib.helpers import just_plot

for _, row in profile_corrected.iterrows():   
    z = [p.z for p in row['geometry']]
    if row['OBJECTID'] == "12559-31":
        just_plot(row['geometry'])
# %%
