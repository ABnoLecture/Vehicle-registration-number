import numpy as np
import cv2
import os
class SimpleDatasetLoader:
    def __init__(self, preprocessors=None):
        self.preprocessor = preprocessors
        # si preprocessor es None,se inicializa como una lista vacia
        if self.preprocessor is None:
            self.preprocessor = []

    def load(self, imagePaths, verbose=-1, gray=0):
        # se inicia la lista de caracteristicas y etiquetas
        data = []
        labels = []
        #un for para agregar las imagenes
        for (i, imagePath) in enumerate(imagePaths):
            image = cv2.imread(imagePath)
            (w,h,c) = image.shape
            if gray == 1 and c>2:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            label = imagePath.split(os.path.sep)[-2]
                #Revisamos si preprocessors no es None
            if self.preprocessor is not None:
                for p in self.preprocessor:
                    image = p.preprocess(image)

            data.append(image)
            labels.append(label)
            if verbose > 0 and i > 0 and (i + 1) % verbose == 0 :
                print("[INFO] processed {}/{}".format( i + 1,
                        len(imagePaths)))
        return (np.array(data),np.array(labels))
