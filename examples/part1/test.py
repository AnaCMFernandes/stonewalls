#%%
import geopandas as gpd

gdf = gpd.read_file('/home/ezra/stonewalls/data/profiles/geojson/all_profiles_100321.geojson')
#%%
import numpy as np
from scipy.signal import find_peaks
import sklearn.linear_model as LinearRegression
import sys; sys.path.append('/home/ezra/stonewalls/lib')
from matplotlib import pyplot as plt
# from helpers import just_plot
sub_gdf = gdf


def just_plot(geom, color='green', title=''):
      try:
         elevs = [p.z for p in geom]
      except:
         elevs = [p.y for p in geom]

      x = np.arange(len(elevs))
      y = np.array(elevs)

      plt.plot(x, y, color=color, alpha=0.7)
      

      plt.yticks(np.arange(1.5,step=0.2))

      plt.show()
      return True



for index, row in sub_gdf.iterrows():
   profile = row['geometry']
   wall_type = row['type']
   elevs = np.array([p.z for p in profile])

   if wall_type == '0':
      # peaks, _ = find_peaks(elevs, prominence=0.1)
      X = np.arange(len(elevs))
      y = np.array(elevs)

      X = X.reshape(-1, 1)

      LR = LinearRegression.LinearRegression()
      LR.fit(X, y)
      score = LR.score(X, y)
      if score > 0.95:
         # print(score)
         just_plot(profile, 'red') 
      # else:
      #    print(index)
      #    just_plot(profile, 'blue')
   

    


# %%
