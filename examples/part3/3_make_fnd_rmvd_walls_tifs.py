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

walls_prox_tiles = glob.glob("walls_prox_tiles/*.npy")
prediction_tiles = glob.glob("prediction_tiles/*.npy")

walls_ref = glob.glob("wall_tiles/*.tif")

for i in range(len(walls_prox_tiles)):

    walls_prox_arr = np.load(walls_prox_tiles[i])
    pred_arr = np.load(prediction_tiles[i])
    ref = walls_ref[i]

    prox_mask = walls_prox_arr < 25
    pred_arr[prox_mask] = 0

    npy_out_name = "found_walls/{}_found_walls.npy".format(i)
    tif_out_name = "found_walls/{}_found_walls.tif".format(i)

    np.save(npy_out_name, pred_arr)
    blocks_to_raster(pred_arr, reference=ref, out_path=tif_out_name)

# walls_prox = glob.glob("walls_prox_tiles/*.npy")
# prediction = glob.glob("prediction_tiles/*.npy")

# walls_ref = glob.glob("wall_tiles/*.tif")

# for i in range(len(walls_prox)):

#     walls_prox_arr = np.load(walls_prox[i])

#     pred_arr = np.load(prediction[i])

#     ref = walls_ref[i]

#     prox_mask = walls_prox_arr < 5
#     pred_arr[prox_mask] = 0

#     npy_out_name = "found_walls/{}_found_walls.npy".format(i)
#     tif_out_name = "found_walls/{}_found_walls.tif".format(i)

#     np.save(npy_out_name, pred_arr)
#     blocks_to_raster(pred_arr, reference=ref, out_path=tif_out_name)

