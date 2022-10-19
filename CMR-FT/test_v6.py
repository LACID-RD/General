import itertools
from logging import raiseExceptions
from array_generator_cardio import *
import SimpleITK as sitk
import numpy as np
import cv2 as cv
from scipy.signal import convolve2d
import sys




tensor, objList = array_generator_cardio()

#Cropper Reference
totalOfImages = int(len(objList))
middleImage = int(totalOfImages/2)
referenceImage = ((objList[middleImage]).img)
referenceImage2 = referenceImage.astype(np.int8)
# ROI for Cropper method
roi = cv.selectROI("Seleccione el ROI a analizar", referenceImage2)
print('Chosen ROI', roi)
cv.destroyAllWindows()

newList = []

for i in objList:
    normArr = i.normalize_image(np.array(i.img))
    crop = i.crop_array(normArr, roi)
    gradients = i.gradients_IxIy(crop, 3)
    setattr(i, 'Ix', gradients[0])
    setattr(i, 'Iy', gradients[1])
    setattr(i, 'cropped', crop)
    newList.append(i)
    

#Un atributo de cada objeto es el numero de phase cardiacas (esto te reeordena los objetitos)
cardPhase = int((newList[0]).cardPhase)
totalCardiacCycles = int(totalOfImages/cardPhase)
print('Cantidad de img = ', totalOfImages)
print("Cantidad de fases cardiacas = ", totalCardiacCycles)
# Lista de listas, cada ista tiene una fase entera cardiaca (generalmente 30 objetos c/u)
splitedList = np.array_split(newList, totalCardiacCycles)


class LucasKanadeData:
    def __init__(self, Ix1, Ix2, Iy1, Iy2, crop1, crop2):
        self.Ix1 = Ix1
        self.Ix2 = Ix2
        self.Iy1 = Iy1
        self.Iy1 = Iy2
        self.crop1 = crop1
        self.crop2 = crop2
        self.It = None 
    
    @classmethod
    def ItGradient(crop1, crop2):
        It = np.subtract(crop2, crop1)
        return It
i=0
iteratorList = []
for i in splitedList:
    iterlist = list(itertools.pairwise(i))
    iteratorList.append(iterlist)
i=0
n=0
lkInstances = []
for i in iteratorList:
    for n in i:
        if not type((n[0]).cropped) is None:
            obj1 = n[0]
            obj2 = n[1]
            Ix1 = obj1.Ix
            Ix2 = obj2.Ix
            Iy1 = obj1.Iy
            Iy2 = obj2.Iy
            crop1 = obj1.cropped
            crop2 = obj2.cropped
            #print(type(obj1.cropped))
            instance = LucasKanadeData(Ix1, Ix2, Iy1, Iy2, crop1, crop2)
            lkInstances.append(instance)
        else:
            continue
        
print(len(lkInstances))

for x in lkInstances:
    c1 = np.array(x.crop1)
    c2 = np.array(x.crop2)
    val = x.ItGradient(c1, c2)
    print(val)
    setattr(x, 'It', val)
    
