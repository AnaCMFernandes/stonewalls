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
y = types.map({'0': 0, '1': 1, '2': 1, '3': 1 }).tolist()
y = keras.utils.to_categorical(
    y, num_classes=2, dtype='float32'
)
# %%
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import datasets, layers, models
import matplotlib.pyplot as plt

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.33)

import numpy as np

X_train = np.array(X_train).astype('float32')
X_train = X_train.reshape(139726, 51)
X_test = np.array(X_test).astype('float32')
X_test = X_test.reshape(68821, 51)
y_train = np.array(y_train).astype('uint8')
y_test = np.array(y_test).astype('uint8')

# %%

model = keras.Sequential()


model.add(layers.Dense(units=64, activation='relu', input_shape=(51,)))
model.add(layers.Dense(units=32, activation='relu'))
model.add(layers.Dense(units = 2, activation='softmax'))
model.summary()

model.compile(optimizer='adam',
              loss="binary_crossentropy",
              metrics=['accuracy'])

#%%
history = model.fit(X_train, y_train, epochs=10, 
                    validation_data=(X_test, y_test))

# %%
predictions = model.predict(x=X_test, verbose=1)
predictions = predictions.round()
# %%
import itertools

def plot_confusion_matrix(cm, classes, normalize=False, title='Confusion matrix', cmap=plt.cm.Blues):
   plt.imshow(cm, interpolation='nearest', cmap=cmap)
   plt.title(title)
   plt.colorbar()
   tick_marks = np.arange(len(classes))
   plt.xticks(tick_marks, classes, rotation=45)
   plt.yticks(tick_marks, classes)

   if normalize:
      cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
      print("Normalized confusion matrix")
   else:
      print("Confusion matrix, without normalization")

   print(cm)

   thresh = cm.max() /2.

   for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
      plt.text(j, i, cm[i, j], horizontalalignment="center", color="white" if cm[i, j] > thresh else "black"
      )
   
   plt.tight_layout()
   plt.ylabel('True label')
   plt.xlabel('Predicted label')

cm_plot_labels = ['no_wall', 'wall']

from sklearn.metrics import confusion_matrix



cm = confusion_matrix(y_test.argmax(axis=1), predictions.argmax(axis=1))
plot_confusion_matrix(cm=cm, classes=cm_plot_labels, title='Confusion Matrix')
#
# %%
