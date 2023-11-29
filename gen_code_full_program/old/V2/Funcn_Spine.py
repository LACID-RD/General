#from operator import contains
#import cmath
#import matplotlib.pyplot as plt
#from numpy.lib.npyio import save
#from skimage.io import imread, imsave
#import pydicom
#import tkinter as tk
#from tkinter import filedialog
#from pydicom.uid import generate_uid
#from scipy.optimize import least_squares, minpack2
#import gdcm
#import os
#import cv2 as cv
#from PIL import Image
#from skimage.color import gray2rgb
#from skimage import color
#from skimage.util import img_as_ubyte,img_as_float
#import math
#import SimpleITK as sitk
#import pandas as pd
#from Class_Study import CStudy
#from Class_Serie import CSerie
#from Class_Image import CImage
#import matplotlib.pyplot as Htt
import csv
import matplotlib.pyplot as plt
import numpy as np
import sys
### Local libraries
from main import PATH_HOME
sys.path.insert(0, PATH_HOME)
from Class_LoadI import CLoadI
import Funcn_Proce
import Funcn_QAPro

#############################
#############################
# Funciones Spine
#############################
#############################
# Identificacion de series
###################
# SagT1(0), SagT2(1), SagStir(3) y AxT2 a los discos

def FS_series_ident(AllStud):
    sag_t1 = sag_t2 = sag_stir = ax_gre = -2

    # Series identification
    for i, ser in enumerate(AllStud.AllSers):
        if ser.S12AcPl == 1:
            if ser.S11MRCo == 15: sag_t1 = i
            elif ser.S11MRCo == 20: sag_t2 = i
            elif ser.S11MRCo == 30: sag_stir = i
        elif ser.S12AcPl == 0 and ser.S11MRCo == 20: 
            ax_gre = i
    # QA
    if min(sag_t1, sag_t2, sag_stir, ax_gre) < -1:
        raise ValueError("Error: No se encuentran las secuencias necesarias (FSSer).")
    sag_array = [sag_t1, sag_t2, sag_stir]
    val_qa, min_res_sag = AllStud.CYGeoSrQA(sag_array)

    if val_qa == 1:
        raise ValueError("Error: Geometria no coincide en los sagitales (FSSer).")
    return sag_array, min_res_sag, ax_gre

###################
# Segmenta Sagitales
###################

def FSSegmSag(AllStud, SrArrSg, MinRsSg, resolution):
    offSetV=100; sag_t1=SrArrSg[0]; sag_t2=SrArrSg[1]; sag_stir=SrArrSg[2]
    sSTsT1c=500

    #Histogramas para detectar minimos y maximos
    t1_newSr = AllStud.CY_new_serie(sag_t1,MinRsSg,-1,0) # Redimensiona T1, se coloca en la serie -1
    T1Junto = AllStud.AllSers[t1_newSr].CSUneSres() # Se unen todas las imagenes           
    varBin1,T1Histo = Funcn_Proce.FP_hist_analysis(T1Junto,resolution, 1, 0, 0, 0)
    T1maxId = np.argmax(T1Histo[offSetV:])+offSetV # Maximo valor de hist sin contar el offSet
    T1minId = np.argmin(T1Histo[:T1maxId]) # Maximo valor de hist sin contar el offSet
    #print("T1min-max:",T1minId,T1maxId)
    t2_newSr = AllStud.CY_new_serie(sag_t2,MinRsSg,-2,0) # Redimensiona T2, se coloca en la serie -2
    T2Junto = AllStud.AllSers[t2_newSr].CSUneSres() # Se unen todas las imagenes           
    varBin2, T2Histo=Funcn_Proce.FP_hist_analysis(T2Junto,resolution, 1, 0, 0, 0)
    T2maxId = np.argmax(T2Histo[offSetV:])+offSetV # Maximo valor de hist sin contar el offSet
    T2minId = np.argmin(T2Histo[:T2maxId]) # Maximo valor de hist sin contar el offSet
    #print("T2min-max:",T2minId,T2maxId)

    #Primera segmentacion, ruido y tejido blando (T1 y T2)
    shapeMx = AllStud.AllSers[t1_newSr].AllImag[0].ImgData.shape
    '''
    for i in range(len(AllStud.AllSers[t1_newSr].AllImag)):
        for j in range(shapeMx[0]): 
            for k in range(shapeMx[1]):
                if AllStud.AllSers[t1_newSr].AllImag[i].ImgData[j,k]<T1minId:
                    AllStud.AllSers[t1_newSr].AllImag[i].ImgData[j,k] = 0
                else:
                    if AllStud.AllSers[t2_newSr].AllImag[i].ImgData[j,k]<T2minId:
                        AllStud.AllSers[t1_newSr].AllImag[i].ImgData[j,k] = 3
                    else: AllStud.AllSers[t1_newSr].AllImag[i].ImgData[j,k] = 1
    '''
    # Convert the image data to numpy arrays for efficient computation
    T1_img_data = np.array([img.ImgData for img in AllStud.AllSers[t1_newSr].AllImag])
    T2_img_data = np.array([img.ImgData for img in AllStud.AllSers[t2_newSr].AllImag])
    # Create masks based on the conditions
    mask_T1 = T1_img_data < T1minId
    mask_T2 = T2_img_data < T2minId
    # Apply the conditions using numpy's where function
    T1_img_data = np.where(mask_T1, 0, np.where(mask_T2, 3, 1))
    # Assign the modified data back to the original structure
    for i, img in enumerate(AllStud.AllSers[t1_newSr].AllImag):
        img.ImgData = T1_img_data[i]

    #Segunda segmentacion, CSF (STIR-T1)
    AllStud.CYRmSerie(0, t2_newSr) # Se borra serie -2
    a1_newSr = AllStud.CY_new_serie(sag_stir, sag_t1, -2, 2) # Resta STIR menos T1
    AllStud.AllSers[a1_newSr].CSImgTrns(resolution, 1, 1) # Transformada exponencial
    A1Junto = AllStud.AllSers[a1_newSr].CSUneSres() # Se unen todas las imagenes
    varBin3,A1Histo = Funcn_Proce.FP_hist_analysis(A1Junto, resolution, 1, 0, 0, 0)

    for i in range(len(AllStud.AllSers[t1_newSr].AllImag)):
        for j in range(shapeMx[0]): 
            for k in range(shapeMx[1]):
                #if i[j,k]==1:
                if AllStud.AllSers[a1_newSr].AllImag[i].ImgData[j,k] > sSTsT1c:
                    AllStud.AllSers[t1_newSr].AllImag[i].ImgData[j,k] = 5
                else: pass
        #plt.imshow(AllStud.AllSers[t1_newSr].AllImag[i].ImgData,cmap=plt.cm.bone)
        #plt.title('i-pos'); plt.show()

    ###############
    # Manipula Ax-Gre
    ###############

def FS_axt2a_manp(AllStud, SrArrSg, ax_gre, resolution):

    t1_newSr = AllStud.SeNuLst.index(-2)
    AllStud.CY_serGeo_proj(t1_newSr, ax_gre, -3)
    #Funcn_QAPro.FQA_class(2) #QA POO
    Funcn_QAPro.FQA_series(AllStud, 0) # QA
