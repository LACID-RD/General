#FUESMEN - Resonancia
#Autor: Rodrigo N. Alcalá M.


import numpy as np
import tkinter as tk
from tkinter import filedialog
import pydicom as dicom
from array_generator import array_generator
from myshow import *
from scipy.stats.stats import pearsonr 
#Encuentra la posicion z del mapa de ivim y luego busca la imágen 
# de la perfu más cercana en z.


def ivim_z_localizator():

    print("Seleccionar el mapa de IVIM a comparar")
    #file_name = filedialog.askopenfilenames(title="IVIM MAP")
    
    ivimarray, ivimMapObject = array_generator()

    ivimZLoc = [obj.slice for obj in ivimMapObject]
    ivimZLoc = ivimZLoc[0]
    
    return ivimarray, ivimMapObject, ivimZLoc
#ivim_z_localizator()


def perfu_locator():
    imshow = False
    ivimArray, ivimMapObject, ivimZLoc = ivim_z_localizator()
    #print(ivimZLoc)
    print("Select the perfution files")
    array, objList = array_generator()

    closeImage = [obj for obj in objList if abs(obj.slice - ivimZLoc) < 0.25]
    imageList = [obj.img for obj in closeImage]
    im = closeImage[0]
    #print(im.slice)
    if imshow == True:
        for image in imageList:
            img = sitk.GetImageFromArray(image)
            myshow(img)

    #print(len(closeImage))
    #print(len(imageList))

    #print(closeImage)
    return ivimMapObject,closeImage
#perfu_locator()


def final_comparator(x1,x2,y1,y2):
    
    ivim,pharma = perfu_locator()

    ivimArr = ivim[0].img
    ivimArr = ivimArr[x1:x2,y1:y2]
    print(np.shape)
    ivimArr = ivimArr.flatten()

    pharmaArray = pharma[0].img
    pharmaArray = pharmaArray[x1:x2,y1:y2]
    pharmaArray = pharmaArray.flatten()
    
    coef = pearsonr(ivimArr,pharmaArray)
    print("Coeficiente de Correlación: ")
    return coef

#final_comparator()