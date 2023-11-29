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
import matplotlib.pyplot as plt
#import numpy as np
#import os
from pathlib import Path
import sys
import time
#Constantes
PATH_HOME = "C:/Users/Daniel/Documents/IT/Python/SRC/V3/"
RESOLUTION = 2048
sys.path.insert(0, PATH_HOME)
# Local libraries
from Class_LoadI import CLoadI
import Funcn_Proce
import Funcn_QAPro
import Funcn_Spine


#############################
#############################
# Define main function
#############################
#############################

def main():
    start_time = time.time()
    #linePat=int(sys.argv[1]); pathFol=sys.argv[2]
    # Get the current working directory
    path_main = Path.cwd()
    Funcn_Proce.FP_main_path(path_main)
    path_lumbar = "C:/Users/Daniel/Documents/IT/Python/Images/Lumbar"
    
    # Abre y organiza estudio
    Img1 = CLoadI(RESOLUTION)
    Img1.CL_load_img(path_main, path_lumbar) # Carga header DCM
    if len(Img1.Studies) > 1.5:
        raise ValueError("Error: Se ingreso mas de un estudio.")
    Img1.CL_img_order(-2)  # Ordena imagenes y carga matrices
    #Img1.CL_img_matrix()  # Carga en matrices las imagenes
    Img1.AllStud[0].CYPrtInfo() # Imprime info de la serie
    open_time = time.time()
    print("Load time:",open_time - start_time)
    Funcn_QAPro.FQA_class(0) #QA POO
    #Funcn_QAPro.FQA_series(Img1.AllStud[0], 0) # QA
    
    '''
    # Segmentacion de imagenes
    print("\nSegmentando imagenes sagitales")
    SrArrSg,MinRsSg,aT2 = Funcn_Spine.FS_series_ident(Img1.AllStud[0]) #Identifica series
    Funcn_Spine.FSSegmSag(Img1.AllStud[0], SrArrSg, MinRsSg, RESOLUTION) #Segmenta sagitales
    sag_time = time.time()
    print("Segm time:",sag_time - open_time)
    Funcn_QAPro.FQA_class(0) #QA POO
    print("Incorporando Axial GRE")
    Funcn_Spine.FS_axt2a_manp(Img1.AllStud[0], SrArrSg, aT2, RESOLUTION) #Ax-Gre
    '''
#############################
#############################
# Run main() function
#############################
#############################

if __name__ == '__main__':
    main()
    __author__ = 'Daniel Fino <dfinov85@gmail.com>'
    __version__ = "1.0.0"
