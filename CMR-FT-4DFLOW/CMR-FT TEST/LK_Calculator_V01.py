import itertools
from array_generator_cardio import *
import SimpleITK as sitk
import numpy as np
import cv2 as cv
from scipy.signal import convolve2d
from scipy import linalg
import matplotlib.pyplot as plt


class LucasKanadeData:
    def __init__(self, cropArr1, cropArr2,  velX, velY, velMod):
        self.cropArr1 = cropArr1
        self.cropArr2 = cropArr2
        self.velX = velX
        self.velY = velY
        self.velMod = velMod


# def optical_flow(arr1, arr2, window_size=3, tau=1e-2):

#     kernel_x = np.array([[-1., 1.], [-1., 1.]])
#     kernel_y = np.array([[-1., -1.], [1., 1.]])
#     kernel_t = np.array([[1., 1.], [1., 1.]]) #*.25
    
#     w = int(window_size/2) # window_size is odd, all the pixels with offset in between [-w, w] are inside the window
    
#     arr1 = arr1 / 255. # normalize pixels
#     arr2 = arr2 / 255. # normalize pixels
#     # Implement Lucas Kanade
#     # for each point, calculate I_x, I_y, I_t
    
#     mode = 'same'
    
#     fx = convolve2d(arr1, kernel_x, boundary='symm', mode=mode)
#     fy = convolve2d(arr1, kernel_y, boundary='symm', mode=mode)
#     ft = convolve2d(arr2, kernel_t, boundary='symm', mode=mode) + convolve2d(arr1, -kernel_t, boundary='symm', mode=mode)

#     shapeArr1 = np.shape(arr1)
#     shapeArr2 = np.shape(arr2)
        
#     u = np.zeros(shapeArr1)
#     v = np.zeros(shapeArr2)
    
#     # within window window_size * window_size
#     for i in range(w, shapeArr1[0] - w):
#         for j in range(w, shapeArr2[1] - w):
#             Ix = fx[i-w:i+w+1, j-w:j+w+1].flatten()
#             Iy = fy[i-w:i+w+1, j-w:j+w+1].flatten()
#             It = ft[i-w:i+w+1, j-w:j+w+1].flatten()
#             b = np.reshape(It, (It.shape[0], 1)) # get b here
#             A = np.vstack((Ix, Iy)).T # get A here
#             if np.min(abs(np.linalg.eigvals(np.matmul(A.T, A)))) >= tau:
#                 nu = np.matmul(np.linalg.pinv(A), b) # get velocity here
#                 u[i,j]=nu[0]
#                 v[i,j]=nu[1]
#     return (u, v)



def optical_flow(objTuple, window_size=3, tau=1e-15):

    obj1 = objTuple[0]
    obj2 = objTuple[1]
    arr1 = obj1.cropArr
    arr2 = obj2.cropArr
    
    kernel_x = np.array([[-1., 1.], [-1., 1.]])
    kernel_y = np.array([[-1., -1.], [1., 1.]])
    kernel_t = np.array([[1., 1.], [1., 1.]])
    
    w = int(window_size/2) # window_size is odd, all the pixels with offset in between [-w, w] are inside the window
    
    arr1 = arr1 / 255. # normalize pixels
    arr2 = arr2 / 255. # normalize pixels
    # Implement Lucas Kanade
    # for each point, calculate I_x, I_y, I_t
    
    mode = 'same'
    
    fx = convolve2d(arr1, kernel_x, boundary='symm', mode=mode)
    fy = convolve2d(arr1, kernel_y, boundary='symm', mode=mode)
    ft = convolve2d(arr2, kernel_t, boundary='symm', mode=mode) + convolve2d(arr1, -kernel_t, boundary='symm', mode=mode)

    shapeArr1 = np.shape(arr1)
    shapeArr2 = np.shape(arr2)
        
    u = np.zeros(shapeArr1)
    v = np.zeros(shapeArr2)
    
    # within window window_size * window_size
    for i in range(w, shapeArr1[0] - w):
        for j in range(w, shapeArr2[1] - w):
            Ix = fx[i-w:i+w+1, j-w:j+w+1].flatten()
            Iy = fy[i-w:i+w+1, j-w:j+w+1].flatten()
            It = ft[i-w:i+w+1, j-w:j+w+1].flatten()
            b = np.reshape(It, (It.shape[0], 1)) # get b here
            A = np.vstack((Ix, Iy)).T # get A here
            eigen = np.min(abs(np.linalg.eigvals(np.matmul(A.T, A))))
            #print(eigen)
            if eigen >= tau:
                nu = np.matmul(np.linalg.pinv(A), b) # get velocity here
                u[i,j]=nu[0]
                v[i,j]=nu[1]
    return (u, v)


