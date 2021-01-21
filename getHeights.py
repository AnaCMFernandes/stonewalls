from osgeo import gdal
from pyproj import Transformer

def getHeights(points, DTM):
   dataset = gdal.Open(DTM, gdal.GA_ReadOnly)
   band = dataset.GetRasterBand(1)

   transform = dataset.GetGeoTransform()
   pixelWidth = abs(transform[1])
   pixelHeight = abs(transform[5])

   xOrigin = transform[0]
   yOrigin = transform[3]

   elevation = []
   for coord in points.coords:

      (x, y) = coord

      px = int((x - xOrigin) / pixelWidth)
      py = int((yOrigin - y) / pixelHeight)
      
      data = band.ReadAsArray(px, py, 1, 1)
      elevation.append(data[0][0])

   return elevation