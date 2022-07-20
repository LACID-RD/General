import pydicom as dicom
import numpy as np
import tkinter as tk
from tkinter import filedialog
import operator
from myshow import *
import SimpleITK as sitk
from scipy.signal import convolve2d
import cv2 as cv


class Image:
    
    
    def __init__(self, slice, img, spacing, thickness, sobel, laplace, laplace2):
        self.slice = slice
        self.img = img
        self.spacing = spacing
        self.thickness = thickness
        self.sobel = sobel
        self.laplace = laplace
        self.laplace2 = laplace2
    def newAttr(self, attr):
        setattr(self, attr, attr)


def edgeConvolution(arr):
    
    #Edge detection

    kernelx = np.array([
        [-1,0,1],
        [-1,0,1],
        [-1,0,1]
    ])
    kernely = np.array([
        [-1,-1,-1],
        [0,0,0],
        [1,1,1]
    ])    

    
    xConvolution = convolve2d(arr, kernelx, 
    mode="same")
    yConvolution = convolve2d(arr, kernely,
    mode="same")
    edgedArray = np.sqrt((xConvolution**2)+(yConvolution**2))

    #Sobel Convolution

    kernelSobel1 = np.array([
        [1,0,-1],
        [2,0,-2],
        [1,0,-1]
    ])
    kernelSobel2 = np.array([
        [1,2,1],
        [0,0,0],
        [-1,-2,-1]
    ])

    sobel1 = convolve2d(arr, kernelSobel1, mode="same")
    sobel2 = convolve2d(arr, kernelSobel2, mode="same")

    sobelFilterArray = np.sqrt((sobel1)**2 + (sobel2)**2)


    #LaplacianFilter
    kerLaplace = np.array([
        [0,-1,0],
        [-1,4,-1],
        [0,-1,0]
    ])

    laplacianFilter = convolve2d(arr, kerLaplace, mode="same")
    return edgedArray, sobelFilterArray, laplacianFilter


def edgeDetection(arr):
    arr = np.array(np.copy(arr))
    image = sitk.GetImageFromArray(arr)
    sigma = 2.5
    
    
    #Laplace Recursive
    rglaplacianfilter = sitk.LaplacianRecursiveGaussianImageFilter()
    rglaplacianfilter.SetSigma(sigma)
    rglaplacianfilter.SetNormalizeAcrossScale(True)
    rglaplacianimage  = rglaplacianfilter.Execute(image)

    laplace = sitk.GetArrayFromImage(rglaplacianimage)

    
    #Sobel
    sobelFilter = sitk.SobelEdgeDetectionImageFilter()
    float_image =  sitk.Cast(image, sitk.sitkFloat32)
    sobelEdge = sitk.SobelEdgeDetection(float_image)

    sobel = sitk.GetArrayFromImage(sobelEdge)
    laplace2 = cv.Laplacian(arr, cv.CV_64F)
    return sobel, laplace, laplace2


def objectGenerator():

    emptyString = ""
    imagesDicom = []
    positionList = []
    counter = 0
    # Crear cuadro de selección de archivos:
    # Iterar sobre cada archivo .dcm del archivo seleccionado:
    image_list, image_slices, pmesh, img_qtt, countmesh, result, dcm_im_all = [], [], [], 0, 0, 0, []
    
    # Carga las imágenes, genera lista de slice y genera objetos
    path = tk.Tk()
    path.withdraw()
    file_name = filedialog.askopenfilenames(title="Array Generator")

    for i in file_name:
        #CREA LA LISTA DE OBJETOS
        dcm = dicom.dcmread(i)
        #counter += 1
        image_list.append('Imagen' + str(img_qtt))
        
        image_slices.append(dcm[0x0020,0x1041].value)
        sobel,laplace,laplace2 = edgeDetection(np.copy(dcm.pixel_array))
        
        image_list[img_qtt] = Image(dcm[0x0020,0x1041].value, np.copy(dcm.pixel_array), 
        dcm.PixelSpacing, dcm.SliceThickness, sobel, laplace, laplace2) # Lista de objetos tipo image
        
        dcm_im_all.append(dcm.pixel_array)
        img_qtt = img_qtt + 1
        sorted_image_list  = sorted(image_list, key = operator.attrgetter('slice'))
    
    list_of_arrays = [o.img for o in sorted_image_list]
    
    array = np.dstack(list_of_arrays)
    shape = np.shape(array)
    
    cond = False
    if cond == True:
        for n in range(shape[2]):
            arr = array[:,:,n]
            img = sitk.GetImageFromArray(arr)
            myshow(img)
    
    objectList = sorted_image_list

    return objectList, array

    
#objectGenerator()