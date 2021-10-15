from re import T
import sys
from tkinter.constants import PROJECTING
import gdcm
import cv2 as cv
from PIL import Image
from skimage.color import gray2rgb
#from skimage import color
from skimage.util import img_as_ubyte,img_as_float
import tempfile
import pandas as pd
import math
import SimpleITK as sitk
from lmfit import Model
from class_dicom import ObjetoDicom
import os
import pydicom
import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt
from tkinter import filedialog
import imageio
from PIL.Image import fromarray
import skimage.color
import skimage.filters
import skimage.io
import rawMethods
from mpl_toolkits import mplot3d
import segmentation as seg
from pydicom.pixel_data_handlers.util import apply_modality_lut

#np.set_printoptions(threshold=sys.maxsize)

# Main #
def main(): 
    
    #Abrir variables
    Dcm_imagen = []
    matriz = []
    ImageNumber = 0
    #Abre cuadro de diálogo y pregunta path del forlder
    cuadro=tk.Tk()
    cuadro.withdraw()
    FolPath=filedialog.askdirectory(title="DICOM Images")
    
    #Warning si no se abre algún folder
    StringVacio=""

    if FolPath is StringVacio:
        print("Error: No seleccionó directorio.")
        sys.exit(0)
    
    for root,dirs,files in os.walk(FolPath):
        for i in files:
            #Toma las imagenes dycom
            if i.endswith(".dcm"):
                
                ImageNumber = ImageNumber + 1
                #Leer el path de cada imagen
                PathAux=os.path.join(root,i)
                Img1=ObjetoDicom()
                Img1.DescomDicom(PathAux)
                Dcm1=Img1.ReaderDicom(PathAux)
                #print(Dcm1)
                
                dcm = pydicom.dcmread(PathAux)
                Data_img=np.copy(dcm.pixel_array)  
                Dcm_imagen.append(Data_img)


                #print("Numéro de corte: " + str(ImageNumber))
                #print("Valores de pixeles: " + str(Data_img[200, 30]))
                #print("Valores de pixeles: " + str(Data_img[100, 100]))

                #houndfieldArray = apply_modality_lut((dcm.pixel_array), dcm)
                
                #Produce histogramas de las intensidades de cada toma

                #treshMatrix = rawMethods.thresholdMatrix(Data_img)

                #rawMethods.histogram2D(Data_img)
                
                #Produce 3 figuras comparativas CT/Mascara/Superposition

                rawMethods.imagePlots(Data_img, dcm)

                arrayHU = rawMethods.getHoundfieldArray(dcm)

                #print("Valores HU: " + str(arrayHU[100,100]))


                


    #(572,512) SAGITAL
    #(572,512) CORONAL

    Matrix3DVolumeIntensities= np.array(Dcm_imagen)

    #rawMethods.volumetricPlot(Matrix3DVolumeIntensities)

#    print(Matrix3DVolumeIntensities) ### SE MUERE TODITO SI IMPRIMIS ESTO

    print(Matrix3DVolumeIntensities.shape)
    print(type(Matrix3DVolumeIntensities))
    print(ImageNumber)

    ## SEGMENTACION
    size = Matrix3DVolumeIntensities.shape
    #contour = np.zeros((size[0],size[1],size[2]))

    # for i in range(ImageNumber):
        
    #     contour[i,:,:] = seg.get_contour(Matrix3DVolumeIntensities[i,:,:])

    # print(contour)


#Ejecuta función main() 
if __name__ == '__main__':
    main()
