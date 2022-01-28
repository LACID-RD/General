import random
import numpy as np
import pandas as pd
# def lists():
#     counter = 0
#     counterList = []
#     for i in range(20):
#         counter += 1
#         counterList.append(counter)
#         #print(counter)
#     print(counterList)

#     numList = []
#     for n in range(20):
#         num = np.random.rand()
#         numList.append(num)
#     print(numList)
#     return counterList,numList
# #counterList, numList = lists()
counterList = [1,2,3,4,5,6,7,8,9,10]
numList = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]

# print(len(counterList) == len(numList))

# def getLists(cList,nList):
#     for item in nList:
#         if 0.2 < item < 0.5:
#             x = nList.index(item)
#             nList.pop(x)
#     return nList


# #getLists(counterList, numList)
union = [counterList,numList]
mat = np.dstack(union)
# #print(mat)


# m,n = 0,0
# shape = np.shape(mat)
# mat = np.reshape(mat, (shape[1],shape[2]))

# #print(mat)
# newShape = np.shape(mat)

# for m in range(newShape[0]):
#     for n in range(newShape[1]):
#         if mat[:][n] < 0.5:
#             np.delete((mat),mat[:][n])
# print(mat)


# def pandaMatrixManipulator(array,lowboundry,highboundry):
#     shape =np.shape(array)
#     array = np.reshape(array, (shape[1], shape[2]))
#     columns = ["imgNum", "porcentage"]
#     df = pd.DataFrame(array,columns=columns)
#     df = df[(df.porcentage > lowboundry) & (df.porcentage < highboundry)]
#     matrix = df.to_numpy()
#     return matrix


# pandaMatrixManipulator(mat)





# i = 0
# z = 1227
# theList = np.array([i for i in range(1,z + 1)])
# print(len(theList))
# print(theList)
# print(np.shape(np.vstack(theList)))

porcentageData = np.array(np.vstack([i for i in range(50,101)]))
#print(np.shape(porcentageData))

resampledMatrix = np.ones((500,100,100))
shaper = (np.shape(resampledMatrix))

zList = np.array(np.vstack([i for i in range(shaper[0])]))
#print(np.shape(zList))

ref = porcentageData[:, 0]
#print(np.shape(ref))
#print(type(ref))
ref = list(ref)
#print(np.shape(ref))
#print(type(ref))
#print(ref)


# indexL = (reference[x])
# string = [str(indexL) for n in indexL]
# aString = "".join(string)
# index = int(aString)

def imageEliminator(porcentageData,resampledMatrix):
    i, x, n = 0, 0, 0
    matList = []

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
    
    return matrix
    



imageEliminator(porcentageData,resampledMatrix)