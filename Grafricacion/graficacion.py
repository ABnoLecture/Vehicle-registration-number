import matplotlib.pyplot as plt
import numpy as np
def figura(epocas, H, save=False,ruta=None):
    plt.style.use("ggplot")
    plt.figure()
    plt.plot(np.arange(0, epocas), H.history["loss"], label="train_loss")
    plt.plot(np.arange(0, epocas), H.history["val_loss"], label="val_loss")
    plt.plot(np.arange(0, epocas), H.history["acc"], label="train_acc")
    plt.plot(np.arange(0, epocas), H.history["val_acc"], label="val_acc")
    plt.title("Training Loss and Accuracy")
    plt.xlabel("Epoch #")
    plt.ylabel("Loss/Accuracy")
    plt.legend()
    if save: plt.savefig(ruta)
    else: plt.show()
