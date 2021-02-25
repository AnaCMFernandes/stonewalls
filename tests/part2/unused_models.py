# model = models.Sequential()
# model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(64, 64, 1)))
# model.add(layers.MaxPooling2D((2, 2), strides=(2,2), padding = "VALID"))
# model.add(layers.Conv2D(64, (3, 3), activation='relu'))
# model.add(layers.MaxPooling2D((2, 2), strides=(2,2), padding = "VALID"))
# model.add(layers.Conv2D(128, (3, 3), activation='relu'))
# model.add(layers.Flatten())
# model.add(layers.Dense(64, activation='relu'))
# model.add(layers.Dense(1))
# model.summary()

# from functools import partial
# DefaultConv2D = partial(keras.layers.Conv2D,
# kernel_size=3, activation='relu', padding="SAME")
# model = keras.models.Sequential([
# DefaultConv2D(filters=64, kernel_size=7, input_shape=[64, 64, 1]),
# keras.layers.MaxPooling2D(pool_size=2),
# DefaultConv2D(filters=128),
# DefaultConv2D(filters=128),
# keras.layers.MaxPooling2D(pool_size=2),
# DefaultConv2D(filters=256),
# DefaultConv2D(filters=256),
# keras.layers.MaxPooling2D(pool_size=2),
# keras.layers.Flatten(),
# keras.layers.Dense(units=128, activation='relu'),
# keras.layers.Dropout(0.5),
# keras.layers.Dense(units=64, activation='relu'),
# keras.layers.Dropout(0.5),
# keras.layers.Dense(units=1, activation='softmax'),
# ])
