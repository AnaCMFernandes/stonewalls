#%%
yellow_follow = "//wsl$/Ubuntu-20.04/home/afer/yellow/"
import os
import sys 
sys.path.append(yellow_follow)
sys.path.append(os.path.join(yellow_follow, "buteo/"))


import math
import time
import numpy as np
from glob import glob
from osgeo import gdal, ogr
import pandas as pd
from glob import glob
import re
import tensorflow_addons as tfa

# import ml_utils 
from machine_learning.patch_extraction import extract_patches, test_extraction, predict_raster
from raster.io import is_raster, rasters_are_aligned, raster_to_array, raster_to_metadata, stack_rasters, array_to_raster
#from raster.clip import clip_raster
#from raster.grid import raster_to_grid

# %%

path = 'C:/Users/AFER/Documents/Projects/StoneWalls/Data/stonewalls/Aeroe/training_data/test_rasters/'

## Stacking rasters

raster1 = glob(path + "dtm_test_clip.tif")
raster2 = glob(path + "dsm_test_clip.tif")
raster3 = glob(path + "hot_test_clip.tif")

rasters_stack = stack_rasters([raster1, raster3], path + 'stacked_dtmhot_clip.tif')


## Dividing into tiles: OPTION A
# stack = path + "stacked_dtmhot_clip.tif"
# grid = 'C:/Users/AFER/Documents/Projects/StoneWalls/Data/Denmark_10km_grid.gpkg'

# raster_to_grid(
#     raster=stack,
#     grid=grid,
#     out_dir=path,
#     generate_vrt=True,
#     overwrite=True,
# )

## Dividing into tiles: OPTION B
raster_path = "C:/Users/AFER/Documents/Projects/StoneWalls/Data/stonewalls/Aeroe/training_data/test_rasters/stacked_dtmhot_clip.tif"

dset = gdal.Open(raster_path)

width = dset.RasterXSize
height = dset.RasterYSize

print(width,'x',height)

tilesize = 5000

for i in range(0, width, tilesize):
    for j in range(0, height, tilesize):
        w = min(i+tilesize, width) - i
        h = min(j+tilesize, height) - j
        gdaltranString = "gdal_translate -of GTIFF -srcwin "+str(i)+", "+str(j)+", "+str(w)+", " \
            +str(h)+" " + raster_path + " " + path +"test_area" + "_"+str(i)+"_"+str(j)+".tif"
        os.system(gdaltranString)
