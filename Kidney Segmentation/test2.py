#!/usr/bin/env python
# coding: utf-8

import pydicom as dicom
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import numpy as np
import sys
import gdcm
import os
import shutil
import skimage.data as data
import skimage.segmentation as seg
import skimage.filters as filters
import skimage.draw as draw
import skimage.color as color
from skimage import measure
from sklearn import cluster
from class_dicom import ObjetoDicom
from scipy.ndimage.filters import gaussian_filter
import SimpleITK as sitk
import scipy.ndimage
from sklearn.cluster import KMeans
from glob import glob
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from skimage import morphology
from skimage.transform import resize
from plotly import __version__
from plotly.tools import FigureFactory as FF
from plotly.graph_objs import *
from gui import *
from myshow import myshow, myshow3d
import pandas as pd
from numba import jit,cuda,vectorize,njit
def getHoundfieldArray(dcm):
    arrayHU = (dcm.pixel_array*dcm.RescaleSlope) + dcm.RescaleIntercept
    return arrayHU
# def volHUMatrixGenerator():

#     #Variables
#     emptyString = ""
#     imagesDicom = []
#     counter = 0
#     mean = []
#     volumetricHUMatrix = []

#     # Crear cuadro de selección de archivos:
#     cuadroDirectorio = tk.Tk()
#     cuadroDirectorio.withdraw()
#     folderPath = filedialog.askdirectory(title="DICOM Images")
#     if folderPath is emptyString:
#         print("Error: No seleccionó directorio.")
#         sys.exit(0)

#     # Iterar sobre cada archivo .dcm del archivo seleccionado:
#     for root, dirs, files in os.walk(folderPath):
#         for i in files:
#             if i.endswith(".dcm"):

#                 counter += 1
#                 filePath = os.path.join(root, i)
#                 Img1 = ObjetoDicom()
#                 Img1.DescomDicom(filePath)
#                 ds = dicom.dcmread(filePath)
#                 pixelArray = ds.pixel_array
                
#                 imageData = np.copy(pixelArray)
#                 imagesDicom.append(imageData)

#                 #Obtener array matricial de U° HoundsField
#                 arrayHU = getHoundfieldArray(ds)

#                 # Variables de resampling:
#                 sliceThickness = ds.SliceThickness
#                 pixelSpacing = ds.PixelSpacing

#                 # Generar matriz volumetrica en HU
#                 aux = np.copy(arrayHU)
#                 volumetricHUMatrix.append(aux)
#                 image = sitk.GetImageFromArray(arrayHU)
#                 #seriesArray = sitk.GetArrayViewFromImage(image)
#                 print(ds.ImagePositionPatient)
#     print("Patient ID = " + str(ds.PatientID))
#    # vol_HU_matrix = volumetricHUMatrix
#     #print(np.shape(vol_HU_matrix))

#     return image
# volHUMatrixGenerator()


