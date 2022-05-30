import matplotlib.pyplot as plt
import pydicom
import tkinter as tk
from tkinter import filedialog
import numpy as np
import sys 
import collections
import cv2 as cv
from scipy import stats



# Allows to select one general ROI wich can be use in every image.

def position_ROI(Dcm_im_ROI):
    '''
    Give the general position of the ROI used to be copy on every image

    '''
    Dcm_im8 = (Dcm_im_ROI/256).astype(np.uint8)
    Dcm_im8 = cv.applyColorMap(Dcm_im8,cv.COLORMAP_BONE)
    showCrosshair = False
    r = cv.selectROI("Seleccione el ROI a analizar", Dcm_im8,showCrosshair)
    return r

def Img_filter(Dcm_im):
    
    '''
    Filter the confidence map

    '''
    Neighbor = 1
    imax,jmax=Dcm_im.shape
    I,J=np.where(Dcm_im == 0) 
    Conditional=np.logical_and(np.logical_and(imax-Neighbor>I, Neighbor<=I), np.logical_and(jmax-Neighbor>J, Neighbor <=J))
    I= I[Conditional]
    J= J[Conditional]
    np.set_printoptions(threshold=sys.maxsize)     
    for i in range (len(I)):
        Dcm_im[I[i]-Neighbor:I[i]+Neighbor,J[i]-Neighbor:J[i]+Neighbor] = 0
        Dcm_im[I[i],J[i]-Neighbor]=0
        Dcm_im[I[i],J[i]+Neighbor]=0
    return Dcm_im

#ROI

def img_ROI(Dcm_final, general_ROI): 
    '''
    Crop the image used the position given by position_ROI

    '''  
    imCrop = Dcm_final[int(general_ROI[1]):int(general_ROI[1]+general_ROI[3]), int(general_ROI[0]):int(general_ROI[0]+general_ROI[2])]
    plt.imshow(imCrop, cmap = plt.cm.bone)
    plt.title('ROI selected')
    plt.show()
    # cv.imshow("Usted selecciono este ROI", imCrop)
    #cv.waitKey(0)
    cv.destroyAllWindows()
    return imCrop


root = tk.Tk()
root.withdraw()

file_name = filedialog.askopenfilenames()


amplitud = []
sequences = []


for i in file_name:

    Dcm = pydicom.dcmread(i)
    Dcm_im = np.copy(Dcm.pixel_array)
    # Dcm_im2 = np.copy(Dcm.pixel_array)  Try if mask - nomask = 0
    print('Name:',i)
    print('\n N° of pixels of this image is:', np.sum(Dcm_im > 0))    #np.sum(Dcm_im > 0) return sum of true or false 
    plt.imshow(Dcm_im, cmap = plt.cm.bone)
    plt.show()
    amplitud.append(np.sum(Dcm_im>0))
    sequences.append(i)
    print('Image MRE (0-8 kPa) with no mask:\n ')
    Img_filter(Dcm_im)
    plt.imshow(Dcm_im, cmap = plt.cm.bone)
    plt.title('No mask image')
    plt.show() 
    #print(Dcm)
    print('\n\n')

print('------------------------------------------------------------------------------------')    
print('\n\nThe maximum value of pixel is: ' , max(amplitud))
print('\nThe image with the largest area is: ', sequences[amplitud.index(max(amplitud))] )
print('\n\n------------------------------------------------------------------------------------\n\n') 



# Muestra valores repetidos.

repeticion = collections.Counter(amplitud)
a= list(repeticion.values())

for z in a:
    if z != 1:
            print('WARNING...')
            print('-----------------------------------------------')
            print('Repeated values')
            print('\n', repeticion)
            print('-----------------------------------------------')
    

#  Filter all the neighbors of any pixel, [I,J] runs every position where the condition of Dcm_im=0. Then conditional
# delete all the corners of the image where I rows and J columns were going to have problems to been delete bc there is
# no neighbors there. For loop is just run in "I" bc i goes for every element of I (every rows) from 0 to 255
# then I[i] and J[i] runs for every row and column.



# def Img_filter(Dcm_im):
#     Neighbor = 1
#     imax,jmax=Dcm_im.shape
#     I,J=np.where(Dcm_im == 0)  #Le da a I y J solo las posiciones donde los el valor de pixel vale cero
#     Conditional=np.logical_and(np.logical_and(imax-Neighbor>I, Neighbor<=I), np.logical_and(jmax-Neighbor>J, Neighbor <=J))
#     I= I[Conditional]
#     J= J[Conditional]
#     np.set_printoptions(threshold=sys.maxsize)     
#     for i in range (len(I)):
#         Dcm_im[I[i]-Neighbor:I[i]+Neighbor,J[i]-Neighbor:J[i]+Neighbor] = 0
#         Dcm_im[I[i],J[i]-Neighbor]=0
#         Dcm_im[I[i],J[i]+Neighbor]=0
#     return Dcm_im

