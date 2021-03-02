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
from scipy.stats import reciprocal
from sklearn.model_selection import RandomizedSearchCV


yellow_follow = '/mnt/c/Users/EZRA/Documents/TOOLBOXES/yellow/lib/'
import sys; sys.path.append(yellow_follow)
import ml_utils

input_path = '/home/ezra/stonewalls/data/profiles/cross_sections_aeroe_final.geojson'

gdf = gpd.read_file(input_path)


### CREATE LABELS
labels = gdf['type']
labels = labels.map({'0': 0, '1': 1, '2': 1, '3': 1 }).to_numpy()
counts = ml_utils.count_freq(labels)
mask = ml_utils.minority_class_mask(labels, counts[0][1])
labels = labels[mask]
labels = keras.utils.to_categorical(
    labels, num_classes=2, dtype='float32'
)

geom = gdf['geometry']
geom = geom[mask]
profiles = geom.apply((lambda x: np.array([(p.z) for p in x]).astype('float32')))
profiles = np.stack(profiles.values)

profiles_flipped = np.array([np.flip(f) for f in profiles])

x = np.concatenate([profiles, profiles_flipped])
x = ml_utils.add_fixed_noise(x)
y = np.concatenate([labels,labels])

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.33)
X_train = np.array([np.array(x).astype('float32') for x in X_train])
X_test = np.array([np.array(x).astype('float32') for x in X_test])
X_train = X_train.reshape(X_train.shape[0], 51 , 1)
X_test = X_test.reshape(X_test.shape[0], 51, 1)

def build_model(kernel_initializer="glorot_uniform", optimizer='Adam', n_hidden=1, filters=32, n_neurons=30, learning_rate=3e-3, dropout = 0.2, kernel_size = 3, input_shape=(51,1), activation="relu"):

   model = keras.models.Sequential()
   options = {"input_shape": input_shape}

   model.add(layers.Conv1D(filters=filters, kernel_size = kernel_size, kernel_initializer=kernel_initializer, activation=activation, input_shape=(51,1)))
   model.add(layers.Conv1D(filters=filters, kernel_size = kernel_size, kernel_initializer=kernel_initializer, activation=activation))
   model.add(layers.MaxPooling1D(pool_size=2))
   model.add(layers.Flatten())
   model.add(layers.Dropout(0.33))
   model.add(layers.Dense(units=n_neurons, kernel_initializer=kernel_initializer, activation=activation))
   model.add(layers.Dense(units=n_neurons, kernel_initializer=kernel_initializer, activation=activation))
   model.add(layers.Dense(units = 2, activation='softmax'))

   options = {}
   model.add(keras.layers.Dense(2, **options))
   optimizer = keras.optimizers.SGD(learning_rate)
   model.compile(loss="mse", optimizer=optimizer)
   return model

keras_reg = keras.wrappers.scikit_learn.KerasRegressor(build_model)

keras_reg.fit(X_train, y_train, epochs=30,
validation_split=0.3,
callbacks=[keras.callbacks.EarlyStopping(patience=10)])
mse_test = keras_reg.score(X_test, y_test)
y_pred = keras_reg.predict(X_test)

param_distribs = {
    "activation" :["relu", "swish", "mish", "tanh", "elu"],
    "optimizer" : ['SGD', 'RMSprop', 'Adagrad', 'Adadelta', 'Adam', 'Adamax', 'Nadam'],
    "kernel_initializer" : ['glorot_normal', 'glorot_uniform', 'he_normal', 'he_uniform'],
    "filters" : [16, 32, 64, 128],
    "kernel_size" : [3,5],
    "dropout" : [0.2, 0.33, 0.5],
    "n_neurons": np.arange(1, 100),
    "learning_rate": reciprocal(3e-4, 3e-2),
}

rnd_search_cv = RandomizedSearchCV(keras_reg, param_distribs, n_iter=10, cv=3)
rnd_search_cv.fit(X_train, y_train, epochs=30,
validation_split=0.3,
callbacks=[keras.callbacks.EarlyStopping(patience=10)])

print(rnd_search_cv.best_params_)
model = rnd_search_cv.best_estimator_.model
model.save("./models/best_model.h5")