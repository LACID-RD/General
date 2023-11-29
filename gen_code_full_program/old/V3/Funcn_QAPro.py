#from inspect import CO_ITERABLE_COROUTINE
#from operator import contains
#import cmath
#from numpy.lib.npyio import save
#from skimage.io import imread, imsave
#import tkinter as tk
#from tkinter import filedialog
#from pydicom.uid import generate_uid
#import collections
#from scipy.optimize import least_squares, minpack2
#import math
#from lmfit import Model
#from lmfit import Parameters,minimize,fit_report
#from scipy.signal import lfilter, lfilter_zi, filtfilt, butter
#from matplotlib.pyplot import plot, legend, show, grid, figure, savefig
import matplotlib.pyplot as plt
import numpy as np
import sys
### Local libraries
from Class_Image import CImage
from Class_LoadI import CLoadI
from Class_Serie import CSerie
from Class_Study import CStudy
LINE_FLUSH = '\r\033[K'
UP_FRONT_LINE = '\033[F'

#############################
#############################
# QA Functions
#############################
#############################
# Print: series info and image of half
###################

def FQA_SerieInfo_Half(series):

    print(f"{series.S02SeNu} SlTk: {series.S04SlTk}, Mat: {series.S04RwNb}x{series.S04ClNb}, PiSp: {series.S04PiSp}")
    mid_index = len(series.AllImag) // 2
    title = series.AllImag[mid_index].CIFTitles(0)
    plt.imshow(series.AllImag[mid_index].ImgData, cmap=plt.cm.bone)
    plt.title(title)
    plt.show()

###################
# Series analysis
###################

def FQA_process_study(study, series_indices):
    print("QA_Study:", study.StuItem, "Cantidad de series:", len(series_indices), end="")
    if len(series_indices) == len(study.AllSers):
        print(" (Todas)")
    else: print("\n")
    for index in series_indices:
        FQA_SerieInfo_Half(study.AllSers[index])

###################
# Series QA
###################
# Se pueden colocar arrays de estudios y/o series
# Si serie_array=0, se analizan todas las series

def FQA_series(study_array,serie_array):
    if isinstance(study_array,np.ndarray): # Si study_array es un array...
        for study in study_array:
            if isinstance(serie_array, np.ndarray): # Si serie_array es un array...
                FQA_process_study(study, serie_array)
            elif serie_array==0: # Todas las series
                FQA_process_study(study, range(len(study.AllSers)))
            else: print("Error: No paso QA (FQASer)."); sys.exit(0)
    else:
        if isinstance(serie_array,np.ndarray): # Pero serie_array es un array...
            FQA_process_study(study_array, serie_array)
        elif serie_array==0:
            FQA_process_study(study_array, range(len(study_array.AllSers)))
        else: print("Error: No paso QA (FQASer)."); sys.exit(0)
    print("End QA_Study")

###################
# QA over libraries POO de las librerias
###################
#level_info: 0(no imprime), 1(Img), 2(Serie)

def FQA_class(level_info):
    qa_var = [0,0]; var_aux0 = []
    for i, image in enumerate(CImage.Instanc):
        var_aux0.append(image)
        if level_info == 1:
            print(i, " Stu:", image.StuItem, " Ser:", image.SerItem, " Num:", image.D02SeNu, " Cont:", image.D11MRCo, " Pln:", image.D12AcPl)

    # Study: Features within a study
    for i, study in enumerate(CStudy.Instanc):
        if len(study.AllSers) != len(study.SeNuLst):
            qa_var = [1, i]
            break    
    
    # Series: The images in all series match all image objects
    var_suma = 0; var_aux1 = []
    for i, serie in enumerate(CSerie.Instanc):
        var_aux1.append(serie)
        if level_info == 2:
            print(i, " Stu:", serie.StuItem, " Ser:", serie.SerItem, " Num:", serie.S02SeNu, " Img:", len(serie.AllImag))
        var_suma += len(serie.AllImag)
        # Dimension of the images
        if serie.AllImag[0].ImgData.shape != (serie.S04RwNb, serie.S04ClNb):
            qa_var = [2, 0]
    if len(CImage.Instanc) != var_suma:
        qa_var = [2, 1]

    # Images
    for i, serie in enumerate(CSerie.Instanc):
        v_count0 = sum((obj.StuItem == serie.StuItem and obj.S02SeNu == CStudy.Instanc[serie.StuItem].SeNuLst[serie.SerItem]) for obj in var_aux1)
        if v_count0 != 1: qa_var = [3, i]
        v_count1 = len(serie.AllImag)
        v_count2 = sum((img.StuItem == serie.StuItem and img.SerItem == serie.SerItem and img.D02SeNu == serie.S02SeNu) for img in var_aux0)
        if v_count1 != v_count2:
            qa_var = [4, i]
    
    # Closure
    if qa_var[0]==0: print("QA approved")
    else:
        print("Error: Problemas con objetos de una clase (FQABC). Code:",qa_var); sys.exit(0)


#############################
#############################
# Convenciones
#############################
#############################
# Rows and Columns: en DICOM Rows es en X y Columns en Y
# https://dicom.innolitics.com/ciods/rt-dose/image-plane/00280030
# en python 
#
# ImageOrientation e ImagePosition, bien explicado
# https://cds.ismrm.org/protected/18MProceedings/PDFfiles/5652.html
#