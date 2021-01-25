from osgeo import gdal, ogr
import math
import numpy as np
from shapely.geometry import Point, LineString, MultiPoint

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




