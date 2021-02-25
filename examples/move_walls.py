#%%
import geopandas as gpd
import time
import os
import sys; sys.path.append('..'); sys.path.append('../lib') 
from lib.core import initV2, init

start = time.time() 

path_to_stonewalls = '../data/stonewalls/aeroe/Stonewalls_AEROE.shp'
dtm = '../data/DTM/DTM_AEROE/DTM_AEROE.vrt'

gdf = gpd.read_file(path_to_stonewalls)
gdf = gdf.to_crs(epsg=25832)

gdf = gdf[:10]
 
thingV2 = initV2(gdf, dtm)

finish = time.time()

print("Time Taken is {0}s".format(finish - start))



# %%
output_path = "/mnt/c/Users/EZRA/Desktop/output"
import time
the_time = time.time()
thingV2.to_file(os.path.join(output_path, 'walls' + str(int(the_time)) + '.geojson'), driver="GeoJSON")

# %%

# %%
