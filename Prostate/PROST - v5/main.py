import matplotlib.pyplot as plt
import numpy as np
import SimpleITK as sitk
from myshow import *
import cv2 as cv
from loader import *


# TAGS IMPORTANTES
# Bval individual [0x0043,0x1039]
# img por bval [0x0021, 0x104F]

generatedMatrix, objectList = obj_loader()

#Identificamos y asignamos el valor de b correspondiente a cada imagen
for i in objectList:
    bvalues = i.bvalue
    bvalues = bvalues[0]
    s = str(bvalues)
    s = s[1:]
    value = s.split('00000')
    b = int(value[1])
    setattr(i, 'b', b)
    
#Marcamos la cantidad de imagens por valor de b    
imgPerBvalue  = objectList[0].imgPerBvalue

print('Img quantity per bvalue:', imgPerBvalue)

## LISTA DE LISTAS cada sublista es un corte con sus n bvals.
splitList = np.array_split(objectList, imgPerBvalue)
#print('Shape of bvalues sub-list', np.shape(splitList))

## LISTA DE LISTAS, cada sublista son todas las imagenes de cada bval.
bvalSortedList = list()
bvalList = list()

for i in splitList[0]:
    val = i.b
    bvalList.append(val)

print('bvalues list:', bvalList)

numOfBvalues = len(bvalList)
print('num of b vals:', numOfBvalues)
auxList = list()

for i in bvalList:
    for j in objectList:
        if i == j.b:
            auxList.append(j)

# Arr de 3 listas, cada lista tiene todas las imagenes de cada b val.
bvalSplit = np.array_split(auxList, numOfBvalues)
           
## ROI sobre las imagenes.
# Version un ROI para todos los b-val

ref = bvalSplit[0]
refImg = ref[int(len(ref)/2)].img
refImg = refImg.astype(np.uint8)

roi = cv.selectROI('Select a prostate ROI', refImg)
print('Selected ROI:', roi)
cv.destroyAllWindows()

for _ in bvalSplit:
    for j in _:
        img = np.array(j.img)
        cropArr = j.crop_array(img, roi)
        setattr(j, 'cropArr', cropArr)
        normCropArr = j.normalize_image(cropArr)
        setattr(j, 'normCropArr', normCropArr)
        

### Eq IVIM:
'''
S/S0 = fexp(-bD*) + (1-f)exp(-bD + (bD)**2 * K/6)
'''
### Mapas de Intensidad vs B-value:

# splitList es la lista cuyas sublistas son cada corte

def sitk_histogram(arr):
    img = sitk.GetImageFromArray(arr)
    threshold = sitk.ThresholdImageFilter()
    threshold.SetOutsideValue(0)
    threshold.SetLower(100)
    threshold.SetUpper(8000)
    res = threshold.Execute(img)
    myshow(res)

### Grafico Crudo para chekar que las img esten ordenadas.

for _ in bvalSplit:
    for j in _:
        crop = np.array(j.cropArr)
        #sitk_histogram(crop)

def map_ADC():
    
    return

def signal_points(sliceList):
    signalPointsList = list()
    S0 = sliceList[0]
    
    for i in sliceList:
        signalOverS0 = np.divide(i, S0)
        signalPointsList.append(signalOverS0)
        
    return signalPointsList

        
for slice in splitList:
    pass