# print('Image MRE (0-8 kPa) with no mask:\n ')
# Img_filter(Dcm_im)
# plt.imshow(Dcm_im, cmap = plt.cm.bone)
# plt.title('No mask image')
# plt.show() 
# print('\n\n')

# Try if mask - nomask = 0 show if the pixels in prostate has same value

# plt.imshow(Dcm_im2, cmap = plt.cm.bone)
# plt.show() 
# imgresta = Dcm_im2 - Dcm_im
# plt.imshow(imgresta, cmap = plt.cm.bone)
# plt.show() 

root = tk.Tk()
root.withdraw()

file_name_ROI = filedialog.askopenfilename()
Dcm_ROI = pydicom.dcmread(file_name_ROI)
Dcm_im_ROI = np.copy(Dcm_ROI.pixel_array)
Img_filter(Dcm_im_ROI)
    
general_ROI = position_ROI(Dcm_im_ROI)

# print('ROI selected from MRE (0-8 kPa) with no mask: \n')
# Final_ROI=img_ROI(Dcm_im,general_ROI)
# print('\n\n')

amplitud_ROI = []
sequences_ROI = []
final_image = []


for item in file_name:
    Dcm_item = pydicom.dcmread(item)
    Dcm_im_item = np.copy(Dcm_item.pixel_array)
    Dcm_final = Img_filter(Dcm_im_item)
    print('ROI selected from MRE (0-8 kPa) with no mask: \n')
    print('Name:',item)
    Final_ROI=img_ROI(Dcm_final,general_ROI)
    print('\n N° of pixels of this image is:', np.sum(Final_ROI > 0))
    print('\n\n')
    amplitud_ROI.append(np.sum(Final_ROI>0))
    sequences_ROI.append(item)
    final_image.append(Final_ROI)


print('------------------------------------------------------------------------------------')    
print('\n\nThe maximum value of pixel is: ' , max(amplitud_ROI))
print('\nThe image with the largest area is: ', sequences[amplitud_ROI.index(max(amplitud_ROI))] )
print('\n\n------------------------------------------------------------------------------------\n\n') 


#print(final_image[0])


omega = int(input('Seleccione cantidad de frecuencias/amplitudes a analizar de menor a mayor:'))

w_total = []

for _ in range(omega):
    valores_frecuencia = int(input('Introduzca los valores de las frecuencias:'))
    w_total.append(valores_frecuencia)

w = np.asarray(w_total)
print(w_total)

img_shape = final_image[0].shape

newmap1 = np.zeros(img_shape)
newmap2 = np.zeros(img_shape)

for i in range(img_shape[0]):
    for j in range (img_shape[1]):
        x = []
        # print('linear regression:')
        for k in range(len(w)):
            x.append(final_image[k][i,j])
        # plt.scatter(w,x)
        # plt.show()  
        if 0 in x:
            newmap1[i,j] = 0
            
        else:
            slope, intercept, r_value, p_value, std_err = stats.linregress(w,x)
            def predict_y_for(w):
                return slope * w + intercept

            # plt.scatter(w,x)
            # plt.plot(w, predict_y_for(w), c='r')
            # plt.show()
            newmap1[i,j] = r_value**2
            
for i in range(img_shape[0]):
    for j in range (img_shape[1]):
        x = []
        # print('linear regression:')
        for k in range(len(w)):
            x.append(final_image[k][i,j])
        # plt.scatter(w,x)
        # plt.show()  
        if 0 in x:
            newmap2[i,j] = 0
            
        else:
            slope, intercept, r_value, p_value, std_err = stats.linregress(w,x)
            predict_y_for(w)
                

            # plt.scatter(w,x)
            # plt.plot(w, predict_y_for(w), c='r')
            # plt.show()
            newmap2[i,j] = slope
        

# print(newmap1)
plt.imshow(newmap1, cmap = plt.cm.bone)
plt.title('Final Map[r^2]')
plt.show()

# print(newmap2)
plt.imshow(abs(newmap2), cmap = plt.cm.bone)
plt.title('Final Map[abs(slope)]')
plt.show()

