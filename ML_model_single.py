import pickle
import numpy as np
from matplotlib import pylab as plt
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten, BatchNormalization
from keras.layers import Conv2D, MaxPooling2D
from keras.utils import to_categorical
from keras.preprocessing.image import ImageDataGenerator
from load_data import load_data
from utilities import one_hot
import keras.backend as K

import psutil
learning_rate = 0.001
batch_size = 32
epochs = 100
print("batch size: ", batch_size, ", learning rate: ", learning_rate, ", epochs: ", epochs)
decay=0
x_data, y_data = load_data(roof=None)
print("x_data max: ", np.max(x_data))
rand_index = np.random.permutation(x_data.shape[0])

x_data = x_data[rand_index]
y_data = y_data[rand_index]

split_index = int(x_data.shape[0]*0.9)

x_train = x_data[:split_index]
y_train = y_data[:split_index]

x_test = x_data[split_index:]
y_test = y_data[split_index:]


print(x_train.shape[0], 'train samples')
print(x_test.shape[0], 'test samples')
num_classes=15
# Convert class vectors to binary class matrices.
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)
x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255

print('x_train shape:', x_train.shape)
print('y_train shape:', y_train.shape)
print('x_test shape:', x_test.shape)
print('y_test shape:', y_test.shape)



def construct_model():
    model = Sequential()
    model.add(Conv2D(32, (3, 3), padding='same',
                 input_shape=[100,100,4]))
    model.add(Activation('relu'))
    model.add(Conv2D(32, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Conv2D(64, (3, 3), padding='same'))
    model.add(Activation('relu'))
    model.add(Conv2D(64, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(512))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(num_classes))
    model.add(Activation('softmax'))

    opt = keras.optimizers.Adam(learning_rate=learning_rate, decay=decay)
    # opt = keras.optimizers.SGD(learning_rate=learning_rate, decay=decay)

    # Let's train the model using RMSprop
    model.compile(loss='categorical_crossentropy',
                       optimizer=opt,
                       metrics=['accuracy'])

    return model


class ML_model:

    def __init__(self):
        self.model = construct_model()
        self.save_as = 'MLmodel'

    def load_model(self):
        self.model = keras.models.load_model(self.save_as + '.hdf5')

    def predict(self, x_data):
        # predict
        return self.model.predict(x_data)


    def train(self, x_train, y_train, x_test, y_test, epochs=10, batch_size=50, data_augmentation=True):

        mcp_save = keras.callbacks.ModelCheckpoint(self.save_as + '.hdf5',
                                                   save_best_only=True,
                                                   monitor='val_loss',
                                                   mode='min')



        if not data_augmentation:
            print('Not using data augmentation.')
            self.model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, validation_split=0.1)
        else:
            print('Using real-time data augmentation.')
            # This will do preprocessing and realtime data augmentation:
            datagen = ImageDataGenerator(
                featurewise_center=False,  # set input mean to 0 over the dataset
                samplewise_center=False,  # set each sample mean to 0
                featurewise_std_normalization=False,  # divide inputs by std of the dataset
                samplewise_std_normalization=False,  # divide each input by its std
                zca_whitening=False,  # apply ZCA whitening
                zca_epsilon=1e-06,  # epsilon for ZCA whitening
                rotation_range=0,  # randomly rotate images in the range (degrees, 0 to 180)
                # randomly shift images horizontally (fraction of total width)
                width_shift_range=0.1,
                # randomly shift images vertically (fraction of total height)
                height_shift_range=0.1,
                shear_range=0.,  # set range for random shear
                zoom_range=0.,  # set range for random zoom
                channel_shift_range=0.,  # set range for random channel shifts
                # set mode for filling points outside the input boundaries
                fill_mode='nearest',
                cval=0.,  # value used for fill_mode = "constant"
                horizontal_flip=True,  # randomly flip images
                vertical_flip=False,  # randomly flip images
                # set rescaling factor (applied before any other transformation)
                rescale=None,
                # set function that will be applied on each input
                preprocessing_function=None,
                # image data format, either "channels_first" or "channels_last"
                data_format=None,
                validation_split=0.1)

            # Compute quantities required for feature-wise normalization
            # (std, mean, and principal components if ZCA whitening is applied).
            datagen.fit(x_train)

            # Fit the model on the batches generated by datagen.flow().
            history = self.model.fit_generator(datagen.flow(x_train, y_train, batch_size=batch_size),
                                         epochs=epochs,
                                         validation_data=(x_test, y_test),
                                         workers=4,
                                         callbacks=[mcp_save])


            return history


M = ML_model()
M.train(x_train, y_train, x_test, y_test)