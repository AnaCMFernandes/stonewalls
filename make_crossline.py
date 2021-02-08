from osgeo import gdal, ogr
import math
import numpy as np
from shapely.geometry import Point, LineString, MultiPoint
from shapely import affinity
import geopandas as gpd
import LOCAL_VARS
import wall_score
from scipy import signal

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

    x_list = []
    y_list = []
    z_list = []

    for coord in points.coords:

        (x, y) = coord

        px = int((x - xOrigin) / pixelWidth)
        py = int((yOrigin - y) / pixelHeight)

        data = band.ReadAsArray(px, py, 1, 1)
        z = data[0][0]

        x_list.append(x) 
        y_list.append(y) 
        z_list.append(z)

        # point3D = Point(x, y, z)
        # multipoint.append(point3D)

    lowest_point = min(z_list)
    corrected_z_list = [z - lowest_point for z in z_list]

    ###
    # make multipoint from x_list, y_list, and corrected_z

    for i in range(len(x_list)):
        point3D = (x_list[i], y_list[i], corrected_z_list[i])
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

def make_crossline(pt, bearing, dist, shift_offset=0, interval=LOCAL_VARS.PIXEL_SIZE):
    ### move the line by the index difference between the ideal center (25) and the current center (0-50)
    totalshift = shift_offset * interval
    left = offset_point(pt, bearing, 270, ((dist)/2)+totalshift)
    right = offset_point(pt, bearing, 90, ((dist)/2)-totalshift)
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

def check_stonewall(multipoint):
    elevs = [p.z for p in multipoint]
    high = max(elevs)
    low = min(elevs)
    if high - low < 0.3:  return 0 
    else: return 1

def init(gdf):
    DTM = LOCAL_VARS.DTM
    # length = len(gdf.index)
    object_ids = []
    geoms = []
   
    for _, row in gdf.iterrows():
        # print(round(index / length * 100, 2))
        geometry = row["geometry"]
        linestring = redistribute_vertices(geometry, 5)
        coords = list(linestring.coords)

        DigeID = row["DigeID"]
        types = []

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

            wall_score.only_plot(cross_points_3D, 'black')

            peak, wall_type = wall_score.find_wall_peak(cross_points_3D)

            ### calculate correction
            ideal_mid = math.floor(len(cross_points_3D)/2)
           
            ## if there are multiple peaks, then take the peak that is closest to the center.
            if (len(peak) > 1):
                curr_closest = -1
                closest_value = 50
                for peak in peak:
                    diff = abs(peak - ideal_mid)
                    if (diff < closest_value):
                        closest_value = diff
                        curr_closest = peak
                
                peak = curr_closest
            elif (len(peak) == 0): peak = ideal_mid

            
            correction = ideal_mid - peak

            ### compute basic linear regression and also print plots
             
            if correction != 0:
                # pipeline with correction
                cross_section_line = make_crossline(vert, bearing, 20.0, correction)
                cross_points = redistribute_vertices(cross_section_line, 0.4)
                cross_points_3D = get_heights3D(cross_points, DTM)
             
                
                if (wall_type=='1'):     
                    wall_score.only_plot(cross_points_3D, 'green')
                if (wall_type=='2'):     
                    wall_score.only_plot(cross_points_3D, 'orange')
                if (wall_type=='3'):     
                    wall_score.only_plot(cross_points_3D, 'red')
                if (wall_type=='0'):     
                    wall_score.only_plot(cross_points_3D, 'blue')

                
                ### compute basic linear regression and also print plots
                
            ### push data to lists for creation of dataframe
            object_ids.append("{0}-{1}".format(DigeID, i))
            geoms.append(cross_points_3D)
            types.append(wall_type)
           
        ### create dataframe
        data = {'OBJECTID': object_ids, 'type': types, 'geometry': geoms}
        out_gdf = gpd.GeoDataFrame(data, crs="EPSG:25832")
    return out_gdf

