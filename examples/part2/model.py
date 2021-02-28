#%%
## Local path, change this.
yellow_follow = '/mnt/c/Users/EZRA/Documents/TOOLBOXES/yellow/lib/'


import sys; sys.path.append(yellow_follow) 
import pandas as pd
import ml_utils
import math
import time
import numpy as np
import os

np.set_printoptions(suppress=True)
os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'

from sqlalchemy import create_engine

from sklearn.model_selection import train_test_split

# Tensorflow
import tensorflow_addons as tfa
from tensorflow.keras import Model, Input
from tensorflow.keras.layers import Dense, BatchNormalization, Dropout, Dropout, Conv2D, MaxPooling2D, Flatten, Conv2DTranspose, Add
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, LearningRateScheduler
from tensorflow.keras.constraints import max_norm
from tensorflow.keras.utils import plot_model

folder = '../../data/ML/'

#%%
dtm = np.load(os.path.join(folder, "dtm.npy"))
walls = np.load(os.path.join(folder, "walls.npy"))
meta = pd.read_csv(os.path.join(folder, "metadata.csv"))
#%%
walls = (walls == 1).astype('uint8')
#%%
land_mask = np.swapaxes(meta[meta["land"] == 1].values, 0, 1)[0]
wall_mask = np.swapaxes(meta[meta["wall"] == 1].values, 0, 1)[0]    # Has a wall
no_wall_mask = np.swapaxes(meta[meta["wall"] == 2].values, 0, 1)[0] # Has _no_ wall
#%%
no_wall_mask.shape
#%%
wall_mask.shape
#%%
####REGRESSION

train = np.concatenate([dtm[wall_mask], dtm[no_wall_mask]])
truth = np.concatenate([meta.values[wall_mask], meta.values[no_wall_mask]])
truth = (np.swapaxes(truth, 0, 1)[2] == 1).astype('uint8')
#%%
train = ml_utils.add_rotations(train)
train.shape
#%%
truth = np.concatenate([truth, truth, truth, truth])
#%%
# Shuffle the dataset
shuffle_mask = np.random.permutation(len(truth))
train = train[shuffle_mask]
truth = truth[shuffle_mask]
#%%
X_train, X_test, y_train, y_test = train_test_split(train, truth, test_size=0.33, random_state=42)

#%%
X_train.shape
X_train = X_train.reshape(3521, 64, 64, 1)
#%%
X_test.shape
X_test = X_test.reshape(1735, 64, 64, 1)
#%%
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import datasets, layers, models
import matplotlib.pyplot as plt

model = keras.Sequential()

model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(64, 64, 1)))
# model.add(layers.GaussianNoise(1))
model.add(layers.MaxPooling2D((2, 2), strides=(2,2), padding = "SAME"))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2), strides=(2,2), padding = "SAME"))
model.add(layers.Conv2D(128, (3, 3), activation='relu'))
model.add(layers.Flatten())
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(1))
model.summary()

#%%

model.compile(optimizer='adam',
              loss='log_cosh',
              metrics=['accuracy'])
#%%
history = model.fit(X_train, y_train, epochs=10, 
                    validation_data=(X_test, y_test))

#%%
plt.plot(history.history['accuracy'], label='accuracy')
plt.plot(history.history['val_accuracy'], label = 'val_accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.ylim([0.5, 1])
plt.legend(loc='lower right')

test_loss, test_acc = model.evaluate(X_test,  y_test, verbose=2)
#%%
model.evaluate(X_test, y_test)
# %%
