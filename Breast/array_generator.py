#FUESMEN - Resonancia
#Autor: Rodrigo N. Alcalá M.


import pydicom as dicom
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import numpy as np
import operator
from class_dicom import ObjetoDicom
import SimpleITK as sitk
from myshow import *
import pandas as pd


# Genera los array de los dicoms correspondientes en forma de array y como objetos


class imagen:
    def __init__ (self, slice, img):
        self.slice = slice
        self.img = img


def array_generator():

    #Variables
    emptyString = ""
    imagesDicom = []
    positionList = []
    counter = 0
    # Crear cuadro de selección de archivos:
    # Iterar sobre cada archivo .dcm del archivo seleccionado:
    image_list, image_slices, pmesh, img_qtt, countmesh, result, dcm_im_all = [], [], [], 0, 0, 0, []
    # Carga las imágenes, genera lista de slice y genera objetos
    path = tk.Tk()
    path.withdraw()
    file_name = filedialog.askopenfilenames(title="Array Generator")
    for i in file_name:

        dcm = dicom.dcmread(i)
        #counter += 1
        image_list.append('imagen' + str(img_qtt))
        image_slices.append(dcm[0x0020,0x1041].value)

        image_list[img_qtt] = imagen(dcm[0x0020,0x1041].value, np.copy(dcm.pixel_array)) # Lista de objetos tipo image
        dcm_im_all.append(dcm.pixel_array)
        img_qtt = img_qtt + 1

        sorted_image_list  = sorted(image_list, key = operator.attrgetter('slice'))
        
    list_of_arrays = [o.img for o in sorted_image_list]
    
    array = np.dstack(list_of_arrays)
    shape = np.shape(array)
    cond = False
    if cond == True:
        for n in range(shape[2]):
            arr = array[:,:,n]
            img = sitk.GetImageFromArray(arr)
            myshow(img)
    
    generatedMatrix = np.copy(array)
    objectList = sorted_image_list
    # with open("mapKEP.npy","wb")  as a:
    #     np.save(a,generatedMatrix)
    return generatedMatrix,objectList

if __name__ == "__main__ ":
    array_generator()
#array_generator()