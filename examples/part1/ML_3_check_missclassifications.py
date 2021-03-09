#%%
import geopandas as gpd
input_path = '/home/ezra/stonewalls/data/profiles/cross_sections_aeroe_final.geojson'

gdf = gpd.read_file(input_path)
#%%
from tensorflow import keras

model_path = '/home/ezra/stonewalls/examples/part1/models/balanced_flipped_no_noise.h5'
model = keras.models.load_model(model_path)
# %%
import numpy as np

x = np.load('/home/ezra/stonewalls/data/profiles/training_walls.npy')
y = np.load('/home/ezra/stonewalls/data/profiles/training_walls_labels.npy')
# %%

x = x.reshape(x.shape[0],51,1)
predictions = model.predict(x=x, verbose=1)
predictions = predictions.round()
# %%
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y.argmax(axis=1), predictions.argmax(axis=1))
cm
# %%
results = model.evaluate(x, y, batch_size=128)
# %%

one_cold_predictions = [np.argmax(x, axis=0) for x in predictions]
one_cold_y = [np.argmax(x, axis=0) for x in y]

gdf['predictions'] = list(one_cold_predictions)
gdf['truth'] = list(one_cold_y)
# %%
A = gdf['predictions']
B = gdf['truth']
C = A == B

# %%
gdf['agreement'] = C
# %%
gdf = gdf.rename(columns={'predictions':'step2class', 'truth':'step1class'})
# %%
gdf.to_file("missclassifications_04032021.geojson", driver='GeoJSON')


# %%
import sys; sys.path.append('/home/ezra/stonewalls/lib')
from helpers import just_plot
# %%
missclass = gdf.loc[gdf['agreement'] == False]

# %%
for i, row in missclass[100:120].iterrows():

   step_1 = row['step1class']
   step_2 = row['step2class'] 

   print('INITIAL CLASSIFICATION -----', step_1)
   print('NEW CLASSIFICATION -----', step_2)
   just_plot(row['geometry'])
# %%
