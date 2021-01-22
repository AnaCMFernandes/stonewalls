#%%
from osgeo import gdal, ogr
import os
import numpy as np
import geopandas as gpd
import shapely
from shapely.geometry import Point, LineString, MultiPoint
from shapely.ops import unary_union, substring
import matplotlib.pyplot as plt
import LOCAL_VARS

# %%
# Stonewalls
layer = gpd.read_file(LOCAL_VARS.STONEWALLS)
layer = layer.to_crs(epsg=25832)

layer['length'] = layer.geometry.length

#%%

def redistribute_vertices(geom, distance):
    if geom.geom_type == 'LineString':
        num_vert = int(round(geom.length / distance))
        if num_vert == 0:
            num_vert = 1
        return LineString(
            [geom.interpolate(float(n) / num_vert, normalized=True)
             for n in range(num_vert + 1)])
    elif geom.geom_type == 'MultiLineString':
        parts = [redistribute_vertices(part, distance)
                 for part in geom]
        return type(geom)([p for p in parts if not p.is_empty])
    else:
        raise ValueError('unhandled geometry %s', (geom.geom_type,))



# %%
#updating the geometry of each linestring
gdf_line = layer[0:5]  

gdf_line_interpolate = gdf_line.copy()
gdf_line_interpolate.geometry = gdf_line.geometry.apply(redistribute_vertices,distance=15)
gdf_line_interpolate['nverts'] = gdf_line_interpolate.geometry.apply(lambda x: len(x.coords))

#%%
#or just adding the attribute column:
gdf_line_interpolate = gdf_line.copy()
gdf_line_interpolate['nverts'] = gdf_line.geometry.apply(redistribute_vertices,distance=15).apply(lambda x: len(x.coords))

