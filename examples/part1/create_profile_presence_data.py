
import geopandas as gpd
import time
import sys; sys.path.append('/home/ezra/stonewalls/lib')
from datetime import datetime

from core import create_profiles

start = time.time() 

path_to_stonewalls = '/mnt/c/Users/ezra/OneDrive - NIRAS/thesis/Data/aeroe/Stonewalls/Stonewalls_AEROE.shp'
dtm = '/mnt/c/Users/ezra/Desktop/AEROE_terainn_data/DTM/DTM_AEROE.vrt'
output_folder = '/mnt/c/Users/ezra/Desktop/wall_output/'
distance = 0.4
date = datetime.now().strftime("%m-%d-%Y")


gdf = gpd.read_file(path_to_stonewalls)
gdf = gdf.to_crs(epsg=25832)

# activate and replace first arg of create_profiles for smaller subset
sub_gdf = gdf[:50]

profiles, walls = create_profiles(sub_gdf, dtm, subwall_distance=distance)

profiles_out = '{}profiles_{}_{}.geojson'.format(output_folder, str(distance)+'m', date)
walls_out = '{}walls_{}_{}.geojson'.format(output_folder, str(distance)+'m', date)

profiles.to_file(profiles_out, driver="GeoJSON")
walls.to_file(walls_out, driver="GeoJSON")

finish = time.time()

print("Time Taken is {0}s".format(finish - start))
print(output_folder)



