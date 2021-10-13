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
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits import mplot3d
np.set_printoptions(threshold=sys.maxsize)


def getHoundfieldArray(dcm):

    arrayHU = (dcm.pixel_array*dcm.RescaleSlope) + dcm.RescaleIntercept
    
    return arrayHU


def thresholdMatrix(Data_img):
    
    treshold = Data_img.copy()
    
    treshold[treshold < 1000] = 0
    treshold[treshold > 1100] = 0

    return treshold


def binaryArray(houndfieldArray):

    binaryArray = houndfieldArray.copy()

    binaryArray[binaryArray >= 20] = 1
    binaryArray[binaryArray > 40] = 0
    binaryArray[binaryArray < 20] = 0

    array = binaryArray

    return array


def houndfieldMask(houndfieldArray):

    mask = binaryArray(houndfieldArray)

    mask[mask >= 20] = 1000
    mask[mask > 40] = 0
    mask[mask < 20] = 0

    return mask



def imagePlots(Data_img, dcm):

    treshold = thresholdMatrix(Data_img)
    arrayHU = getHoundfieldArray(dcm)
    
    fig = plt.figure(figsize=(15, 15))

    fig.add_subplot(1, 4, 1)
    plt.imshow(Data_img, cmap="gray", vmin=0, vmax=255)
    plt.axis("off")
    plt.title("W/O Threshold")

    fig.add_subplot(1, 4, 2)
    plt.imshow(treshold, cmap="gray", vmin=0, vmax=255)
    plt.title("With Treshold")
    plt.axis("off")
#cmap=plt.cm.bone
    fig.add_subplot(1, 4, 3)
    superPositionData = np.multiply(Data_img, treshold)
    plt.imshow(superPositionData, cmap="gray", vmin=0, vmax=255)
    plt.title("Superposition")
    plt.axis("off")
    
    fig.add_subplot(1, 4, 4)
    plt.imshow(arrayHU, cmap="gray", vmin=0, vmax=255)
    plt.title("Houndfield Mask")
    plt.axis("off")

    plt.show()


def histogram2D(Data_img):

    n, bins, patches = plt.hist(Data_img, "sqrt", density=True, fc="b", ec="k")

    plt.ylim([0,0.08])
    plt.xlim([0,1250])
    plt.title("Intensity Histogram")

    plt.show()


#Grafica arrays 3d de Numpy
def volumetricPlot(matrix):

    fig = plt.figure()
    #z, x, y = matrix
    ax = fig.add_subplot(111, projection="3d")
    ax.plot(matrix[:, 0],
            matrix[:, 1], 
            matrix[:, 2])
    #ax.scatter(x, y, z, c=z,alpha=1)

    #plt.axis("off")
    plt.show()

