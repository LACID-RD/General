'''
    Breast IVIM Image Preprocessing, two step method
    Authors: Trinidad González
    Daniel Fino
    Rodrigo Alcalá
    Nicolás Moyano Brandi
    Federico González
'''

from operator import contains
import cmath
import matplotlib.pyplot as plt
from numpy.lib.npyio import save
from skimage.io import imread, imsave
import pydicom
import tkinter as tk
from tkinter import filedialog
import numpy as np
from pydicom.uid import generate_uid
from scipy.optimize import least_squares, minpack2
import gdcm
import sys
import cv2 as cv
from PIL import Image
from skimage.color import gray2rgb
from skimage import color
from skimage.util import img_as_ubyte,img_as_float
import math
import SimpleITK as sitk
import pandas as pd
from Class_Study import CStudy
from Class_Image import CImage

#################################################
#################################################
#####################  Define funcion principal
#################################################
#################################################
def main():
    fileAcq=[]
    geometry=[]
    linePat=int(sys.argv[1])
    pathFol=sys.argv[2]
    
    ########### LEE ARCHIVO PACIENTES Y CARGAN VARIABLES EXTERNAS
    #ImagePosition en las imágenes axiales de mama se incrementa en
    #sentido FH (caudal-craneal), EN SENTIDO INVERSO AL VMPACS
    #Tanto el archivo Pacientes.xlsx como las carpetas con
    #las imagenes deben estar en esta carpeta:
    path_basic=pathFol+"/Images/"
    path_name="Pacientes.xlsx"
    path_files=path_basic+path_name
    TablaFull=pd.read_excel(path_files,header=0)
    fileAcq.append(TablaFull["Key"].tolist())
    fileAcq.append(TablaFull["X1"].tolist())
    fileAcq.append(TablaFull["Y1"].tolist())
    fileAcq.append(TablaFull["X2"].tolist())
    fileAcq.append(TablaFull["Y2"].tolist())
    fileAcq.append(TablaFull["Slices"].tolist())
    path_key=fileAcq[0][linePat]
    path_full=path_basic+path_key         #path_full: path a la carpeta del paciente
    selSlice=fileAcq[5][linePat]
    geometry.append(fileAcq[1][linePat])
    geometry.append(fileAcq[2][linePat])
    geometry.append(fileAcq[3][linePat])
    geometry.append(fileAcq[4][linePat])

    ########### Analisis de ima de DWI, crea mapas IVIM
    Img1=CImage()
    Std=CStudy(path_full)
    sec=1                       #1:DWI, 2:PWI
    Std.load_img(geometry)
    print("-Termina carga de imagenes DWI, inicia su organización")
    Img1=Std.Sec_read(Img1,sec)
    Std.DWI_org()
    zSlPo=Std.DWI_sliPo(selSlice)
    Img1=Std.fit_mngnt(path_full,Img1)

    ########### Analisis de ima. PWI
    print("-Inicia carga y organizacion de imagenes PWI")
    Img2=CImage()
    sec=2
    Img2=Std.Sec_read(Img2,sec)
    Std.PWI_org(zSlPo)


#################################################
##################### Ejecuta función main()
#################################################

if __name__ == '__main__':
    main()
