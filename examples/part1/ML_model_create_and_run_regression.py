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

# %%

x = np.load('/home/ezra/stonewalls/data/profiles/npy/training_by_peak_walls.npy')
max_x = 254
min_x = -7
x = ((x - min_x) / (max_x - min_x))

y = np.load('/home/ezra/stonewalls/data/profiles/npy/training_by_peak_walls_labels.npy')
np.where(y==-99,53, y)

# %%
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.33)

X_train = np.array([np.array(x).astype('float32') for x in X_train])
X_test = np.array([np.array(x).astype('float32') for x in X_test])
X_train = X_train.reshape(X_train.shape[0], 51 , 1)
X_test = X_test.reshape(X_test.shape[0], 51, 1)
y_train = np.array(y_train)
y_test = np.array(y_test)

# %%
   
model = keras.Sequential()
model.add(layers.Conv1D(filters=100, kernel_size = 3, kernel_initializer='he_normal', input_shape=(51,1), activation ='relu'))
model.add(layers.Flatten())
model.add(layers.Dense(units=100,kernel_initializer='he_normal', activation ='relu'))
model.add(layers.Dense(units = 1, kernel_initializer='he_normal'))
model.compile(loss='mean_squared_error', optimizer='Adam', metrics=['accuracy'])


# early_stopping = keras.callbacks.EarlyStopping(patience=6)
# reduce_lr = keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.2,
#                               patience=4, min_lr=0.001)


history = model.fit(
   x=X_train,
   y=y_train,
   epochs=5,
   batch_size=20,
   verbose=1,
   validation_split=0.2,
   # callbacks = [early_stopping, reduce_lr]
)

# %%

predictions = model.predict(x=X_test, verbose=1)
predictions = predictions.round()
cm = confusion_matrix(y_test.argmax(axis=1), predictions.argmax(axis=1))
cm

# %%
