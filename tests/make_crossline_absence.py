from osgeo import gdal, ogr
import math
import numpy as np
from shapely.geometry import Point, LineString, MultiPoint
import geopandas as gpd
import site
import sys

sys.path.insert(0,'/utils')
sys.path.insert(0,'/lib')

from .utils import LOCAL_VARS
from .lib import wall_score


def get_heights(points, DTM):
    dataset = gdal.Open(DTM, gdal.GA_ReadOnly)
    band = dataset.GetRasterBand(1)

    transform = dataset.GetGeoTransform()
    pixelWidth = abs(transform[1])
    pixelHeight = abs(transform[5])

    xOrigin = transform[0]
    yOrigin = transform[3]

    elevations = []
    for coord in points.coords:

        (x, y) = coord

        px = int((x - xOrigin) / pixelWidth)
        py = int((yOrigin - y) / pixelHeight)

        data = band.ReadAsArray(px, py, 1, 1)
        elevations.append(data[0][0])

    return elevations

def get_heights3D(points, DTM):
    dataset = gdal.Open(DTM, gdal.GA_ReadOnly)
    band = dataset.GetRasterBand(1)

    transform = dataset.GetGeoTransform()
    pixelWidth = abs(transform[1])
    pixelHeight = abs(transform[5])

    xOrigin = transform[0]
    yOrigin = transform[3]

    multipoint = []
    for coord in points.coords:

        (x, y) = coord

        px = int((x - xOrigin) / pixelWidth)
        py = int((yOrigin - y) / pixelHeight)

        data = band.ReadAsArray(px, py, 1, 1)
        z = data[0][0]

        point3D = Point(x, y, z)
        multipoint.append(point3D)

    return MultiPoint(multipoint)


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
    left = offset_point(pt, bearing, 270, (dist)/2)
    right = offset_point(pt, bearing, 90, (dist)/2)
    return LineString([left, right])

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

def init(gdf):
    DTM = LOCAL_VARS.DTM
    length = len(gdf.index)
    object_ids = []
    geoms = []
    lr_scores = []
    stonewall = []


    for index, row in gdf.iterrows():
        print(round(index / length * 100, 2))
        geometry = row["geometry"]
        linestring = redistribute_vertices(geometry, 5)
        coords = list(linestring.coords)

        DigeID = row["DigeID"]

        for i, p in enumerate(coords):
            ## every point except for the last point will use the next point to create bearing
            if i < len(coords) - 1:
                vert = Point(p)
                next_vert = Point(coords[i + 1])
                bearing = calculate_initial_compass_bearing(
                    vert.coords[0], next_vert.coords[0]
                )
            ### go between the last and the second last point 
            if i == len(coords) - 1:
                vert = Point(p)
                previous_vert = Point(coords[i - 1])
                bearing = calculate_initial_compass_bearing(
                    previous_vert.coords[0], vert.coords[0]
                )

            # pipeline
            cross_section_line = make_crossline(vert, bearing, 20.0)
            cross_points = redistribute_vertices(cross_section_line, 0.4)
            cross_points_3D = get_heights3D(cross_points, DTM)
            highest_point = check_highest_point(cross_points_3D)

            #print('ORIGINAL')
            ### compute basic linear regression and also print plots
            lr_score = wall_score.linear_regression_score3D(cross_points_3D)

            ### push data to lists for creation of dataframe
            object_ids.append("{0}-{1}".format(DigeID, i))
            geoms.append(cross_points_3D)
            lr_scores.append(lr_score)
            
        ### create dataframe
        data = {'OBJECTID': object_ids, 'lr_score': lr_scores, 'geometry': geoms}
        out_gdf = gpd.GeoDataFrame(data, crs="EPSG:25832")
    return out_gdf

def check_highest_point(multipoint):
    elevs = [p.z for p in multipoint]
    return elevs.index(max(elevs))

def check_stonewall(multipoint):
    elevs = [p.z for p in multipoint]

    high = max(elevs)
    low = min(elevs)
    if high - low < 0.3:  return 0 
    else: return 1


# %%
