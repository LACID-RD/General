import itertools
from array_generator_cardio import *
import SimpleITK as sitk
import numpy as np
import cv2 as cv
from scipy.signal import convolve2d
from scipy import linalg
import matplotlib.pyplot as plt


def main():

    tensor, objList = array_generator_cardio()


    #Cropper Reference
    totalOfImages = int(len(objList))
    middleImage = int(totalOfImages/2)
    referenceImage = ((objList[middleImage]).img)
    referenceImage2 = referenceImage.astype(np.int8)

    #Un atributo de cada objeto es el numero de phase cardiacas (esto te reeordena los objetitos)
    cardPhase = int((objList[0]).cardPhase)
    totalCardiacCycles = int(totalOfImages/cardPhase)
    print('Cantidad de img = ', totalOfImages)
    print("Cantidad de fases cardiacas = ", totalCardiacCycles)

    # Lista de listas, cada lista tiene una fase entera cardiaca (generalmente 30 objetos c/u)
    splitedList = np.array_split(objList, totalCardiacCycles)

    # Seleccionar la fase cardiaca a analizar
    print('Introduce the number of the cardiac phase to be processed: ')
    phase = int(input())
    print('Numero de fase', phase)

    #Agarra la fase marcada y toma el comienzo
    phaseList = splitedList[phase]
    phaseStart = phaseList[0].img
    phaseStart2 = phaseStart.astype(np.int8)

    # ROI for Cropper method
    roi = cv.selectROI('Crop the heart', phaseStart2)
    print('Zoom ROI selected', roi)
    cv.destroyAllWindows()

    #x1, x2, y1, y2 = int(roi[0]), int(roi[1]), int(roi[2]), int(roi[3])
    heartviewRaw = phaseStart[int(roi[1]):int(roi[1] + roi[3]), 
                            int(roi[0]):int(roi[0] + roi[2])]
    heartview = heartviewRaw.astype(np.int8)

    #Agarras rois multiples (esto puede variar, te los guarda como arrays)
    rois = cv.selectROIs('Select Lucas-Kanade windows', heartview)
    print(rois, type(rois))
    cv.destroyAllWindows()

    '''
    Aca tuve que armar otra clase porque los objetos del phase list quedan muy 
    sucios depues de todas las huevadas que hice.
    '''

    x, i = 0, 0

    #Acá tiene que ser si o si el phaseList porque los crops son locales
    for i in phaseList:
        
        cropList = []
        IxList = []
        IyList = []
        
        normArr = i.normalize_image(np.array(i.img))
        
        for x in rois:
            
            crop = i.crop_array(normArr, x)
            Ix, Iy = i.gradients_IxIy(crop, 3)
            
            cropList.append(crop)
            IxList.append(Ix)
            IyList.append(Iy)
        
        setattr(i, 'cropList', cropList)
        setattr(i, 'normArr', normArr)
        setattr(i, 'IxList', IxList)
        setattr(i, 'IyList', IyList)


    '''
    hasta aca no deberia haber drama con el código
    '''

    '''
    Cada objetito de la phase list va a tener su array normalizado y una lista con los crops
    producto de los rois,
    cada uno de esos crops es la base para generar los gradientes Ix, Iy
    Los gradientes tambien son listas y los indices estan relacionados entre si
    '''

    '''
    Ahora la idea es poder generar una clase agrupadora que pueda agarrar todos los datos que necesitas para
    poder iterar bien entre imagenes y armarte los gradientes temporales.
    '''

    ''' Te deberian de quedar n-1 objetos si lo comparas con la phaseList'''


    class LucasKanadeData:
        def __init__(self, listIx1, listIx2, listIy1, 
                    listIy2, cropList1, cropList2):
            '''
            INPUT: 
            Lista de gradientes img 1
            Lista de gradientes img 2
            
            Lista de rois sobre img 1
            Lista de rois sobre img 2
            
            VOID: Despues le agregamos como atributo extra la lista de gradientes temporales
            '''
            
            self.listIx1 = listIx1 
            self.listIx2 = listIx2
            self.listIy1 = listIy1
            self.listIy2 = listIy2
            self.cropList1 = cropList1
            self.cropList2 = cropList2
            
            ''' Aca habia intentado definir el calculo de los gradientes temporales
            como metodo propio de la clase, pero por motivos esotericos a python no le gusta'''


    ''' Ahora que ya tenemos la clase armada debemos iterar correctamente sobre las images'
    la idea seria que siga la siguiente secuencia 
    1-2, 2-3, 3-4, 4-5 ... 
    como ven te deberian quedar n-1,
    n-1 tuplas por la implentacion de itertools.pairwise sobre los elementos
    '''

    ''' Como esto iterando sobre tantas huevadas prefiero irle clavando i,x,n a todo aunque queda como
    trabajo a posteriori dejar todo esto más bonito.
    '''

    '''
    el iterator es la salvacion
    '''
    i=0
    iterator = itertools.pairwise(phaseList)
    iteratorList = []
    '''
    Una vez que tenemos el objeto iterator creamos una lista de los pares de tuplas
    que se corresponden a cada par de objetos
    '''
    
    for i in iterator:
        iteratorList.append(i)
            
    # for i in phaseList:
    #     iterlist = itertools.pairwise(i)
    #     iteratorList.append(iterlist)

    # with open('iter.txt', 'w') as f:
    #     l = list(iterator)
    #     for i in l:
    #         f.write(str(i))


    print('hasta aca funka')
    i=0
    n=0
    lkInstances = []

    '''Creamos las instancias de la clase LucasKanadeData'''

    for i in iteratorList:
        crop = i[0].cropList
        if not type(crop[0]) is None:
            obj1 = i[0]
            obj2 = i[1]
            Ix1List = obj1.IxList
            Ix2List = obj2.IxList
            Iy1List = obj1.IyList
            Iy2List = obj2.IyList
            cropList1 = obj1.cropList
            cropList2 = obj2.cropList
            instance = LucasKanadeData(Ix1List, Ix2List, Iy1List, 
                                    Iy2List, cropList1, cropList2)
            lkInstances.append(instance)
        else:
            continue
            
    print('len lkInstance', len(lkInstances))

    i, x = 0, 0 
    '''HASTA ACA ANDA BIEN v11'''
    '''Esta lista sera la lista de arrays correspondientes a los 
    IT'''
    timeGradientList = []
    for x in lkInstances:
        #index = lkInstances.index(x)
        ''' Buscamos las dos listas de los crops, deberian ser cada una, 
        una lista de arrays, un elemento de lista por cada mini imagen'''
        
        c1 = x.cropList1
        c2 = x.cropList2
        # print(np.shape(c1[0])==np.shape(c2[0]))
        
        for i, j in zip(c1, c2):
            gradient = np.subtract(j, i)
            myshow(sitk.GetImageFromArray(gradient))
            timeGradientList.append(gradient)
            
        
        # for i in c1:
        #     index = c1.index(i)
        #     timeGradient = np.subtract(c2[index], c1) 
        #     timeGradientList.append(timeGradient)
            
        setattr(x, 'listIt', timeGradientList)
        #img = sitk.GetImageFromArray(It)
        #myshow(img, cmap=plt.cm.bone)

    print('len TIME GRADIENTS', len(timeGradientList))
        
    def lucas_kanade_all(objList):
        
        vectors = []

        for i in objList:
            
            Ix1 = np.array(i.Ix1)
            Ix2 = np.array(i.Ix2)
            
            Iy1 = np.array(i.Iy1)
            Iy2 = np.array(i.Iy2)
            
            crop1 = np.array(i.crop1)
            crop2 = np.array(i.crop2)
            
            It = np.array(i.It)
            
            #print(np.shape(crop1))
            #print(np.shape(crop2))       
            
            A = np.hstack(Ix1)
            B = np.hstack(Iy1)
            
            S = np.column_stack((A, B))
            St = np.transpose(S)
            
            C = np.matmul(St, S)
            
            T = np.hstack(It)
            b = np.column_stack((T))

            #print(linalg.inv(C))
            #\print(linalg.det(C))
            #print(linalg.eigvals(C))
            
            #x = linalg.solve(S, b)
            var1 = linalg.inv(C)
            
        # print('It:', np.shape(It))
        # print('Ix:', np.shape(Ix1))
        # print('Iy:', np.shape(Iy1))
        # print('S:', np.shape(S))
        # print('St:', np.shape(St))
        # print('(St.S)inv:', np.shape(var1))
            
            var2 = np.matmul(St, T)
            x = np.matmul(var1, var2)
            
            vectors.append(x)
            
        normVectors = []
        #print(np.shape(x))
        for x in vectors:
            nor = np.linalg.norm(x)
            #print('norma', nor)
            if abs(nor) > 0: 
                normalized = x/nor
                normVectors.append(normalized)
            elif abs(nor) <= 0:
                normVectors.append(x)
                
        return normVectors
            
    
    # vecs = lucas_kanade_all(lkInstances)
    # print(vecs)
    # with open('vectors.txt', 'w') as file:
    #     for i in vecs:
    #         file.write(str(i))
    #         file.write('\n')
    
    
if __name__ == '__main__':
    main()