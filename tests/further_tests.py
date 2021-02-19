#%%
import geopandas as gpd

path_to_profiles = '../data/profiles/test_completed_cross_sections_2.geojson'

df = gpd.read_file(path_to_profiles) 
# df['match'] = df.col1 == df.col1.shift()

# for index, row in df.iterrows():
#    row['wall_id'] = row['OBJECTID'].split('-')[0] 
#    print(row['wall_id'])





# %%
df['type'].value_counts()
# %%

from shapely.geometry import MultiPoint, LineString, Point

df['match'] = df['type'] == df['type'].shift()

lines = []
last = (-1,-1)
for index, row in df.iterrows():
   x = row['geometry'][25].x
   y = row['geometry'][25].y

   if index == 0:
      last = (x,y)
      continue
   else:
      line = LineString([Point(last), Point(x,y)])
      lines.append(line)
      last = (x,y)

   row['yo'] = 'whatup'

print(lines)

print(df)
# data = { 'geometry': lines }

# out_gdf = gpd.GeoDataFrame(data, crs="EPSG:25832")
# %%
out_gdf.to_file("../data/stonewalls/corrected_lines.geojson", driver="GeoJSON")