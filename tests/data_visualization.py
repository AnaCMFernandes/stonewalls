#%%
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import geopandas as gpd
from osgeo import gdal, ogr
from glob import glob

#%%
stack_path = '/mnt/c/Users/AFER/Projects/StoneWalls/Data/rasters/stacked_dtmsobelhot_tiles/tile_0_0.tif'
dtm_path = '/mnt/c/Users/AFER/Projects/StoneWalls/Data/rasters/dtm_tiles/test_area_0_0.tif'
dtm = gdal.Open(stack_path)
stack_tile = gdal.Open(stack_path)

# %%
def raster2array(geotif_file):
    metadata = {}
    dataset = gdal.Open(geotif_file)
    metadata['array_rows'] = dataset.RasterYSize
    metadata['array_cols'] = dataset.RasterXSize
    metadata['bands'] = dataset.RasterCount
    metadata['driver'] = dataset.GetDriver().LongName
    metadata['projection'] = dataset.GetProjection()
    metadata['geotransform'] = dataset.GetGeoTransform()

    mapinfo = dataset.GetGeoTransform()
    metadata['pixelWidth'] = mapinfo[1]
    metadata['pixelHeight'] = mapinfo[5]
#     metadata['xMin'] = mapinfo[0]
#     metadata['yMax'] = mapinfo[3]
#     metadata['xMax'] = mapinfo[0] + dataset.RasterXSize/mapinfo[1]
#     metadata['yMin'] = mapinfo[3] + dataset.RasterYSize/mapinfo[5]

    metadata['ext_dict'] = {}
    metadata['ext_dict']['xMin'] = mapinfo[0]
    metadata['ext_dict']['xMax'] = mapinfo[0] + dataset.RasterXSize/mapinfo[1]
    metadata['ext_dict']['yMin'] = mapinfo[3] + dataset.RasterYSize/mapinfo[5]
    metadata['ext_dict']['yMax'] = mapinfo[3]

    metadata['extent'] = (metadata['ext_dict']['xMin'],metadata['ext_dict']['xMax'],
                          metadata['ext_dict']['yMin'],metadata['ext_dict']['yMax'])

    if metadata['bands'] == 1:
        raster = dataset.GetRasterBand(1)
        metadata['noDataValue'] = raster.GetNoDataValue()
        metadata['scaleFactor'] = raster.GetScale()

        # band statistics
        metadata['bandstats'] = {} #make a nested dictionary to store band stats in same 
        stats = raster.GetStatistics(True,True)
        metadata['bandstats']['min'] = round(stats[0],2)
        metadata['bandstats']['max'] = round(stats[1],2)
        metadata['bandstats']['mean'] = round(stats[2],2)
        metadata['bandstats']['stdev'] = round(stats[3],2)

        array = dataset.GetRasterBand(1).ReadAsArray(0,0,metadata['array_cols'],metadata['array_rows']).astype(np.float)
        array[array==int(metadata['noDataValue'])]=np.nan
        array = array/metadata['scaleFactor']
        return array, metadata

    elif metadata['bands'] > 1:
        print('More than one band ... fix function for case of multiple bands')



# %%
##visualizations
def plot_band_array(band_array,refl_extent,title,cbar_label,colormap='terrain',alpha=1):
    plt.imshow(band_array,extent=refl_extent,alpha=alpha); 
    cbar = plt.colorbar(); plt.set_cmap(colormap); 
    cbar.set_label(cbar_label,rotation=270,labelpad=20)
    plt.title(title); ax = plt.gca(); 
    ax.ticklabel_format(useOffset=False, style='plain') #do not use scientific notation #
    rotatexlabels = plt.setp(ax.get_xticklabels(),rotation=90) #rotate x tick labels 90 degree


def hillshade(array,azimuth,angle_altitude):
    azimuth = 360.0 - azimuth 

    x, y = np.gradient(array)
    slope = np.pi/2. - np.arctan(np.sqrt(x*x + y*y))
    aspect = np.arctan2(-x, y)
    azimuthrad = azimuth*np.pi/180.
    altituderad = angle_altitude*np.pi/180.

    shaded = np.sin(altituderad)*np.sin(slope) + np.cos(altituderad)*np.cos(slope)*np.cos((azimuthrad - np.pi/2.) - aspect)

    return 255*(shaded + 1)/2
# %%

dtm_array, dtm_metadata = raster2array('/mnt/c/Users/AFER/Projects/StoneWalls/Data/rasters/dtm_tiles/test_area_0_0.tif')

#%%
plot_band_array(dtm_array, dtm_metadata['extent'], 'DTM', 'Elevation')
ax = plt.gca(); plt.grid('on')
# %%
hs_array = hillshade(dtm_array,225,45)
plot_band_array(hs_array,dtm_metadata['extent'],'TEAK Hillshade, Aspect=225°',
                'Hillshade',colormap='Greys',alpha=0.8)
ax = plt.gca(); plt.grid('on') 
# %%
#Overlay transparent hillshade on DTM:
fig = plt.figure(frameon=False)
im1 = plt.imshow(dtm_array,cmap='terrain_r',extent=dtm_metadata['extent']); 
cbar = plt.colorbar(); cbar.set_label('Elevation, m',rotation=270,labelpad=20)
im2 = plt.imshow(hs_array,cmap='Greys',alpha=0.8,extent=dtm_metadata['extent']); #plt.colorbar()
ax=plt.gca(); ax.ticklabel_format(useOffset=False, style='plain') #do not use scientific notation 
rotatexlabels = plt.setp(ax.get_xticklabels(),rotation=90) #rotate x tick labels 90 degrees
plt.grid('off'); # plt.colorbar(); 
plt.title('Hillshade + DTM')
# %%
## validation
path = '/mnt/c/Users/AFER/Projects/Stonewalls/Data/postprocess/'

y_pred = np.load(path + 'bestmodel_1_64.npy')
y_truth = np.load(path + 'walls_singlepart_tile1_64.npy')


path_mask = '/mnt/c/Users/AFER/Projects/Stonewalls/Data/postprocess/'
val_meta = pd.read_csv(path_mask + 'val_mask_area1.csv')

#%%

val_mask = np.swapaxes(val_meta[val_meta["val_area"] == 1].values, 0, 1)[0]
print(y_pred.shape)
print(y_truth.shape)
print(val_mask.shape)

y_pred_val = y_pred[val_mask]
y_truth_val = y_truth[val_mask]
print(y_pred_val.shape)
print(y_truth_val.shape)

#%%

def pixel_wise_eval(y_true, y_pred):
    return (
        np.logical_or(
            np.logical_and(y_true > 0, y_pred > 0),
            np.logical_and(y_true == 0, y_pred == 0),
        ).sum()
        / y_true.size
    )

wallspred_eval = pixel_wise_eval(y_truth_val, y_pred_val)

print("pixel wise metric: ", np.round(wallspred_eval, 2))

#%%

pred_images = y_pred_val[[1805, 63, 64, 2407]]
truth_images = y_truth_val[[1805, 63, 64, 2407]]
