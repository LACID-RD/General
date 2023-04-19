#FUESMEN - Resonancia
#Autor: Rodrigo N. Alcalá M.


import pydicom as dicom
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import numpy as np
import operator
#from class_dicom import ObjetoDicom
import SimpleITK as sitk
from myshow import *
import pandas as pd
import os
import cv2 as cv
from scipy.signal import convolve2d
# Genera los array de los dicoms correspondientes en forma de array y como objetos


class Study:
    def __init__ (self, slice, img, cardPhase, path):
        self.slice = slice
        self.img = img
        self.cardPhase = cardPhase
        self.path = path
    
    def crop_array(self, arr, roi):
        x1, x2, y1, y2 = int(roi[0]), int(roi[1]), int(roi[2]), int(roi[3])
        crop = arr[y1:int(y1 + y2), x1:int(x1 + x2)]
        return crop
    
        
    def gradients_IxIy(self, arr, size):
        #3x3
        #Ix
        ker1 = np.array([[0, 0, 0],
                        [0, -1, 1],
                        [0, 0, 0]])
        #Iy    
        ker2 = np.array([[0, 0, 0],
                        [0, -1, 0],
                        [0, 1, 0]])
        #5x5
        #Ix
        ker3 = np.array([[0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0],
                        [0, 0, -1, 1, 1],
                        [0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0]])
        #Iy
        ker4 = np.array([[0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0],
                        [0, 0, -1, 0, 0],
                        [0, 0, 1, 0, 0],
                        [0, 0, 1, 0, 0]])
        
        if size == 3:
            Ix = convolve2d(arr, ker1, mode='same')
            Iy = convolve2d(arr, ker2, mode='same')
        if size == 5:
            Ix = convolve2d(arr, ker3, mode='same')
            Iy = convolve2d(arr, ker4, mode='same')       
        
        #gradients = (Ix, Iy)
        
        return Ix, Iy
    
    def normalize_image(self, arr):
        img = sitk.GetImageFromArray(arr)
        #img = sitk.Cast(img, sitk.sitkFloat32)
        n = sitk.NormalizeImageFilter()
        normalize = n.Execute(img)
        normalize = sitk.GetArrayFromImage(normalize)
        
        return normalize







def laplacian(arr):
    laplace = cv.Laplacian(arr, cv.CV_64F, ksize=3)
    return laplace


def sobel_filter(arr):
    #Sobel
    image = sitk.GetImageFromArray(arr)
    sobelFilter = sitk.SobelEdgeDetectionImageFilter()
    float_image =  sitk.Cast(image, sitk.sitkFloat32)
    sobelEdge = sitk.SobelEdgeDetection(float_image)

    sobel = sitk.GetArrayFromImage(sobelEdge)
    return sobel


def array_generator_cardio():

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
    file_name = filedialog.askopenfilenames(title="Cardio")
    
    for i in file_name:
        
        path = os.path.abspath(i)
        dcm = dicom.dcmread(i)
        #counter += 1
        image_list.append('imagen' + str(img_qtt))
        image_slices.append(dcm[0x0020, 0x1041].value)
        
        #laplace = laplacian(dcm.pixel_array)
        #sobel = sobel_filter(dcm.pixel_array)
        
        image_list[img_qtt] = Study(dcm[0x0020, 0x1041].value, np.copy(dcm.pixel_array),
                                    dcm[0x0018, 0x1090].value, path) # Lista de objetos tipo image
        
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
    return generatedMatrix, objectList


if __name__ == "__main__ ":
    array_generator_cardio()
#array_generator()