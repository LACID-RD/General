import pydicom as dicom
import tkinter as tk
from tkinter import filedialog
import numpy as np
import operator
import SimpleITK as sitk
#from myshow import *
import os
import cv2 as cv
from scipy.signal import convolve2d


class Study:
    def __init__ (self, slice, img, path, bvalue, imgPerBvalue):
        self.slice = slice
        self.img = img
        self.path = path
        self.bvalue = bvalue
        self.imgPerBvalue = imgPerBvalue


def obj_loader():

    #Variables
    emptyString = ""
    imagesDicom = []
    positionList = []
    counter = 0
   
    # Crear cuadro de selección de archivos:
    # Iterar sobre cada archivo .dcm del archivo seleccionado:
    image_list, image_slices, img_qtt, dcm_im_all = [], [],  0, []
    
    # Carga las imágenes, genera lista de slice y genera objetos
    path = tk.Tk()
    path.withdraw()
    file_name = filedialog.askopenfilenames(title="Select DWI images")
    
    for i in file_name:
        
        path = os.path.abspath(i)
        dcm = dicom.dcmread(i)
        #counter += 1
        image_list.append('imagen' + str(img_qtt))
        image_slices.append(dcm[0x0020, 0x1041].value)
        
        image_list[img_qtt] = Study(dcm[0x0020, 0x1041].value, np.copy(dcm.pixel_array),
                                    path, dcm[0x0043,0x1039].value, dcm[0x0021,0x104F].value) # Lista de objetos tipo image
        
        dcm_im_all.append(dcm.pixel_array)
        img_qtt = img_qtt + 1

        sorted_image_list  = sorted(image_list, key = operator.attrgetter('slice'))
        
    list_of_arrays = [o.img for o in sorted_image_list]
    
    array = np.dstack(list_of_arrays)
    shape = np.shape(array)
    
    cond = False
    
    # if cond == True:
    #     for n in range(shape[2]):
    #         arr = array[:, :, n]
    #         img = sitk.GetImageFromArray(arr)
    #         myshow(img)
    
    generatedMatrix = np.copy(array)
    objectList = sorted_image_list
    
    return generatedMatrix, objectList


if __name__ == "__main__ ":
    obj_loader()