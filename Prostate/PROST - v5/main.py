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
        
### Grafico Crudo para chekar que las img esten ordenadas.

for _ in bvalSplit:
    for j in _:
        img = sitk.GetImageFromArray(np.array(j.img))
        crop = sitk.GetImageFromArray(np.array(j.cropArr))
        #myshow(img)
        myshow(crop)