def main():

    tensor, objList = array_generator_cardio()

    '''Create a reference array for the crop'''    
    totalOfImages = int(len(objList))
    middleImage = int(totalOfImages/2)
    referenceImage = ((objList[middleImage]).img)
    referenceImage2 = referenceImage.astype(np.int8)

    # Un atributo de cada objeto es el numero de phase cardiacas (esto te reeordena los objetitos)
    cardPhase = int((objList[0]).cardPhase)
    totalCardiacCycles = int(totalOfImages/cardPhase)
    print('Img quantity: ', totalOfImages)
    print('Total cardiac phases', totalCardiacCycles)

    # Lista de listas, cada lista tiene una fase entera cardiaca (generalmente 30 objetos c/u)
    splitedList = np.array_split(objList, totalCardiacCycles)

    # Seleccionar la fase cardiaca a analizar
    phase = int(input('Introduce the number of the cardiac phase to be processed: '))
    print('Phase Number: ', phase)

    #Agarra la fase marcada y toma el comienzo
    phaseList = splitedList[phase]
    phaseStart = phaseList[0].img
    phaseStart2 = phaseStart.astype(np.int8)

    # ROI for Cropper method
    roi = cv.selectROI('Crop the heart', phaseStart2)
    print('Zoom ROI selected', roi)
    cv.destroyAllWindows()

    # x1, x2, y1, y2 = int(roi[0]), int(roi[1]), int(roi[2]), int(roi[3])
    heartviewRaw = phaseStart[int(roi[1]):int(roi[1] + roi[3]), 
                            int(roi[0]):int(roi[0] + roi[2])]
    # heartview = heartviewRaw.astype(np.int8)

    x, i = 0, 0
    
    for i in phaseList:
        ''' Normalize and crop array of the cardiac phase.'''
        normArr = i.normalize_image(np.array(i.img))
        cropArr = i.crop_array(normArr, roi)
        ''' Add the arrays as new obj attrs'''
        setattr(i, 'normArr', normArr)
        setattr(i, 'cropArr', cropArr)
        
    '''Para ahorrar memoria en esta version del code, preferi hacer el tema de los
    gradientes dentro del propio calculo de los vectores, apundando a dejar una clase
    no muy sucia.'''
    '''
    PD: el iterator es la salvacion (solo compatible con Python 3.10 y superior)
    '''
    
    i=0
    iterator = itertools.pairwise(phaseList)
    iteratorList = list(iterator)
    
    '''El iterador nos va a generar una lista de tuplas de la forma que podamos calcular
    (obj1, obj2), (obj2, obj3) ... etc {pensandolo mejor capaz podemos obviar esta parte 
    de la implementacion}'''

    print('Iterator object creation completed...', '\n')
    
    '''Mi nueva idea es divir la imagen obtenida en ventanitas nxn, n E [2, 5].
    considero que deberiamos realizar el cálculo con las ventas internas, omitiendo 
    los pasos para los k nxn bordes de la img.
    
    Ojo con el crop.
    
    Esto tambien esta bueno porque puedo usar los mismos datos para implementar HornShunck.'''
    
    ''' TODO: i.cropArr with window selector '''
    vectorList = list()
    # with open('vectors.txt', 'w') as f:
        
    #     for i in iteratorList:
    #         velVector = optical_flow(i, 3)
    #         f.write(str(velVector))
    #         f.write('\n')
    #         print(np.mean(velVector))
    #         print(np.max(velVector))
    #         print(np.min(velVector))
    #         velImg = sitk.GetImageFromArray(velVector)
    #         modVel = np.sqrt(np.)
    #         myshow(velImg, cmap=plt.cm.bone)
    
    lkDataList = list()
    
    for i in iteratorList:
        obj1 = i[0]
        obj2 = i[1]
        velVector = optical_flow(i, 3)
        velX = velVector[0]
        velY = velVector[1]
        squareVel = np.add(np.square(velX), np.square(velY))
        modVel = np.sqrt(squareVel)

        lkInstance = LucasKanadeData(cropArr1 = obj1.cropArr, cropArr2 = obj2.cropArr,
                                     velX = velX, velY = velY, velMod = modVel)
        
        lkDataList.append(lkInstance)
        
        #velImg = sitk.GetImageFromArray(modVel)
        
        #myshow(velImg, cmap=plt.cm.bone)


    #arr1 = arr1 / 255. # normalize pixels
    #arr2 = arr2 / 255. # normalize pixels
   
    # mode = 'same'
    
    # fx = convolve2d(arr1, kernel_x, boundary='symm', mode=mode)
    # fy = convolve2d(arr1, kernel_y, boundary='symm', mode=mode)
    # ft = convolve2d(arr2, kernel_t, boundary='symm', mode=mode) + convolve2d(arr1, -kernel_t, boundary='symm', mode=mode)

    # shapeArr1 = np.shape(arr1)
    # shapeArr2 = np.shape(arr2)
        
    # u = np.zeros(shapeArr1)
    # v = np.zeros(shapeArr2)
    
    
    # lkInstances = []

    # '''Creamos las instancias de la clase LucasKanadeData'''

    # for i in iteratorList:
    #     crop = i[0].cropList
    #     if not type(crop[0]) is None:
    #         obj1 = i[0]
    #         obj2 = i[1]
    #         Ix1List = obj1.IxList
    #         Ix2List = obj2.IxList
    #         Iy1List = obj1.IyList
    #         Iy2List = obj2.IyList
    #         cropList1 = obj1.cropList
    #         cropList2 = obj2.cropList
    #         instance = LucasKanadeData(Ix1List, Ix2List, Iy1List, 
    #                                 Iy2List, cropList1, cropList2)
    #         lkInstances.append(instance)
    #     else:
    #         continue
            
    # print('len lkInstance', len(lkInstances))

    # i, x = 0, 0 
    # '''HASTA ACA ANDA BIEN v11'''
    # '''Esta lista sera la lista de arrays correspondientes a los 
    # IT'''
    # timeGradientList = []
    # for x in lkInstances:
    #     #index = lkInstances.index(x)
    #     ''' Buscamos las dos listas de los crops, deberian ser cada una, 
    #     una lista de arrays, un elemento de lista por cada mini imagen'''
        
    #     c1 = x.cropList1
    #     c2 = x.cropList2
    #     # print(np.shape(c1[0])==np.shape(c2[0]))
        
    #     for i, j in zip(c1, c2):
    #         gradient = np.subtract(j, i)
    #         myshow(sitk.GetImageFromArray(gradient))
    #         timeGradientList.append(gradient)
            
        
    #     # for i in c1:
    #     #     index = c1.index(i)
    #     #     timeGradient = np.subtract(c2[index], c1) 
    #     #     timeGradientList.append(timeGradient)
            
    #     setattr(x, 'listIt', timeGradientList)
    #     #img = sitk.GetImageFromArray(It)
    #     #myshow(img, cmap=plt.cm.bone)

    # print('len TIME GRADIENTS', len(timeGradientList))
        
    # def lucas_kanade_all(objList):
        
    #     vectors = []

    #     for i in objList:
            
    #         Ix1 = np.array(i.Ix1)
    #         Ix2 = np.array(i.Ix2)
            
    #         Iy1 = np.array(i.Iy1)
    #         Iy2 = np.array(i.Iy2)
            
    #         crop1 = np.array(i.crop1)
    #         crop2 = np.array(i.crop2)
            
    #         It = np.array(i.It)
            
    #         #print(np.shape(crop1))
    #         #print(np.shape(crop2))       
            
    #         A = np.hstack(Ix1)
    #         B = np.hstack(Iy1)
            
    #         S = np.column_stack((A, B))
    #         St = np.transpose(S)
            
    #         C = np.matmul(St, S)
            
    #         T = np.hstack(It)
    #         b = np.column_stack((T))

    #         #print(linalg.inv(C))
    #         #\print(linalg.det(C))
    #         #print(linalg.eigvals(C))
            
    #         #x = linalg.solve(S, b)
    #         var1 = linalg.inv(C)
            
    #     # print('It:', np.shape(It))
    #     # print('Ix:', np.shape(Ix1))
    #     # print('Iy:', np.shape(Iy1))
    #     # print('S:', np.shape(S))
    #     # print('St:', np.shape(St))
    #     # print('(St.S)inv:', np.shape(var1))
            
    #         var2 = np.matmul(St, T)
    #         x = np.matmul(var1, var2)
            
    #         vectors.append(x)
            
    #     normVectors = []
    #     #print(np.shape(x))
    #     for x in vectors:
    #         nor = np.linalg.norm(x)
    #         #print('norma', nor)
    #         if abs(nor) > 0: 
    #             normalized = x/nor
    #             normVectors.append(normalized)
    #         elif abs(nor) <= 0:
    #             normVectors.append(x)
                
    #     return normVectors
            
    
    # # vecs = lucas_kanade_all(lkInstances)
    # # print(vecs)
    # # with open('vectors.txt', 'w') as file:
    # #     for i in vecs:
    # #         file.write(str(i))
    # #         file.write('\n')
    
    
if __name__ == '__main__':
    main()