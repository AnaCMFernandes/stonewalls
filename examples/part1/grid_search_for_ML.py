#%%
import geopandas as gpd
import time
import os
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import datasets, layers, models
from tensorflow.keras.callbacks import ReduceLROnPlateau, EarlyStopping
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from scipy.stats import reciprocal
from sklearn.model_selection import RandomizedSearchCV

from sklearn.model_selection import GridSearchCV

from tensorflow.keras.wrappers.scikit_learn import KerasClassifier
# Function to create model, required for KerasClassifier

def create_model(kernel_initializer, optimizer, filters, units):
    # create model
    model = keras.Sequential()
    model.add(layers.Conv1D(filters=filters, kernel_size = 3, kernel_initializer=kernel_initializer, activation='relu', input_shape=(51,1)))
    model.add(layers.Conv1D(filters=filters, kernel_size = 3, kernel_initializer=kernel_initializer, activation='relu'))
    model.add(layers.MaxPooling1D(pool_size=2))
    model.add(layers.Flatten())
    model.add(layers.Dropout(0.5))
    model.add(layers.Dense(units=units[0], kernel_initializer=kernel_initializer, activation='relu'))
    model.add(layers.Dense(units=units[1], kernel_initializer=kernel_initializer, activation='relu'))
    model.add(layers.Dense(units = 2, activation='softmax'))
    model.compile(loss='binary_crossentropy', optimizer=optimizer, metrics=['accuracy'])
    return model
# fix random seed for reproducibility
seed = 7
np.random.seed(seed)
# load dataset

x = np.load('/home/ezra/stonewalls/data/profiles/training_walls.npy')
y = np.load('/home/ezra/stonewalls/data/profiles/training_walls_labels.npy')

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.33)
X_train = np.array([np.array(x).astype('float32') for x in X_train])
X_test = np.array([np.array(x).astype('float32') for x in X_test])
X_train = X_train.reshape(X_train.shape[0], 51 , 1)
X_test = X_test.reshape(X_test.shape[0], 51, 1)

# create model
model = KerasClassifier(build_fn=create_model, verbose=1)
# define the grid search parameters
param_grid = {
'batch_size' : [20],
'epochs' : [30],
'kernel_initializer' : ['he_uniform'],
'optimizer': ['Adam'],
'filters': [128, 64, 32],
'units': [[100,50], [100,100], [50, 50]]
}


grid = GridSearchCV(estimator=model, param_grid=param_grid, n_jobs=-1, cv=3)
grid_result = grid.fit(X_train, y_train)
# summarize results
print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))
means = grid_result.cv_results_['mean_test_score']
stds = grid_result.cv_results_['std_test_score']
params = grid_result.cv_results_['params']
for mean, stdev, param in zip(means, stds, params):
    print("%f (%f) with: %r" % (mean, stdev, param))
# %%
# 'Best: 0.972219 using {'batch_size': 20, 'epochs': 30, 'kernel_initializer': 'he_uniform', 'optimizer': 'Adam'}'