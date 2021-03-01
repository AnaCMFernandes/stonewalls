#%%
import geopandas as gpd
import time
import os
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import datasets, layers, models
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix


yellow_follow = '/mnt/c/Users/EZRA/Documents/TOOLBOXES/yellow/lib/'
import sys; sys.path.append(yellow_follow)
import ml_utils


input_path = '/home/ezra/stonewalls/data/profiles/cross_sections_aeroe_final.geojson'

gdf = gpd.read_file(input_path)

# %%

### CREATE LABELS
labels = gdf['type']
labels = labels.map({'0': 0, '1': 1, '2': 1, '3': 1 }).to_numpy()
counts = ml_utils.count_freq(labels)
mask = ml_utils.minority_class_mask(labels, counts[0][1])
labels = labels[mask]
labels = keras.utils.to_categorical(
    labels, num_classes=2, dtype='float32'
)
# %%
geom = gdf['geometry']
geom = geom[mask]
profiles = geom.apply((lambda x: np.array([(p.z) for p in x]).astype('float32')))
profiles = np.stack(profiles.values)

profiles_flipped = np.array([np.flip(f) for f in profiles])

x = np.concatenate([profiles, profiles_flipped])
x = ml_utils.add_noise(x)
y = np.concatenate([labels,labels])

# %%
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.33)
X_train = np.array([np.array(x).astype('float32') for x in X_train])
X_test = np.array([np.array(x).astype('float32') for x in X_test])
X_train = X_train.reshape(X_train.shape[0], 51 , 1)
X_test = X_test.reshape(X_test.shape[0], 51, 1)

# %%
model = keras.Sequential()
model.add(layers.Conv1D(filters=128, kernel_size = 5,   activation='relu', input_shape=(51,1)))
model.add(layers.Conv1D(filters=64, kernel_size = 3, activation='relu'))
model.add(layers.Dropout(0.5))
model.add(layers.MaxPooling1D(pool_size=2))
model.add(layers.Flatten())
model.add(layers.Dense(units=100, activation='relu'))
# model.add(layers.Dense(units=50, activation='relu'))

model.add(layers.Dense(units = 2, activation='softmax'))
model.summary()
model.compile(optimizer='adam',
              loss="binary_crossentropy",
              metrics=['accuracy'])

#  model.fit(X_train, y_train, epochs=20, 
#                     validation_data=(X_test, y_test))

from tensorflow.keras.callbacks import EarlyStopping, LearningRateScheduler
import math

def step_decay(epoch):
   initial_lrate = 0.001
   drop = 0.5
   epochs_drop = 5

   # import pdb; pdb.set_trace()

   lrate = initial_lrate * math.pow(drop, math.floor((1 + epoch) / epochs_drop)),
   return float(lrate)


history = model.fit(
   x=X_train,
   y=y_train,
   epochs=20,
   verbose=1,
   validation_split=0.2,
   validation_data=(X_test, y_test),
   # callbacks=[
   #    LearningRateScheduler(step_decay),
   #    EarlyStopping(
   #          monitor="val_loss",
   #          patience=10,
   #          min_delta=0.1,
   #          restore_best_weights=True,
   #    )
   # ]
)

# %%

predictions = model.predict(x=X_test, verbose=1)
predictions = predictions.round()
cm = confusion_matrix(y_test.argmax(axis=1), predictions.argmax(axis=1))
cm

# %%
