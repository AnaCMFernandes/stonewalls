import os, sys
from osgeo import gdal

out_path = r"C:\Users\EZRA\Desktop\raster_magic\aeroe_data\prediction_tiles\\"
raster_path = r"C:\Users\EZRA\Desktop\raster_magic\aeroe_data\prediction_tiles\8bit_prediction.tif"

print(os.path.exists(raster_path))
# out_dir = "C:/Users/AFER/Documents/Projects/StoneWalls/Data/stonewalls/Aeroe/training_data/test_rasters/stacked_test/tiles/"

dset = gdal.Open(raster_path)

width = dset.RasterXSize
height = dset.RasterYSize

print(width, "x", height)

tilesize = 5000

for i in range(0, width, tilesize):
    for j in range(0, height, tilesize):
        w = min(i + tilesize, width) - i
        h = min(j + tilesize, height) - j
        gdaltranString = (
            "gdal_translate -of GTIFF -srcwin "
            + str(i)
            + ", "
            + str(j)
            + ", "
            + str(w)
            + ", "
            + str(h)
            + " "
            + raster_path
            + " "
            + out_path
            + "tile"
            + "_"
            + str(i)
            + "_"
            + str(j)
            + ".tif"
        )
        os.system(gdaltranString)
