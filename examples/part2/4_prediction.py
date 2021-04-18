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

model_dir = "C:/Users/AFER/Documents/Projects/StoneWalls/Data/stonewalls/Aeroe/training_data/predictions/"

model = model_dir + "model1_1L_rotations_32.h5"

test_path = "C:/Users/AFER/Documents/Projects/StoneWalls/Data/stonewalls/Aeroe/training_data/test_rasters/"

stacked_tifs = glob(test_path + "*.tif")

tile_dir = 'C:/Users/AFER/Documents/Projects/StoneWalls/Data/stonewalls/Aeroe/training_data/predictions/'

#for single layer prediction
raster = test_path + "dtm_test_clip.tif"

from tensorflow_addons.activations import mish

num = 0

for tif in stacked_tifs:
    num = num + 1
    # print("raster_" + str(num))
    print("predicting tile {0}".format(num))
    predict_raster(
        tif,
        model,
        out_path=tile_dir + "pred1_dtm_rotations32.tif",
        offsets=[(32, 32), (16, 16)],
        batch_size=16,
        mirror=False,
        rotate=False,
        device="gpu",
        custom_objects={ "mish": mish }
    )
    print("All raster tiles predicted.")