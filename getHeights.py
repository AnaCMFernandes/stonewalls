from osgeo import gdal
from pyproj import Transformer

def getHeights(input):

   def pixelCoords(arr):
      return [
         math.floor((arr[0] - xOrigin) / pixelWidth),
         math.floor((yOrigin - arr[1]) / pixelHeight),
      ]   

   DTM = 'M:/Ekstern_datasamling/Danmark/Frie_DATA/DTM_2014/DTM_Grid_1km_TIFF/_merged.vrt'
   UTM32 = '+proj=utm +zone=32 +ellps=GRS80 +units=m +no_defs'
   samples = input.data
   options = input.options
   dataset = gdal.Open(filename, gdal.GA_ReadOnly)
   band = dataset.GetRasterBand(1)

   transform = dataset.GetGeoTransform()
   pixelWidth = abs(transform[1])
   pixelHeight = abs(transform[5])
   xOrigin = transform[0]
   yOrigin = transform[3]

   transformer = Transformer.from_crs('EPSG:4326', UTM32)
  for i in samples: 
    const currFeature = samples[i]
    const currCoords = currFeature.geometry.coordinates
    const heights = []

    for j in currCoords: 
      const pixCoords = pixelCoords(transformer.itransform(currCoords[j]))
      const height = band.pixels.get(pixCoords[0], pixCoords[1])
      heights.push(round(height, 4))
    

    // reduce size of crossSection
    currFeature.geometry.coordinates = [
      currFeature.geometry.coordinates[0],
      currFeature.geometry.coordinates[currCoords.length - 1],
    ];
    currFeature.properties.profile = heights.toString();
    currFeature.properties.stepLength = options.stepLength;
  

  return samples;