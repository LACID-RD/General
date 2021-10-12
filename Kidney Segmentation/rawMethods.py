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

def imagePlots(Data_img):
    fig = plt.figure(figsize=(15, 15))

    fig.add_subplot(1, 3, 1)
    plt.imshow(Data_img, cmap=plt.cm.bone)
    plt.axis("off")
    plt.title("W/O Threshold")

    fig.add_subplot(1, 3, 2)
    treshhold = Data_img.copy()
    treshhold[treshhold < 1000] = 0
    treshhold[treshhold > 1100] = 0
    plt.imshow(treshhold, cmap=plt.cm.bone)
    plt.title("With Treshold")
    plt.axis("off")

    fig.add_subplot(1, 3, 3)
    superPositionData = np.multiply(Data_img, treshhold)
    plt.imshow(superPositionData, cmap=plt.cm.bone)
    plt.title("Superposition")
    plt.axis("off")
    plt.show()

def histogram2D(Data_img):
    n, bins, patches = plt.hist(Data_img, 64, density=True, fc="b", ec="k")
    plt.ylim([0,0.08])
    plt.xlim([0,1250])
    plt.title("Intensity Histogram")
    plt.show()

#Grafica arrays 3d de Numpy
def volumetricPlot(matrix):
    fig = plt.figure()
    z, x, y = matrix
    ax = fig.add_subplot(111, projection="3d")
    #ax.scatter(matrix[:, 0],
    #        matrix[:, 1], 
    #        matrix[:, 2])
    #ax.scatter(x, y, z, c=z,alpha=1)
    plt.show()

