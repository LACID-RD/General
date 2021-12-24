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
import guiqwt
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


def main():
    volumetricHUMatrixList, sliceThickness, pixelSpacing = volHUMatrixGenerator()
    matrixHU, shape = listOf2DMatrixTo3DMatrixGenerator(volumetricHUMatrixList)

    print("Volumetric Matrix HU Shape = " + str(shape))
    print("Slice Thickness of CT = " + str(sliceThickness) + " mm")

    resampledMatrix = resampling(matrixHU, sliceThickness, pixelSpacing)
    resampledShape = np.shape(resampledMatrix)
    
    print("Resampled Volumetric Matrix Shape = " + str(resampledShape))

    processedMatrix = lungMaskMatrixGenerator(resampledMatrix)
    processedMatrixShape = np.shape(processedMatrix)
    print("Shape processedMatrix = " + str(processedMatrixShape))

    for x in range(processedMatrixShape[0]):
        image = sitk.GetImageFromArray(processedMatrix[x,:,:])
        myshow(image)

main()
