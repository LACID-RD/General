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

##@njit(nogil=True)

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



#@jit()
def getHoundfieldArray(dcm):
    arrayHU = (dcm.pixel_array*dcm.RescaleSlope) + dcm.RescaleIntercept
    return arrayHU


##@jit()
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


#@jit()
def listOf2DMatrixTo3DMatrixGenerator(array):
    shape = np.shape(array)
    matrix3D = np.dstack(array)
    matrix3D = np.rollaxis(matrix3D,-1)
    return matrix3D,shape


#@jit()
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


#@jit()
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
    return mask,dilation


#@jit()
def lungMaskMatrixGenerator(resampledMatrix,display):

    shapeIter = np.shape(resampledMatrix)
    maskedList = []
    dilationList = []
    for n in range(shapeIter[0]):
        mask,dilation = makeLungMasks(resampledMatrix[n, :, :], display)
        maskedList.append(mask)
        dilationList.append(dilation)

    processMatrix = np.dstack(maskedList)
    processMatrix = np.rollaxis(processMatrix,-1)

    dilationMatrix = np.dstack(dilationList)
    dilationMatrix = np.rollaxis(dilationMatrix,-1)

    return processMatrix,dilationMatrix


#@jit()
def histogramMaker(array):
    #fig = plt.figure(figsize=(6,6))
    # for i in range(shape[0]):
    #     plt.hist(array[i,:,:], bins=5)
    #     plt.show()
    n, bins, patches = plt.hist(array[1,:,:])
    #plt.show()
    print(bins)
    #return n


#@jit()
def porcentageCalculatorLung(maskArray,dilationArray, maskShape, dilationShape):
    counter = 0
    counterList = []
    porcentageList = []
    for i in range(maskShape[0]):
        
        counter += 1
        
        air = maskArray[i, :, :]
        dim = np.shape(air)
        for m in range(dim[0]):
            for n in range(dim[1]):
                if air[m][n] < 0.5:
                    air[m][n] = 0
        
        m,n = 0,0
        
        dilation = dilationArray[i, :, :]
        dim2 = np.shape(dilation)
        for m in range(dim2[0]):
            for n in range(dim2[1]):
                if dilation[m][n] < 0.5:
                    dilation[m][n] = 0       
        suma = np.sum(air,axis=0)
        suma2 = sum(suma)
        suma3 = np.sum(dilation,axis=0)
        suma4 = sum(suma3)

        relacionAB = suma2/suma4
        porcentageList.append(relacionAB)
        counterList.append(counter)
        unionArray = np.dstack([counterList,porcentageList])
    
    print(np.shape(unionArray))
    return unionArray


#@jit()
def pandaMatrixManipulator(array, lowboundry, highboundry):
    shape = np.shape(array)
    array = np.reshape(array, (shape[1], shape[2]))
    columns = ["imgNum", "porcentage"]
    df = pd.DataFrame(array, columns=columns)
    df = df[(df.porcentage > lowboundry) & (df.porcentage < highboundry)]
    #print(df)
    matrix = df.to_numpy()
    return matrix


#@jit()
def imageEliminator(porcentageData,resampledMatrix,sliceThickness):
    i, x = 0, 0
    matList = []
    cropList = []

    reference = porcentageData[:, 0]
    array = np.copy(resampledMatrix)
    shape = np.shape(array)

    for x in np.nditer(reference):
        index = int(x)
        image = array[index,:,:]
        matList.append(image)

    matrix = np.dstack(matList)
    matrix = np.rollaxis(matrix,-1)
    print(np.shape(matrix))

    sliceThickness = int(sliceThickness)
    conversionMM = sliceThickness/10 #[mm]
    imagesPerCM = (10/conversionMM)/10

    ## MODIFICABLE ##

    distancia = 20
    distancia = distancia*int(sliceThickness)
    imgCons = distancia*imagesPerCM
    imgCons = int(imgCons)
    matrix = matrix[0:imgCons,:,:]
    shape = np.shape(matrix)
    print(shape)
    print("JUANCARLO")
    ## RESHAPER ##
   
    for i in range(shape[0]):
        print()
        arr = matrix[i,:,:]
        voxel = int(shape[1])
        val = 50
        rest = voxel - val
        arr = arr[val:rest][val:rest]
        cropList.append(arr)
    arr = np.dstack(cropList)
    arr = np.rollaxis(matrix,-1)
    print(np.shape(arr))

    with open("postProcessMat.npy","wb") as f:
        np.save(f,arr)
    
    return arr

def array2Image(array):
    shape = np.shape(array)
    for i in range(shape[0]):
        image = sitk.GetImageFromArray
        plt.imshow(image)
        plt.imshow