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

x = np.load('/home/ezra/stonewalls/data/profiles/training_walls_flipped_balanced.npy')
y = np.load('/home/ezra/stonewalls/data/profiles/training_walls_labels_flipped_balanced.npy')
#%%
x = ml_utils.add_fixed_noise(x)
# %%
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.33)
X_train = np.array([np.array(x).astype('float32') for x in X_train])
X_test = np.array([np.array(x).astype('float32') for x in X_test])
X_train = X_train.reshape(X_train.shape[0], 51 , 1)
X_test = X_test.reshape(X_test.shape[0], 51, 1)

# %%
   
model = keras.Sequential()
model.add(layers.Conv1D(filters=100, kernel_size = 3, kernel_initializer='he_uniform', activation='relu', input_shape=(51,1)))
model.add(layers.Conv1D(filters=100, kernel_size = 3, kernel_initializer='he_uniform', activation='relu'))
model.add(layers.MaxPooling1D(pool_size=2))
model.add(layers.Flatten())
model.add(layers.Dropout(0.5))
model.add(layers.Dense(units=100, kernel_initializer='he_uniform', activation='relu'))
model.add(layers.Dense(units=100, kernel_initializer='he_uniform', activation='relu'))
model.add(layers.Dense(units = 2, activation='softmax'))
model.compile(loss='binary_crossentropy', optimizer='Adam', metrics=['accuracy'])


early_stopping = keras.callbacks.EarlyStopping(patience=6)
reduce_lr = keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.2,
                              patience=4, min_lr=0.001)

model.compile(optimizer='adam',
            loss="binary_crossentropy",
            metrics=['accuracy'],
            )

history = model.fit(
   x=X_train,
   y=y_train,
   epochs=50,
   batch_size=20,
   verbose=1,
   validation_split=0.2,
   callbacks = [early_stopping, reduce_lr]
)

# %%

predictions = model.predict(x=X_test, verbose=1)
predictions = predictions.round()
cm = confusion_matrix(y_test.argmax(axis=1), predictions.argmax(axis=1))
cm

