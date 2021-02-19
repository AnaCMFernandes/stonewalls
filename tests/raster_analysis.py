# %%
import os
from osgeo import gdal
 
import numpy as np
import sys

path_to_yellow = "/mnt/c/Users/EZRA/Documents/TOOLBOXES/yellow/"
sys.path.append(path_to_yellow)
sys.path.append(os.path.join(path_to_yellow, "lib"))

from patch_extraction import extract_patches

input_path = "/mnt/d/stonewalls_D/"
input_filenames = ['stonewall_raster_10km_607_58', 'stonewall_raster_10km_607_59', 'stonewall_raster_10km_608_57', 'stonewall_raster_10km_608_59', 'stonewall_raster_10km_609_57', 'stonewall_raster_10km_609_58']
input_file = os.path.join(input_path, input_filenames[0]) + '.tif'

dtm = gdal.Open(input_file)
band = dtm.GetRasterBand(1)
array = np.array([]
)
extract_patches(dtm, array)

