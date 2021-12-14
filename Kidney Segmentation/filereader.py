import os
import pydicom as dicom
import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt
from tkinter import filedialog
import sys
import cv2
import shutil
import PIL
from PIL import Image

import skimage.data as data
import skimage.segmentation as seg
import skimage.filters as filters
import skimage.draw as draw
import skimage.color as color
from skimage import measure
from sklearn import cluster
from class_dicom import ObjetoDicom

from scipy.ndimage.filters import gaussian_filter


def intialMask(pixelArray):
    mask = np.copy(pixelArray)
    shape = np.shape(mask)
    #shape = list(shape)
    #print(shape)
    for m in range(shape[0]):
        for n in range(shape[1]):
            if mask[m][n] <= -200:
                mask[m][n] = 1000
            if 0 <= mask[m][n] <= 60:
                pass
            if mask[m][n] > 60:
                mask[m][n] = 0
    return mask


def getHoundfieldArray(dcm):
    arrayHU = (dcm.pixel_array*dcm.RescaleSlope) + dcm.RescaleIntercept
    return arrayHU


def arraySlicing(array):
    slicedArray = array[250:400,75:425]
    print(np.shape(slicedArray))
    return slicedArray


def basicPlots(arrayHU, maskedArray, slicedArray):
    fig = plt.figure(figsize=(20, 20))
    fig.add_subplot(212)
    plt.imshow(arrayHU, cmap=plt.cm.bone)
    fig.add_subplot(221)
    plt.imshow(maskedArray, cmap=plt.cm.bone)
    fig.add_subplot(222)
    plt.imshow(slicedArray, cmap=plt.cm.bone)
    plt.show()


def main():

    emptyString = ""
    imagesDicom = []
    counter = 0 
    mean = []
    cuadroDirectorio = tk.Tk()
    cuadroDirectorio.withdraw()
    folderPath = filedialog.askdirectory(title="DICOM Images")
    #jpgPath = filedialog.askdirectory(title="Directorio de jpg")
    if folderPath is emptyString:
        print("Error: No seleccionó directorio.")
        sys.exit(0)

    for root,dirs,files in os.walk(folderPath):
        for i in files:
            if i.endswith(".dcm"):
                counter += 1
                filePath = os.path.join(root,i)
                Img1 = ObjetoDicom()
                Img1.DescomDicom(filePath)
                ds = dicom.dcmread(filePath)
                pixelArray = ds.pixel_array
                #print(ds.PatientID)
                #print(pixelArray[250][250])
                #Dcm1 = Img1.ReaderDicom(filePath)
                
                #pixelArray2 = 255 * pixelArray / pixelArray.max()
                imageData = np.copy(pixelArray)
                imagesDicom.append(imageData)

                arrayHU = getHoundfieldArray(ds)
                mask = intialMask(arrayHU)
                maskedArray = np.multiply(arrayHU, mask)
                print(counter)

                blurred = gaussian_filter(maskedArray, sigma=1.1)
                slicedArray = arraySlicing(maskedArray)
                mean = np.mean(slicedArray)
                
                #basicPlots(arrayHU, maskedArray, slicedArray)
                if 2500.0 < mean < 5000.0:
                    figure = plt.figure(figsize=(25,25))
                    figure.add_subplot(111)
                    plt.imshow(slicedArray,cmap=plt.cm.bone)
                    plt.show()
                    print(mean)
                else:
                    pass
                
                

    #print(ds)
main()



