import cv2
class SimplePreprocessor:
    """docstring for SimplePreprocessor."""
    def __init__(self, width, heigth, inter=cv2.INTER_AREA):
        #Se le asigna un valor de alto, ancho e interpolacion
        self.width = width
        self.height = heigth
        self.inter = inter

    def preprocess(self, image):
# resize the image to a fixed size, ignoring the aspect
# ratio

        if image is not None :
            return  cv2.resize(image, (self.width, self.height),
                    interpolation=self.inter)
