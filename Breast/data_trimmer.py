#FUESMEN - Resonancia
#Autor: Rodrigo N. Alcalá M.

import numpy as np
import tkinter as tk
from tkinter import filedialog
import pydicom as dicom
from array_generator import array_generator
from myshow import *
from perfu_locator import perfu_locator


#Sirve para generar un ROI manual croppeando un array
def array_trimmer(array, x0, x1, y0, y1):
    arr = np.copy(array)
    crop = arr[x0:x1,y0:y1,:]
    return crop

if __name__ == "__main__ ":
    array_generator()