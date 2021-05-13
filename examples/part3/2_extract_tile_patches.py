buteo_follow = "c:/buteo/"
buteo_buteo_follow = "c:/buteo/buteo/"

import sys

sys.path.append(buteo_follow)
sys.path.append(buteo_buteo_follow)
sys.path.append(buteo_buteo_follow + "filters/")
sys.path.append(buteo_buteo_follow + "machine_learning/")
sys.path.append(buteo_buteo_follow + "raster/")

# from convolutions import *
# from kernel_generator import *
from filter import *
from patch_extraction import *
from raster import *

from osgeo import gdal

import glob

import os

in_and_out_dir = r"C:\Users\EZRA\Desktop\raster_magic\aeroe_data\prediction_tiles\\"

tifs = glob.glob(in_and_out_dir + "*.tif")
# prediction_prox = glob.glob("prediction_prox_tiles/*.tif")
# walls = glob.glob("walls_tiles/*.tif")
# walls_prox = glob.glob("walls_prox_tiles/*.tif")


for i in range(len(tifs)):
    # out_name = "{}.npy".format(tifs[i].split(".")[0])

    extract_patches(tifs[i], out_dir=in_and_out_dir, size=64, generate_grid_geom=False)

    # np.save(out_name, npy)
# predproxnpy = raster_to_array(prediction_prox[i])
# wallsnpy = raster_to_array(walls[i])
# wallsproxnpy = raster_to_array(walls_prox[i])

