#%%
import geopandas as gpd
import time
import os

input_path = '/home/ezra/stonewalls/data/profiles/cross_sections_aeroe_final.geojson'

gdf = gpd.read_file(input_path)
# %%
gdf.columns
# %%
geoms = gdf['geometry']
types = gdf['type']


# %%
x = geoms.apply((lambda x: [(p.z) for p in x])).tolist()

# %%
y = types.map({'0':'0', '1':'1', '2':'1', '3': '1'}).tolist()
# %%
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.33)

import numpy as np

X_train = np.array(X_train)
X_train = X_train.reshape(139726, 51, 1)
X_test = np.array(X_test)
X_test = X_test.reshape(68821, 51, 1)
y_train = np.array(y_train)
y_test = np.array(y_test)

# %%
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import datasets, layers, models
import matplotlib.pyplot as plt

model = keras.Sequential()
model.add(layers.Dense(51, activation='relu', input_shape=(51,1)))
model.add(layers.Dense(16))
model.add(layers.Dense(1))
model.summary()

model.compile(optimizer='adam',
              loss='log_cosh',
              metrics=['accuracy'])

#%%
history = model.fit(X_train, y_train, epochs=10, 
                    validation_data=(X_test, y_test))
# %%
