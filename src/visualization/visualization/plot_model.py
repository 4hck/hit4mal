from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras import backend as K
import os
from shutil import copyfile
import shutil
import sys
import keras


# helper
location = lambda x: os.path.join(
    os.path.dirname(os.path.realpath(__file__)), x)


# MODEL SETTING
img_width, img_height = 150, 150


trained_model_file = location('../weights_files/weights.best.bigru_3conv_7.hdf5')
visualize_inputs = './visualize_inputs'

def build_model():
    """
    return a myterious model
    """

    if K.image_data_format() == 'channels_first':
        input_shape = (3, img_width, img_height)
    else:
        input_shape = (img_width, img_height, 3)

    model = Sequential()
    model.add(Conv2D(32, (3, 3), input_shape=input_shape))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(32, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(64, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Flatten())

    # FC layer
    model.add(Dense(64))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1))
    model.add(Activation('sigmoid'))

    model.compile(loss='binary_crossentropy',
                  optimizer='adadelta',
                  metrics=['accuracy'])

    return model


if __name__ == '__main__':
    model = build_model()
    model.load_weights(trained_model_file)

    from quiver_engine import server
    server.launch(model, input_folder=visualize_inputs)
