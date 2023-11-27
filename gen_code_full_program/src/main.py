# from operator import contains
# import cmath
# import matplotlib.pyplot as plt
# from numpy.lib.npyio import save
# from skimage.io import imread, imsave
# import pydicom
# import tkinter as tk
# from tkinter import filedialog
# from pydicom.uid import generate_uid
# from scipy.optimize import least_squares, minpack2
# import gdcm
# import cv2 as cv
# from PIL import Image
# from skimage.color import gray2rgb
# from skimage import color
# from skimage.util import img_as_ubyte,img_as_float
# import math
# import SimpleITK as sitk
# import pandas as pd
# from Class_Study import CStudy
# from Class_Serie import CSerie
# from Class_Image import CImage
# import matplotlib.pyplot as Htt
import matplotlib.pyplot as plt

# import numpy as np
# import os
from pathlib import Path
import sys
import time

# Constantes
PATH_SRC = "/home/daniel/Documents/FAuto/SRC"
RESOLUTION = 2048
sys.path.insert(0, PATH_SRC)
# Local libraries
from Class_LoadI import ClassLoadImage
import Funcn_Proce

# import Funcn_QAPro


#############################
#############################
# Define main function
#############################
#############################


def main():
    start_time = time.time()
    # Get the current working directory
    path_main = Path.cwd()
    # Genera error.log
    Funcn_Proce.fp_error_log(path_main)

    # Abre y organiza estudio
    Img1 = ClassLoadImage(RESOLUTION)
    Img1.CL_load_img(0, 0)  # Carga header DCM
    if len(Img1.Studies) > 1.5:
        raise ValueError("Error: Se ingreso mas de un estudio.")
    # Img1.CL_img_order(-2)  # Ordena imagenes y carga matrices
    Img1.CL_img_matrix()  # Carga en matrices las imagenes
    Img1.AllStud[0].CYPrtInfo()  # Imprime info de la serie
    for i in Img1.AllStud[0].AllSers:
        if i.S10AdTy == "3D" and i.SLa11MR == "GRE-T1" and i.SLa12Ac == "Ax":
            print(i.pathFol)
    # open_time = time.time()
    # print("Load time:",open_time - start_time)
    # Funcn_QAPro.FQA_class(0) #QA POO
    # Funcn_QAPro.FQA_series(Img1.AllStud[0], 0) # QA


#############################
#############################
# Run main() function
#############################
#############################

if __name__ == "__main__":
    main()
    __author__ = "Daniel Fino <dfinov85@gmail.com>"
    __version__ = "1.0.0"
