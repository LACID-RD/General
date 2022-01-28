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
from methods import *
from numba import jit, cuda, vectorize


def main2():
    with open("postProcessMat.npy","rb") as f:
        matrix = np.load(f)
    shape = np.shape(matrix)
    print(type(matrix))
    print(shape)
    counter = 0
    for i in range(shape[0]):
        counter += 1
        print(counter)
        array = matrix[i,:,:]
        image = sitk.GetImageFromArray(array)
        myshow(image)
    
        
main2()



