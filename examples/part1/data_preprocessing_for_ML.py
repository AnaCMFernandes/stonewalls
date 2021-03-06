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

input_path = '/home/ezra/stonewalls/data/profiles/geojson/full_profiles_classbypeak_05032021.geojson'
output_folder = '/home/ezra/stonewalls/data/profiles/npy'


gdf = gpd.read_file(input_path)
labels = gdf['type']
geom = gdf['geometry']
profiles = geom.apply((lambda x: np.array([(p.z) for p in x]).astype('float32')))

# %%
## STANDARD DATASET UNBALANCED

# labels_numpy = labels.map({'0': 0, '1': 1, '2': 1, '3': 1 }).to_numpy()
# y = keras.utils.to_categorical(
#     labels, num_classes=52, dtype='float32'
# )

x = np.stack(profiles.values)
y = labels
np.save(os.join(output_folder,'training_by_peak_walls.npy'), x)
np.save(os.join(output_folder,'training_by_peak_walls_labels.npy'), y)
### CREATE LABELS
# %%

### CREATE DATASET FLIPPED

labels_numpy = labels.map({'0': 0, '1': 1, '2': 1, '3': 1 }).to_numpy()

y = keras.utils.to_categorical(
    labels_numpy, num_classes=2, dtype='float32'
)

profiles = np.stack(profiles.values)

profiles_flipped = np.array([np.flip(f) for f in profiles])

x = np.concatenate([profiles, profiles_flipped])
y = np.concatenate([y,y])

np.save('/home/ezra/stonewalls/data/profiles/training_walls_flipped.npy', x)
np.save('/home/ezra/stonewalls/data/profiles/training_walls_labels_flipped.npy', y)
# %%

### CREATE DATASET BALANCED(MINORITY CLASS)

labels_numpy = labels.map({'0': 0, '1': 1, '2': 1, '3': 1 }).to_numpy()

counts = ml_utils.count_freq(labels_numpy)
mask = ml_utils.minority_class_mask(labels_numpy, counts[0][1])

labels_numpy = labels_numpy[mask]
profiles = profiles[mask]
y = keras.utils.to_categorical(
    labels_numpy, num_classes=2, dtype='float32'
)

x = np.stack(profiles.values)

np.save('/home/ezra/stonewalls/data/profiles/training_walls_balanced.npy', x)
np.save('/home/ezra/stonewalls/data/profiles/training_walls_labels_balanced.npy', y)
#%%
### CREATE DATASET FLIPPED BALANCED(MINORITY CLASS)

labels_numpy = labels.map({'0': 0, '1': 1, '2': 1, '3': 1 }).to_numpy()

counts = ml_utils.count_freq(labels_numpy)
mask = ml_utils.minority_class_mask(labels_numpy, counts[0][1])
labels_numpy = labels_numpy[mask]
profiles = profiles[mask]
y = keras.utils.to_categorical(
    labels_numpy, num_classes=2, dtype='float32'
)

profiles = np.stack(profiles.values)

profiles_flipped = np.array([np.flip(f) for f in profiles])

x = np.concatenate([profiles, profiles_flipped])
y = np.concatenate([y,y])

np.save('/home/ezra/stonewalls/data/profiles/training_walls_flipped_balanced.npy', x)
np.save('/home/ezra/stonewalls/data/profiles/training_walls_labels_flipped_balanced.npy', y)

# %%

# %%
