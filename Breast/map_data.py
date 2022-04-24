#FUESMEN - Resonancia
#Autor: Rodrigo N. Alcalá M.


import pydicom as dicom
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import numpy as np
import sys
import os
from class_dicom import ObjetoDicom
import SimpleITK as sitk

from array_generator import array_generator


def arrayslicer(array,leftVal,rightVal):
    array = array[:,:,leftVal:rightVal]
    return array


def mapCollector():

    leftVal = 50
    rightVal = 102

    print("KTRANS")
    mapKTRANS,ktranslist = array_generator()
    mapKTRANS = arrayslicer(mapKTRANS,leftVal,rightVal)
    print(np.shape(mapKTRANS))
    with open("mapKTRANS.npy","wb") as a:
        np.save(a,mapKTRANS)
    
    print("KEP")
    mapKEP,keplist = array_generator()
    mapKEP = arrayslicer(mapKEP,leftVal,rightVal)
    with open("mapKEP.npy","wb") as b:
        np.save(b,mapKEP)
    
    print("VE")
    mapVE,velist = array_generator()
    mapVE = arrayslicer(mapVE,leftVal,rightVal)
    with open("mapVE.npy","wb") as c:
        np.save(c,mapVE) 
      
    print("IAUGC")
    mapIAUGC,iaugclist = array_generator()
    mapIAUGC = arrayslicer(mapIAUGC,leftVal,rightVal)
    with open("mapIAUGC.npy","wb") as d:
        np.save(d,mapIAUGC)
    
    print("CER")
    mapCER,cerlist = array_generator()
    mapCER = arrayslicer(mapCER,leftVal,rightVal)
    with open("mapCER.npy","wb") as e:
        np.save(e,mapCER)
    
    print("BAT")
    mapBAT,batlist = array_generator()
    mapBAT = arrayslicer(mapBAT,leftVal,rightVal)   
    with open("mapBAT.npy","wb") as f:
        np.save(f,mapBAT)
    
    print("MaxSlope")
    mapMaxSlope,maxslopelist = array_generator()
    mapMaxSlope = arrayslicer(mapMaxSlope,leftVal,rightVal)
    with open("mapMaxSlope.npy","wb") as g:
        np.save(g,mapMaxSlope)

    #return mapKTRANS,mapKEP,mapVE,mapIAUGC,mapCER,mapBAT,mapMaxSlope
mapCollector()