from itertools import count
from lucaskanadev1 import *
from array_generator_cardio import *
import SimpleITK as sitk
import numpy as np
import cv2 as cv
from scipy.signal import convolve2d
import sys

def laplacian(arr):
    laplace = cv.Laplacian(arr, cv.CV_64F, ksize=3)
    return laplace


def sobel_filter(arr):
    #Sobel
    image = sitk.GetImageFromArray(arr)
    sobelFilter = sitk.SobelEdgeDetectionImageFilter()
    float_image =  sitk.Cast(image, sitk.sitkFloat32)
    sobelEdge = sitk.SobelEdgeDetection(float_image)

    sobel = sitk.GetArrayFromImage(sobelEdge)
    return sobel


def edge_sharp(arr):
    
    ker1 = np.array([[-1, -1, -1], 
                     [-1, 9, -1], 
                     [-1, -1, -1]])
    
    '''ker2 = np.array([[0, 1, 2], 
                     [-1, 0, 1], 
                     [-2, -1, 0]])
    
    ker3 = np.array([[0, -1, -2], 
                     [1, 0, -1], 
                     [2, 1, 0]]) '''  
    
    sharp = convolve2d(arr, ker1, mode='same')
    #t1 = convolve2d(sharp, ker2, mode='same')
    #t2 = convolve2d(sharp, ker3, mode='same')
    #t1 = t1.astype('float64')
    #t2 = t2.astype('float64')
    #sob = (np.sqrt(np.square(t1), np.square(t2)))
    
    
    
    return sharp
    #print(np.shape(ker1))
    

def gaussian_blur(arr, sigmaX, sigmaY):
    blur = cv.GaussianBlur(arr, (3, 3),
                           sigmaX=sigmaX, sigmaY=sigmaY)
    return blur


def sitk_threshold(arr, lower, upper, outside, inside):
    img = sitk.GetImageFromArray(arr)
    binT = sitk.BinaryThresholdImageFilter()
    binT.SetLowerThreshold(lower)
    binT.SetUpperThreshold(upper)
    binT.SetOutsideValue(outside)
    binT.SetInsideValue(inside)
    binImg = binT.Execute(img)
    return binImg


def binary_contour(arr):
    img = sitk.GetImageFromArray(arr)
    contour = sitk.BinaryContourImageFilter()
    contour.FullyConnectedOn()
    contour.SetBackgroundValue(0)
    contour.SetForegroundValue(1)
    contImg = contour.Execute(img)
    return contImg


def denoise_binary(arr):
    img = sitk.GetImageFromArray(arr)
    img = sitk.Cast(img, sitk.sitkFloat32)
    denoise = sitk.BinaryMinMaxCurvatureFlowImageFilter()
    denoise.SetThreshold(1)
    denoise.SetStencilRadius(10)
    denoise.SetNumberOfIterations(100)
    denoised = denoise.Execute(img)
    return denoised


#Generamos una lista de pixel arrays y una lista de los objetos de cada img
tensors, objList = array_generator_cardio()

#Cropper
totalOfImages = int(len(objList))
middleImage = int(totalOfImages/2)
referenceImage = ((objList[middleImage]).img)
print(type(referenceImage))

#img = myshow(sitk.GetImageFromArray(referenceImage), cmap=plt.cm.bone)
referenceImage2 = referenceImage.astype(np.uint8)
referenceImage2 = cv.applyColorMap(referenceImage2, colormap=cv.COLORMAP_BONE)

roi = cv.selectROI("Seleccione el ROI a analizar", referenceImage2)

print('Chosen ROI', roi)
cv.destroyAllWindows()

x1, y1, x2, y2 = int(roi[0]), int(roi[1]), int(roi[2]), int(roi[3])

newList = []


for n in objList:
    arr = n.img
    newArr = arr[y1:int(y1 + y2), x1:int(x1 + x2)]
    
    
    blur = gaussian_blur(newArr, 2.5, 2.5)
    sobel = sobel_filter(blur)
    sharp = edge_sharp(newArr)
    
    thresh = sitk_threshold(blur, lower=325, upper=750,outside=0, inside=1)
    thresh = sitk.GetArrayFromImage(thresh)
    
    denoised = denoise_binary(thresh)
    denoised = sitk.GetArrayFromImage(denoised)
    
    contour = binary_contour(thresh)
    contour = sitk.GetArrayFromImage(contour)
    
    
    setattr(n, 'crop', newArr)
    setattr(n, 'sobel', sobel)
    setattr(n, 'thresh', thresh)
    setattr(n, 'sharp', sharp)
    setattr(n, 'contour', contour)
    setattr(n, 'denoised', denoised)
    
    
    newList.append(n)
    #print(np.shape(arr), np.shape(newArr))
    #img = myshow(sitk.GetImageFromArray(newArr), cmap=plt.cm.bone)
     
     
#Un atributo de cada objeto es el numero de phase cardiacas (esto te reeordena los objetitos)
cardPhase = int((newList[0]).cardPhase)
totalCardiacCycles = int(totalOfImages/cardPhase)
print('Cantidad de img = ', totalOfImages)
print("Cantidad de fases cardiacas = ", totalCardiacCycles)

splitedList = np.array_split(newList, totalCardiacCycles)

print(np.shape(tensors))


def plot():
    n=1
    for i in splitedList[7]:
        
        print(n)
        n+=1
        
        originalArr = i.crop
        sobelArr = i.sobel
        threshArr = i.thresh
        sharpArr = i.sharp
        substractedArr = np.subtract(originalArr, sobelArr)
        contourArr = i.contour
        denoisedArr = i.denoised
        #sobel2Arr = np.multiply(10000000, sobel2Arr)
        
        originalImg = sitk.GetImageFromArray(originalArr)
        sobelImg = sitk.GetImageFromArray(sobelArr)
        substractedImg = sitk.GetImageFromArray(substractedArr)
        threshImg = sitk.GetImageFromArray(threshArr)
        sharpImg = sitk.GetImageFromArray(sharpArr)
        denoisedImg = sitk.GetImageFromArray(denoisedArr)
        
        contourImg = sitk.GetImageFromArray(contourArr)
        
        myshow(originalImg, cmap=plt.cm.bone)
        myshow(sobelImg, cmap=plt.cm.bone)
        #myshow(substractedImg, cmap=plt.cm.bone)
        myshow(threshImg, cmap=plt.cm.bone)
        #myshow(sharpImg, cmap=plt.cm.bone)
        myshow(contourImg, cmap=plt.cm.bone)
        myshow(denoisedImg, cmap=plt.cm.bone)
plot()  







