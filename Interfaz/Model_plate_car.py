
import os
import matplotlib.pyplot as plt
import cv2
import numpy as np
from imutils import paths
import PossibleChar
from keras.models import load_model
from keras.preprocessing.image import img_to_array

class IdentificadorCaracter(object):

    def checkIfPossibleChar(self,possibleChar):
        # this function is a 'first pass' that does a rough check on a contour to see if it could be a char,
        # note that we are not (yet) comparing the char to other chars to look for a group
        MIN_PIXEL_WIDTH = 10
        MIN_PIXEL_HEIGHT = 55
        MAX_PIXEL_HEIGHT = 110
        MIN_ASPECT_RATIO = 0.25
        MAX_ASPECT_RATIO = 1.0
        MIN_PIXEL_AREA = 1300

        if (possibleChar.intBoundingRectArea > MIN_PIXEL_AREA and
            possibleChar.intBoundingRectWidth > MIN_PIXEL_WIDTH and
            possibleChar.intBoundingRectHeight > MIN_PIXEL_HEIGHT and
            possibleChar.intBoundingRectHeight < MAX_PIXEL_HEIGHT and
            MIN_ASPECT_RATIO < possibleChar.fltAspectRatio and
            possibleChar.fltAspectRatio < MAX_ASPECT_RATIO):
            return True
        else:
            return False

    def findPossibleCharsInPlate(self,imgGrayscale, imgThresh):
        listOfPossibleChars = []                        # this will be the return value
        contours = []
        imgThreshCopy = imgThresh.copy()

                # find all contours in plate
        imgContours, contours, npaHierarchy = cv2.findContours(imgThreshCopy, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:                        # for each contour
            possibleChar = PossibleChar.PossibleChar(contour)

            if self.checkIfPossibleChar(possibleChar):              # if contour is a possible char, note this does not compare to other chars (yet) . . .
                listOfPossibleChars.append(possibleChar)       # add to list of possible chars

        return listOfPossibleChars

    def Conversor(self,ListaA,ListaB):
        if len(ListaA.shape)>=2:
            ListaA=ListaA[0][:]
        else:
            print('El arrego ya es unidimensional')
        np.set_printoptions(suppress=True)
        Resultado=[x for x in zip(ListaB,ListaA)  ]
        return (Resultado)


    def Modelo(self,placas):

        classLabels = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        model = load_model("NumerosLetras.hdf5")
        np.set_printoptions(suppress=True)

        Placa=cv2.imread(placas)
        #Preprocesar la imagen cargada
        Reescalada = cv2.resize(Placa,(315,160), interpolation = cv2.INTER_CUBIC)
        Copia=Reescalada.copy()
        PlacaChannel=cv2.split(Reescalada)
        gris = cv2.cvtColor(Reescalada, cv2.COLOR_BGR2GRAY)
        gris = cv2.GaussianBlur(gris, (7,7), 0)
        thresh = cv2.adaptiveThreshold(gris, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV, 25, 3)
        contours = []
        listOfPossibleCharsInPlate = self.findPossibleCharsInPlate(gris,thresh)
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
        aux = [None]*2
        for i in range(0, len(orden)):
            if i < len(orden)-1:
                if abs(orden[i+1] - orden[i])<=15:
                    contornos.pop(orden.index(max(orden[i+1],orden[i])))
                    orden.pop(orden.index(max(orden[i+1],orden[i])))
            else: break
        Predicciones=[]
        for c in contornos:
            X,Y,W,H = c
            roi=Copia[Y:Y+H, X:X+W]
            image = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            image = cv2.resize(image, (32, 32), interpolation=cv2.INTER_CUBIC)
            image = np.expand_dims(img_to_array(image), axis=0)
            image = np.array(image)
            image = image.astype("float") / 255.0
            pred_porc = model.predict(image, batch_size=12)
            Prediccion=pred_porc.astype("float")*100
            Temporal=self.Conversor(Prediccion,classLabels)
            Predicciones.append(Temporal)
            pred = model.predict(image, batch_size=12).argmax(axis=1)[0]
            predictions.append(classLabels[pred])
            cv2.rectangle(Reescalada, (X - 7, Y - 7),(X + W + 4, Y + H + 4),(255, 0, 0), 1)
            cv2.rectangle(Reescalada, (X-3, Y-17),(X + 15, Y ), (255, 0, 0), -1)
            cv2.putText(Reescalada,classLabels[pred], (X+2, Y-5),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255,255), 2)
        Reescalada=cv2.resize(Reescalada,(Placa.shape[1],Placa.shape[0]), interpolation = cv2.INTER_CUBIC)
        cv2.imwrite(str('image.jpg'), Reescalada)
        return predictions,Predicciones
