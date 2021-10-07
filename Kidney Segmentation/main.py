from re import T
import sys
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

np.set_printoptions(threshold=sys.maxsize)

# Main #

def main(): 
    
    #Abrir variables
    Dcm_imagen = []

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
                #Leer el path de cada imagen
                PathAux=os.path.join(root,i)
                Img1=ObjetoDicom()
                Img1.DescomDicom(PathAux)
                Dcm1=Img1.ReaderDicom(PathAux)
                print(Dcm1)
                
                dcm = pydicom.dcmread(PathAux)
                Data_img=np.copy(dcm.pixel_array)  
                Dcm_imagen.append(Data_img)
                
                #Generar la imagen
                #plt.imshow(Data_img, cmap = plt.cm.bone)
                #plt.title("Imágen")
                #plt.show()  
                
                # HACER HISTOGRAMA DE TRESHOLD ??
            
                n, bins, patches = plt.hist(dcm.pixel_array, 64, density=True, fc="b", ec="k")
                plt.ylim([0,0.08])
                plt.xlim([0,1250])
                plt.title("Intensity Histogram")
                plt.show()

                # MASCARA 
                image = skimage.io.imread(fname=Data_img)
                skimage.io.imshow(image)
                
                blur = skimage.color.rgb2gray(image)
                blur = skimage.filters.gaussian(blur, sigma=1.0)
                
                t = skimage.filters.threshold_otsu(blur)
                mask = blur > T
                
                skimage.io.imshow(mask)
                
                sel = np.zeros_like(image)
                sel[mask] = image[mask]
                skimage.io.imshow(sel)



    print(Data_img)
    print(type(Data_img))


#Ejecuta función main() 
if __name__ == '__main__':
    main()
