#%%
yellow_follow = '/home/afer/yellow/'
import os
import sys; sys.path.append(yellow_follow) 
sys.path.append(os.path.join(yellow_follow, "buteo/"))

import math
import time
import numpy as np
from glob import glob
from osgeo import gdal, gdal_array, ogr
import pandas as pd

from machine_learning import patch_extraction
from raster import io, clip
from vector import io
from gdal_utils import vector_to_reference
import matplotlib.pyplot as plt




#%%

folder = '/mnt/c/Users/AFER/Documents/Projects/StoneWalls/Data/stonewalls/Aeroe/checked/test2/antialiased/'

## Check raster to see if all is good
raster = folder +  "test_area_dtm.tif"
geom = glob(folder + "test_area.gpkg")

raster1 = gdal.Open(raster)
band = raster1.GetRasterBand(1)

rasterArray = gdal_array.LoadFile(raster)

raster1 = None
band = None
rasterArray = None

#%%
###extract geometry patches

patch_extraction.extract_patches(
        glob(folder + "test_area_dtm.tif"),
        folder,
        prefix="",
        postfix="_tests",
        size=64,
        #offsets=[(32, 32), (32, 0), (0, 32)],
        output_geom=True, ##output true for now, ignore geometry output
        clip_to_vector=None,
        verbose=1
    )



#%%

##Test patch extraction 

aligned = glob(folder + "test_area_dtm.tif")
numpy_array = glob(folder + "test_area_dtm_tests.npy")
grid = folder + "patches_64_tests.gpkg"

patch_extraction.test_extraction(aligned, numpy_array, grid)


# %%
##Visualize array to double check
arr = np.load(folder + "test_area_dtm_tests.npy")

for i in range(5):
    plt.subplot(330+1+i)
    plt.imshow(np.reshape(arr[i], (64,64)))
# %%
### inputs arrays and outputs rasters, for visualization of predictions

path = '/mnt/c/Users/AFER/Documents/Projects/StoneWalls/Data/stonewalls/Aeroe/checked/predictions/'
raster = folder +  "test_area_dtm.tif" 
out_path = folder + "test_area_prediction.tif"
blocks = np.load(path + "prediction_array_ana.npy") ## --> predicted array

# %%
patch_extraction.blocks_to_raster(blocks=blocks, 
                                  reference=raster, 
                                  out_path=out_path)
# %%
