import matplotlib.pyplot as plt
from numpy.lib.npyio import save
import pydicom
import tkinter as tk
from tkinter import filedialog
import numpy as np
import collections
from scipy.optimize import least_squares
import gdcm
import sys
import cv2 as cv
from PIL import Image
from skimage.color import gray2rgb
from skimage import color
from skimage.util import img_as_ubyte,img_as_float
import tempfile
import pandas as pd
import math
import SimpleITK as sitk
from lmfit import Model

def decompress(Dcm_file):
    '''
    Decompress DICOM compressed files
    '''
    conerr=0
    file = Dcm_file
    reader=gdcm.ImageReader()
    reader.SetFileName(file)
    if not reader.Read():
        print("Error",conerr,": No se leen correctamente las imágenes.")
        sys.exit(1)
    conerr+=1
    change = gdcm.ImageChangeTransferSyntax()
    change.SetTransferSyntax( gdcm.TransferSyntax(gdcm.TransferSyntax.ImplicitVRLittleEndian) )
    change.SetInput( reader.GetImage() )
    if not change.Change():
        print("Error",conerr,": No se descomprime correctamente las imágenes.")
        sys.exit(2)
    conerr+=1
    writer = gdcm.ImageWriter()
    writer.SetFileName(file)
    writer.SetFile(reader.GetFile())
    writer.SetImage(change.GetOutput())
    if not writer.Write():
        print("Error",conerr,": No se escriben correctamente las imágenes.")
        sys.exit(3)
    conerr+=1
    return Dcm_file

def Reader(fimg):
    '''
    Reads DiCOM files specific  information 
    '''
    ffReDC=[]
    ffReDC.append(fimg[0x0008,0x0060].value) # 0:Modalidad
    if "MR" in ffReDC[0]:
        ffReDC[0]=ffReDC[0]
    else:
        print("Error 4: Las imágenes no son de MR.")
        sys.exit(4)
    ffReDC.append(fimg[0x0008,0x0070].value)# 1:Fabricante
    ffReDC.append(fimg[0x0018,0x0080].value) # 2:Tr
    ffReDC.append(fimg[0x0018,0x0081].value) # 3:Te
    ffReDC.append(fimg[0x0018,0x0020].value)# 4:Tipo de sec 
    ffReDC.append(fimg[0x0018,0x0087].value) # 5:Campo Externo
    #ffReDC.append(fimg[0x0020,0x9056].value) # Stack ID
    try:
        ffReDC.append(fimg[0x0018,0x9087].value) #6:b-value (CASO PARTICULAR PORQUE NO ESTA SIEMPRE)
    except:
        ffReDC.append(0.0)
    #ffReDC.append(fimg[0x2001,0x1020].value)
       # Valor de B
                                               #9:Scaning Seq
    ffReDC.append(fimg[0x020,0x011].value)      #7:series number, lo voy a tener que hacer por fuera
    ffReDC.append(fimg[0x0028,0x0010].value)   #8:Num de filas
    ffReDC.append(fimg[0x0028,0x0011].value)   # 9:Num de colum 
    ffReDC.append(fimg[0x0008,0x103e].value)  #10:Series description  
    listimtype=fimg[0x0008,0x0008].value
    imgtype = list(filter(lambda x: 'ADC' in x, listimtype))
    ffReDC.append(imgtype)                  #11:tipo de imagen 
    if "SIE" in ffReDC[1]:
        ffReDC.append(fimg[0x0020,0x0032].value)# 12:Slice
        # ffReDC.append(fimg[0x0020,0x0037].value)
        # ffReDC.append(fimg[0x0028,0x0030].value)
        if 'Sag' in str(fimg[0x0008,0x103e].value):
            corte='SAGITAL'
            ffReDC.append(corte)               #13: AXIAl/SAGITAL/CORONAL
        elif 'Cor' in str(fimg[0x0008,0x103e].value):
            corte='CORONAL'
            ffReDC.append(corte)
        else:
            corte='AXIAL'
            ffReDC.append(corte)
    elif "GE" in ffReDC[1]:
        ffReDC.append(fimg[0x0020,0x0032].value)
        # ffReDC.append(fimg[0x0018,0x9087].value)
        if 3.0 == ffReDC[5]:
            out=fimg[0x0043,0x1039].value
            out1=str(out)
            out2=list(out1)
            #print('como es esto',int(out2[2]))
            if int(out2[2]) ==0:
                #print('ingresa aca')
                x1=0
                ffReDC.insert(6,x1)
            else:
                x1=int(out2[11])+10*int(out2[10])+100*int(out2[9])+1000*int(out2[8])
                ffReDC.insert(6,x1)

        # ffReDC.append(fimg[0x0020,0x0037].value)
        # ffReDC.append(fimg[0x0028,0x0030].value)
        #FALTAN 10 Y 11
        if 'Sag' in str(fimg[0x0008,0x103e].value):
            corte='SAGITAL'
            ffReDC.append(corte)
        elif 'Cor' in str(fimg[0x0008,0x103e].value):
            corte='CORONAL'
            ffReDC.append(corte)
        else:
            corte='AXIAL'
            ffReDC.append(corte)
    elif "Phil" in ffReDC[1]:
        ffImPo2=fimg[0x5200,0x9230][0]
        ffImPo1=ffImPo2[0x0020,0x9113][0]
        ffReDC.append(ffImPo1[0x0020,0x0032].value)
        #ffReDC.append(fimg[0x0018,0x9087].value)#colocobvalue
        # ffSFGS=fimg[0x5200,0x9229][0]
        # ffImOr1=ffSFGS[0x0020,0x9116][0]
        # ffReDC.append(ffImOr1[0x0020,0x0037].value)
        corte=fimg[0x2001,0x100b].value
        ffReDC.append(corte)
        #print("SlsOri: ",SliOri)
        #ScaTec=fimg[0x2001,0x1020].value
        #ffReDC.append(ScaTec)
        #print("ScaTec: ",ScaTec)
        # ffPiSp1=ffSFGS[0x0028,0x9110][0]
        # ffReDC.append(ffPiSp1[0x0028,0x0030].value)
    else:
        print("Error 5: Las imágenes no son de equipos Philips, ni GE, ni Siemens.")
        sys.exit(5)
    ffReDC.append(fimg[0x0020,0x0013].value) #14:orden
    # print(ffReDC)
    return ffReDC


def position_ROI(Dcm_im_ROI):
    '''
    Give the general position of the ROI used to be copy on every image
    '''
    Dcm_im8 = (Dcm_im_ROI).astype(np.uint8)
    Dcm_im8 = cv.applyColorMap(Dcm_im8,cv.COLORMAP_BONE)
    showCrosshair = False
    r = cv.selectROI("Seleccione el ROI a analizar", Dcm_im8,showCrosshair)
    print("Coordenadas del ROI:",r)
    return r

def img_ROI(Dcm_final, general_ROI): 
    '''
    Crop the image used the position given by position_ROI
    '''  
    imCrop = Dcm_final[int(general_ROI[1]):int(general_ROI[1]+general_ROI[3]), int(general_ROI[0]):int(general_ROI[0]+general_ROI[2])]
    plt.imshow(imCrop, cmap = plt.cm.bone)
    plt.title('ROI selected')
    plt.show()
    cv.destroyAllWindows()
    return imCrop


#####funcion para el b-value en el 3T
def bvalue(ffdicom):
    out1=str(ffdicom)
    out2=list(out1)
    if int(out2[2]) ==0:
            #print('ingresa aca')
        x1=0
    else:
        x1=int(out2[11])+10*int(out2[10])+100*int(out2[9])+1000*int(out2[8])
    return x1

