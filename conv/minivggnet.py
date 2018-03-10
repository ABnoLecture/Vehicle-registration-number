from keras.models import Sequential
from keras.layers.normalization import BatchNormalization
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.layers.core import Activation
from keras.layers.core import Flatten
from keras.layers.core import Dropout
from keras.layers.core import Dense
from keras import backend as k
'''
###############################################################################
Estructura de la red minivggnet modificada, agregando:
"[CONV->RELU->BN->CONV->RELU->BN->POOL->DP]", la original solo cuenta con dos
segmentos como el anterior.
INPUT->[CONV->RELU->BN->CONV->RELU->BN->POOL->DP](x3)->FC->RELU->
BN->DP->FC->SOFTMAX
###############################################################################
'''
class MiniVGGNet:
    @staticmethod
    def build(w, h, d, c):
        model = Sequential()
        inputShape = (h, w, d)
        chanDim = -1
        if k.image_data_format() == "channels_first":
            inputShape = (d, h, w)
            chanDim = 1
        model.add(Conv2D(32, (3,3), padding="same", input_shape=inputShape))
        model.add(Activation("relu"))
        model.add(BatchNormalization(axis=chanDim))
        model.add(Conv2D(64, (3,3), padding="same"))
        model.add(Activation("relu"))
        model.add(BatchNormalization(axis=chanDim))
        model.add(MaxPooling2D(pool_size=(2,2)))#Strides o "pasos" de (1,1)
        model.add(Dropout(0.25))
        model.add(Conv2D(64, (3,3), padding="same"))
        model.add(Activation("relu"))
        model.add(BatchNormalization(axis=chanDim))
        model.add(Conv2D(64, (3,3), padding="same"))
        model.add(Activation("relu"))
        model.add(BatchNormalization(axis=chanDim))
        model.add(MaxPooling2D(pool_size=(2,2)))
        model.add(Dropout(0.25))
        model.add(Conv2D(128, (3,3), padding="same"))
        model.add(Activation("relu"))
        model.add(BatchNormalization(axis=chanDim))
        model.add(Conv2D(128, (3,3), padding="same"))
        model.add(Activation("relu"))
        model.add(BatchNormalization(axis=chanDim))
        model.add(MaxPooling2D(pool_size=(2,2)))
        model.add(Dropout(0.25))
        model.add(Flatten())
        model.add(Dense(512))
        model.add(Activation("relu"))
        model.add(BatchNormalization())
        model.add(Dropout(0.5))
        model.add(Dense(c))
        model.add(Activation("softmax"))#softmax
        return model
