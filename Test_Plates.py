'''Codigo Encargado de la segmentacion y prueba del modelo entrenado
para el reconocimiento de caracteres en una matricula vehicular '''
from keras.models import load_model
from keras.preprocessing.image import img_to_array
import os
import matplotlib.pyplot as plt
import cv2
import numpy as np
from imutils import paths
import pandas as pd
import PossibleChar
from skimage import morphology
np.set_printoptions(suppress=True)
print("[INFO] loading model...")
model = load_model("modelo/NumerosLetras.hdf5")
# Variables que determinan las proporciones de un caracter en un matricula
# vehicular.
MIN_PIXEL_WIDTH = 10
MIN_PIXEL_HEIGHT = 55
MAX_PIXEL_HEIGHT = 110
MIN_ASPECT_RATIO = 0.25
MAX_ASPECT_RATIO = 1.0
MIN_PIXEL_AREA = 1300

classLabels = ['0', '1', '2', '3', '4', '5', '6', '7', '8',
'9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
def checkIfPossibleChar(possibleChar):
    # Funcion encargada de determinar si los contornos de la imagen
    # estan entre los limites establecidos para un caracter.
    if (possibleChar.intBoundingRectArea > MIN_PIXEL_AREA and
        possibleChar.intBoundingRectWidth > MIN_PIXEL_WIDTH and
        possibleChar.intBoundingRectHeight > MIN_PIXEL_HEIGHT and
        possibleChar.intBoundingRectHeight < MAX_PIXEL_HEIGHT and
        MIN_ASPECT_RATIO < possibleChar.fltAspectRatio and
        possibleChar.fltAspectRatio < MAX_ASPECT_RATIO):
        return True
    else:
        return False

def findPossibleCharsInPlate(imgGrayscale, imgThresh):
    # Funcion encargada de seleccionar los contornos que contienen caracteres
    # en la imagen.
    listOfPossibleChars = []
    contours = []
    imgThreshCopy = imgThresh.copy()
    imgContours, contours, npaHierarchy = cv2.findContours(imgThreshCopy,
                    cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        possibleChar = PossibleChar.PossibleChar(contour)

        if checkIfPossibleChar(possibleChar):
            listOfPossibleChars.append(possibleChar)

    return listOfPossibleChars
# Si se desea probar toda las imagenes deja la linea 59, de lo
# contrario descomentar la linea 60
imagePath = list(paths.list_images("Placas"))
# print(imagePath)
# imagePath = np.random.choice(imagePath, size=(10,),replace=False)
for placas in imagePath:
    Placa=cv2.imread(placas)
    #Preprocesar la imagen cargada
    Reescalada = cv2.resize(Placa,(315,160), interpolation = cv2.INTER_CUBIC)
    Copia=Reescalada.copy()
    gris = cv2.cvtColor(Reescalada, cv2.COLOR_BGR2GRAY)
    gris = cv2.GaussianBlur(gris, (7,7), 1)
    thresh = cv2.adaptiveThreshold(gris, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                            cv2.THRESH_BINARY_INV, 25, 3)
    contours = []
    listOfPossibleCharsInPlate = findPossibleCharsInPlate(gris,thresh)
    for possibleChar in listOfPossibleCharsInPlate:
            contours.append(possibleChar.contour)
    predictions, orden, contornos = [], [], []
# Desde aqui hasta la linea 89 se da el procedimiento de como ordenar los
# caracteres de la matricula vehicular y como eliminar los falsos positivos.
    for c in (contours):
        [X,Y,W,H]=cv2.boundingRect(c)
        orden.append(X)
        contornos.append([X,Y,W,H])
    orden = sorted(orden)
    contornos = sorted(contornos)
    aux = [[None,None]]*4
    for i in range(0, len(orden)):
        if i < len(orden)-1:
            if np.abs(orden[i] - orden[i+1])<=13:
                contornos.pop(orden.index(max(orden[i+1],orden[i])))
                orden.pop(orden.index(max(orden[i+1],orden[i])))
        else: break
    for c in contornos:

        X,Y,W,H = c
        roi=Copia[Y:Y+H, X:X+W]
        image = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        image = cv2.resize(image, (32, 32), interpolation=cv2.INTER_AREA)
        image = np.expand_dims(img_to_array(image), axis=0)
        image = np.array(image)
        image = image.astype("float") / 255.0
        pred_porc = model.predict(image, batch_size=12)
        print("Procentaje de prediccion: ",pred_porc*100)
        pred = model.predict(image, batch_size=12).argmax(axis=1)[0]
        predictions.append(classLabels[pred])
        cv2.rectangle(Reescalada, (X - 7, Y - 7),(X + W + 4, Y + H + 4),
                                (255, 0, 0), 1)
        cv2.rectangle(Reescalada, (X-3, Y-17),(X + 15, Y ), (255, 0, 0), -1)
        cv2.putText(Reescalada,classLabels[pred], (X+2, Y-5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255,255), 2)

    print("Placa",predictions)

    cv2.imshow("Caracter ",Reescalada)
    cv2.waitKey(0)
