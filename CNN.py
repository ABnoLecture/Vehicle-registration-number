#-*- coding: utf-8 -*-
'''
Código encargado de la creación, compilación, entrenamiento y prueba de un
modelo de una red convolucional para la identificación de caracteres de una
 matricula vehicular colombiana.
'''

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelBinarizer
import matplotlib.pyplot as plt
import cv2
from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import SGD
from preprocessing.imagetoarraypreprocessor import ImageToArrayPreprocessor
from preprocessing.simplepreprocessor import SimplePreprocessor
from datasets.SimpleDatasetLoader import SimpleDatasetLoader
from conv import MiniVGGNet
from imutils import paths
import numpy as np
from Grafricacion import graficacion

data  =[]
epocas = 100

print("[INFO] preprocessing images ...")
imagePaths = list(paths.list_images("NumerosLetras"))
sp = SimplePreprocessor(32, 32, inter=cv2.INTER_CUBIC)
iap = ImageToArrayPreprocessor()
sdl = SimpleDatasetLoader(preprocessors=[sp,iap])
(data, labels) = sdl.load(imagePaths, gray=1)
data = data.astype("float") / 255.0
lb = LabelBinarizer()
classLabels = ['0','1','2','3','4','5','6',
'7','8','9','A','B','C','D','E','F',
'G','H','I','J','K','L','M','N','O','P','Q',
'R','S','T','U','V','W','X','Y','Z']

print("[INFO] partition data ...")
(trainX, testX, trainY, testY) = train_test_split(data, labels, test_size=0.2,
                random_state=45)
trainY = lb.fit_transform(trainY)
testY = lb.fit_transform(testY)
aug = ImageDataGenerator(rotation_range=30, width_shift_range=0.1,
	height_shift_range=0.1, shear_range=0.2, zoom_range=0.2,
	horizontal_flip=True, fill_mode="nearest")
opt = SGD(lr = 0.01, decay=0.01 / epocas, momentum=0.9, nesterov=True)
model = MiniVGGNet.build(w=32,h=32, d=1, c=36)

print("[INFO] compiling network...")
model.compile(loss="categorical_crossentropy", optimizer=opt,
        metrics=["accuracy"])

print("[INFO] training network...")
H = model.fit_generator(aug.flow(trainX, trainY),
    validation_data=(testX, testY),steps_per_epoch=len(trainX) / 12,
        epochs=epocas, verbose=1)
model.save("modelo/NumerosLetras_prueba.hdf5")

print("[INFO] evaluating network...")
predictions = model.predict(testX, batch_size=12)
print(classification_report(testY.argmax(axis=1),
predictions.argmax(axis=1),target_names=[str(x) for x in lb.classes_]))
graficacion.figura(epocas, H, save=True, ruta="Entrenamiento.jpg")
