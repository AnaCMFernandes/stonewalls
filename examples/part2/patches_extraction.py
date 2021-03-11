#%%
yellow_follow = '/home/afer/yellow/'
import os
import sys 
sys.path.append(yellow_follow)
sys.path.append(os.path.join(yellow_follow, "lib"))

import math
import time
import numpy as np
from glob import glob
from osgeo import gdal
import pandas as pd

from patch_extraction import extract_patches, test_extraction
from raster_io import raster_to_array, raster_to_metadata



#%%

folder = '../../Data/'

#%%
###extract geometry patches

extract_patches(
        glob(folder + "rasters/*.tif"),
        folder + "out/",
        prefix="",
        postfix="_patches",
        size=64,
        #offsets=[(32, 32), (32, 0), (0, 32)],
        output_geom=True,
        clip_to_vector=folder + "walls_buffer.gpkg",
        verbose=1
    )

#%%

aligned = glob(folder + "rasters/*.tif")
numpy_arrays = glob(folder + "out/*.npy")
grid = folder + "out/patches_64_patches.gpkg"

test_extraction(aligned, numpy_arrays, grid)
