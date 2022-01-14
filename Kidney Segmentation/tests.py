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


def pandaMatrixManipulator(array,lowboundry,highboundry):
    shape =np.shape(array)
    array = np.reshape(array, (shape[1], shape[2]))
    columns = ["imgNum", "porcentage"]
    df = pd.DataFrame(array,columns=columns)
    df = df[(df.porcentage > lowboundry) & (df.porcentage < highboundry)]
    matrix = df.to_numpy()
    return matrix


pandaMatrixManipulator(mat)
