import pydicom as dicom
import numpy as np
import SimpleITK as sitk
from scipy.signal import convolve2d
#from array_generator_cardio import array_generator_cardio
from myshow import *
import cv2 as cv 


#arr, obj = array_generator_cardio()

def filters(arr):
    
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
    
    
    #EDGE SHARP ## #TODO#
    convo = sitk.ConvolutionImageFilter()
    

    return sobel, laplace

def edge_sharpening(arr):
    
    ker1 = np.array([
                     [1,1,1], 
                     [0,0,0], 
                     [-1,-1,-1]
                     ])
    ker2 = np.array([
                     [1,0,-1], 
                     [1,0,-1], 
                     [1,0,-1]
                     ])    
    
    for x in range(len(arr)):
        temp1 = convolve2d(arr[x,:,:], ker1, mode='same')
        temp2 = convolve2d(arr[x,:,:], ker2, mode='same')
        temp3 = np.sqrt(np.power(temp1, 2) + np.power(temp2, 2))
        plt.axis('off')
        plt.imshow(temp3, cmap='grey')
        plt.show()

def laplacian(arr):
    laplace = cv.Laplacian(arr, cv.CV_64F)
    return laplace


