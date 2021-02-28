#%%
from osgeo import gdal, ogr
from scipy import signal
from shapely import affinity
from shapely.geometry import Point, LineString, MultiPoint
import math
import numpy as np
import geopandas as gpd
# from . import helpers
# from helpers import *
import helpers

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
    try:
        x = pt.x + dist * math.sin(bearing)
        y = pt.y + dist * math.cos(bearing)
    except:
        pt = Point(pt)
        x = pt.x + dist * math.sin(bearing)
        y = pt.y + dist * math.cos(bearing)
    return Point(x, y)

def make_crossline(pt, bearing, dist, shift_offset=0, interval=0.4):
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

def initV2(gdf, DTM, subwall_distance=5):
    length = len(gdf.index)
    object_ids = []
    geoms = []
    types = []
    corrected_subwalls = []
    for index, row in gdf.iterrows():
        print(round(index / length * 100, 1))
        geometry = row["geometry"]

        outer_coords = list(geometry.coords)
        
        for i in range(len(outer_coords) - 1):
            try:
                curr_point = outer_coords[i]
                nxt_point = outer_coords[i+1]
            except:
                import pdb; pdb.set_trace()
            subline = LineString([curr_point, nxt_point])

            ## calculate for later when needs to be shifted
            subline_bearing = calculate_initial_compass_bearing(curr_point, nxt_point)

            linestring = redistribute_vertices(subline, subwall_distance)

            #coordinates of the points comprising linestring
            inner_coords = list(linestring.coords)

            DigeID = row["DigeID"]

            #array that will contain the wall_type and correction from for the individual profiles
            subwall_types = []
            subwall_corrections = []
            for i, p in enumerate(inner_coords):
                ## every point except for the last point will use the next point to create bearing
                vert = Point(p)
                if i < len(inner_coords) - 1:
                    next_vert = Point(inner_coords[i + 1])
                    bearing = calculate_initial_compass_bearing(
                        vert.coords[0], next_vert.coords[0]
                    )
                ### go between the last and the second last point 
                if i == len(inner_coords) - 1:
                    previous_vert = Point(inner_coords[i - 1])
                    bearing = calculate_initial_compass_bearing(
                        previous_vert.coords[0], vert.coords[0]
                    )

                # pipeline
                cross_section_line = make_crossline(vert, bearing, 20.0)
                cross_points = redistribute_vertices(cross_section_line, 0.4)
                cross_points_3D = get_heights3D(cross_points, DTM)

                # helpers.just_plot(cross_points_3D, 'black')

                peaks_array, wall_type = helpers.find_wall_peak(cross_points_3D)
                
                ### calculate correction
                ideal_mid = math.floor(len(cross_points_3D)/2)
                best_peak = None
                ## if there are multiple peaks, then take the peak that is closest to the center.

                if (len(peaks_array) > 1):
                    curr_closest = -1
                    closest_value = 50
                    for peak in peaks_array:
                        diff = abs(peak - ideal_mid)
                        if (diff < closest_value):
                            closest_value = diff
                            curr_closest = peak
                    best_peak = curr_closest
                elif (len(peaks_array) == 1 ):
                    best_peak = peaks_array[0]
                else: 
                    best_peak = ideal_mid

                correction = ideal_mid - best_peak

                subwall_types.append(wall_type)
                subwall_corrections.append(correction)
        
                if correction != 0:
                    # pipeline with correction
                    cross_section_line = make_crossline(vert, bearing, 20.0, correction)
                    cross_points = redistribute_vertices(cross_section_line, 0.4)
                    cross_points_3D = get_heights3D(cross_points, DTM)



                ## plot walltypes for visual inspection
                # print(wall_type)
                # if ( wall_type not in ['1']):
                #     helpers.plot_profiles(cross_points_3D, wall_type)

                ### push data to lists for creation of dataframe
                object_ids.append("{0}-{1}".format(DigeID, i))
                geoms.append(cross_points_3D)
                types.append(wall_type)

            #### REDRAW WALL
            # average correciton of the arrays along the wall


            #### IF THE WALL IS SHORTER THAN 5, DONT BOTH CORRECTING - OTHERWISE CORRECT BY THE MEDIAN OF THE SUBWALL CORRECTIONS

            if (len(subwall_corrections) > 5):
                average_correction = np.median(subwall_corrections) * 0.4
            else:
                average_correction = 0
            

            # apply correction
            if average_correction > 0:
                new_curr_point = offset_point(curr_point, subline_bearing, 270, abs(average_correction))
                new_nxt_point = offset_point(nxt_point, subline_bearing, 270, abs(average_correction))
            elif average_correction < 0:
                new_curr_point = offset_point(curr_point, subline_bearing, 90, abs(average_correction))
                new_nxt_point = offset_point(nxt_point, subline_bearing, 90, abs(average_correction))
            else:
                new_curr_point = curr_point
                new_nxt_point = nxt_point
        
            # create new line based on 
            corrected_geometry = LineString([new_curr_point, new_nxt_point])


            corrected_linestring = redistribute_vertices(corrected_geometry, subwall_distance)
            corrected_coords = list(corrected_linestring.coords)


            ### USE THIS IF YOU WANT THE LINES  **TO** BE CORRECTED
            for i in range(len(corrected_coords) - 1):
                try:
                    crnt_prfl = subwall_types[i]
                    next_prfl = subwall_types[i+1]

                    crnt_point = corrected_coords[i]
                    nxt_point = corrected_coords[i+1]
                except:
                    import pdb; pdb.set_trace()
                if (crnt_prfl != '0' and next_prfl != '0'):
                    corrected_subwall = LineString([crnt_point, nxt_point])
                    corrected_subwalls.append(corrected_subwall)

            ### USE THIS IF YOU WANT THE LINES ***NOT TO BE*** CORRECTED
            # for i in range(len(inner_coords) - 1):
            #     try:
            #         crnt_prfl = subwall_types[i]
            #         next_prfl = subwall_types[i+1]

            #         crnt_point = inner_coords[i]
            #         nxt_point = inner_coords[i+1]
            #     except:
            #         import pdb; pdb.set_trace()
            #     if (crnt_prfl != '0' and next_prfl != '0'):
            #         corrected_subwall = LineString([crnt_point, nxt_point])
            #         corrected_subwalls.append(corrected_subwall)



    ### create dataframe
    data = {'OBJECTID': object_ids, 'type': types, 'geometry': geoms}
    subwalldata = {'geometry': corrected_subwalls}
    out_gdf1 = gpd.GeoDataFrame(data, crs="EPSG:25832") 
    out_gdf2 = gpd.GeoDataFrame(subwalldata, crs="EPSG:25832") 

    # return out_gdf1
    return out_gdf1, out_gdf2
#%%

import geopandas as gpd
import time
import os
import sys; sys.path.append('..'); sys.path.append('../lib') 


start = time.time() 

path_to_stonewalls = '../data/stonewalls/aeroe/Stonewalls_AEROE.shp'
dtm = '../data/DTM/DTM_AEROE/DTM_AEROE.vrt'

gdf = gpd.read_file(path_to_stonewalls)
gdf = gdf.to_crs(epsg=25832)
# gdf = gdf[400:420]

profiles, walls = initV2(gdf, dtm, 5)
# thingV2 = initV2(gdf, dtm)
finish = time.time()

print("Time Taken is {0}s".format(finish - start))



 # %%
output_path = "/mnt/c/Users/EZRA/Desktop/output"
import time
the_time = time.time()

profiles.to_file(os.path.join(output_path, str(int(the_time)) + 'profiles' + '.geojson'), driver="GeoJSON")
walls.to_file(os.path.join(output_path, str(int(the_time)) + 'walls' + '.geojson'), driver="GeoJSON")

# %%
