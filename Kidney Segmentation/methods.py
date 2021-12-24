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


def multiplicableMask(pixelArray):
    mask = np.copy(pixelArray)
    shape = np.shape(mask)
    #shape = list(shape)
    #print(shape)
    for m in range(shape[0]):
        for n in range(shape[1]):
            if mask[m][n] <= -200:
                mask[m][n] = 1000  # 1000
            if 0 <= mask[m][n] <= 60:
                pass
            if mask[m][n] > 60:
                mask[m][n] = 0  # 0
    return mask


def getHoundfieldArray(dcm):
    arrayHU = (dcm.pixel_array*dcm.RescaleSlope) + dcm.RescaleIntercept
    return arrayHU


def volHUMatrixGenerator():

    #Variables
    emptyString = ""
    imagesDicom = []
    counter = 0
    mean = []
    volumetricHUMatrix = []

    # Crear cuadro de selección de archivos:
    cuadroDirectorio = tk.Tk()
    cuadroDirectorio.withdraw()
    folderPath = filedialog.askdirectory(title="DICOM Images")
    if folderPath is emptyString:
        print("Error: No seleccionó directorio.")
        sys.exit(0)

    # Iterar sobre cada archivo .dcm del archivo seleccionado:
    for root, dirs, files in os.walk(folderPath):
        for i in files:
            if i.endswith(".dcm"):

                counter += 1
                filePath = os.path.join(root, i)
                Img1 = ObjetoDicom()
                Img1.DescomDicom(filePath)
                ds = dicom.dcmread(filePath)
                pixelArray = ds.pixel_array
                
                imageData = np.copy(pixelArray)
                imagesDicom.append(imageData)

                #Obtener array matricial de U° HoundsField
                arrayHU = getHoundfieldArray(ds)

                # Variables de resampling:
                sliceThickness = ds.SliceThickness
                pixelSpacing = ds.PixelSpacing

                # Generar matriz volumetrica en HU
                aux = np.copy(arrayHU)
                volumetricHUMatrix.append(aux)
                image = sitk.GetImageFromArray(arrayHU)
                seriesArray = sitk.GetArrayViewFromImage(image)
    print("Patient ID = " + str(ds.PatientID))
    vol_HU_matrix = volumetricHUMatrix
    print(np.shape(vol_HU_matrix))

    return vol_HU_matrix, sliceThickness, pixelSpacing


def listOf2DMatrixTo3DMatrixGenerator(array):
    shape = np.shape(array)
    matrix3D = np.dstack(array)
    matrix3D = np.rollaxis(matrix3D,-1)
    return matrix3D,shape


def resampling(matrix_HU,sliceThickness,pixelSpacing):
    resampledArrayList = []

    shape = np.shape(matrix_HU)
    newVoxelSize = [1, 1, 1]
    spacing = sliceThickness + pixelSpacing[0]
    spacing = list([spacing, spacing, spacing])
    spacing = np.array(spacing)

    resizeFactor = (
        [spacing[0], float(pixelSpacing[0]), float(pixelSpacing[1])])
    resizeFactor = np.array(resizeFactor)
    shape = np.array(shape)

    newRealShape = np.multiply(shape, resizeFactor)
    print(newRealShape)

    newShape = np.round(newRealShape)

    #Función de resampling, ojo con el orden
    image = scipy.ndimage.zoom(matrix_HU, resizeFactor, order=1)
    resampledArrayList.append(image)

    resampledMatrix = np.dstack(resampledArrayList)
    #resampledMatrix = np.rollaxis(resampledMatrix,-1)
    return resampledMatrix


def makeLungMasks(img, display=False):
    row_size = img.shape[0]
    col_size = img.shape[1]

    mean = np.mean(img)
    std = np.std(img)
    img = img-mean
    img = img/std
    # Find the average pixel value near the lungs
    # to renormalize washed out images
    middle = img[int(col_size/5):int(col_size/5*4),
                int(row_size/5):int(row_size/5*4)]
    mean = np.mean(middle)
    max = np.max(img)
    min = np.min(img)
    # To improve threshold finding, I'm moving the
    # underflow and overflow on the pixel spectrum
    img[img == max] = mean
    img[img == min] = mean
    #
    # Using Kmeans to separate foreground (soft tissue / bone) and background (lung/air)
    #
    kmeans = KMeans(n_clusters=2).fit(
        np.reshape(middle, [np.prod(middle.shape), 1]))
    centers = sorted(kmeans.cluster_centers_.flatten())
    threshold = np.mean(centers)
    thresh_img = np.where(img < threshold, 1.0, 0.0)  # threshold the image

    # First erode away the finer elements, then dilate to include some of the pixels surrounding the lung.
    # We don't want to accidentally clip the lung.

    eroded = morphology.erosion(thresh_img, np.ones([3, 3]))
    dilation = morphology.dilation(eroded, np.ones([8, 8]))

    # Different labels are displayed in different colors
    labels = measure.label(dilation)
    label_vals = np.unique(labels)
    regions = measure.regionprops(labels)
    good_labels = []
    for prop in regions:
        B = prop.bbox
        if B[2]-B[0] < row_size/10*9 and B[3]-B[1] < col_size/10*9 and B[0] > row_size/5 and B[2] < col_size/5*4:
            good_labels.append(prop.label)
    mask = np.ndarray([row_size, col_size], dtype=np.int8)
    mask[:] = 0

    #
    #  After just the lungs are left, we do another large dilation
    #  in order to fill in and out the lung mask
    #
    for N in good_labels:
        mask = mask + np.where(labels == N, 1, 0)
    mask = morphology.dilation(mask, np.ones([10, 10]))  # one last dilation

    if (display):
        fig, ax = plt.subplots(3, 2, figsize=[12, 12])
        ax[0, 0].set_title("Original")
        ax[0, 0].imshow(img, cmap='gray')
        ax[0, 0].axis('off')
        ax[0, 1].set_title("Threshold")
        ax[0, 1].imshow(thresh_img, cmap='gray')
        ax[0, 1].axis('off')
        ax[1, 0].set_title("After Erosion and Dilation")
        ax[1, 0].imshow(dilation, cmap='gray')
        ax[1, 0].axis('off')
        ax[1, 1].set_title("Color Labels")
        ax[1, 1].imshow(labels)
        ax[1, 1].axis('off')
        ax[2, 0].set_title("Final Mask")
        ax[2, 0].imshow(mask, cmap='gray')
        ax[2, 0].axis('off')
        ax[2, 1].set_title("Apply Mask on Original")
        ax[2, 1].imshow(mask*img, cmap='gray')
        ax[2, 1].axis('off')

        plt.show()
        #return mask*img
    return mask


def lungMaskMatrixGenerator(resampledMatrix):

    shapeIter = np.shape(resampledMatrix)
    maskedList = []

    for n in range(shapeIter[0]):
        mask = makeLungMasks(resampledMatrix[n, :, :], display=False)
        maskedList.append(mask)
    processMatrix = np.dstack(maskedList)
    processMatrix = np.rollaxis(processMatrix,-1)

    return processMatrix
