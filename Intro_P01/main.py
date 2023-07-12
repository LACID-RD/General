##########################
## PROGRAMA INTRODUCTORIO

## Librerias
import matplotlib.pyplot as plt
import matplotlib.pyplot as htt
import pydicom
import tkinter as tk
from tkinter import filedialog
import numpy as np
import sys

###################################
####### Manipula una imagen
##################################

def ImgMan(PathImg):

    print("Path:",PathImg)                  #Imprime el path
    DCMHead=pydicom.dcmread(PathImg)        #Lee header DICOM
    ReadDC(DCMHead)                         #Llama funcion ReadDC     
    #print(DCMHead)                          #Imprime header DICOM
    DataImg=np.copy(DCMHead.pixel_array)    #Se extrae datos de la imagen
    plt.imshow(DataImg, cmap = "bone")      #Se imprime arreglo
    plt.show()
    htt.hist(DataImg.ravel(),'sqrt')        #Se calcula histograma
    htt.xlim(1,800)
    htt.ylim(0,3000)
    htt.show()  


###################################
####### Lee caracteristicas DICOM
##################################

def ReadDC(ffImg):
    ffReDC=[]
    ffReDC.append(ffImg[0x0008,0x0060].value) # 0:Modalidad
    if "MR" in ffReDC[0]:
        ffReDC[0]=ffReDC[0]
    else:
        print("Error 4: Las imágenes no son de MR.")
        sys.exit(4)
    ffReDC.append(ffImg[0x0008,0x0070].value) # 1:Fabricante
    ffReDC.append(ffImg[0x0008,0x1090].value) # 2:Modelo
    ffReDC.append(ffImg[0x0018,0x0080].value) # 3:Tr
    ffReDC.append(ffImg[0x0018,0x0081].value) # 4:Te
    print("DICOM Features:",ffReDC)


###################################
####### Funcion principal
##################################

def main():
    
    value=input("Ingrese 0 para seleccionar imagen o 1 por path:\n"); value=int(value)
    if value==1:
        #Escriba aca el path
        PathImg="C:/Users/Daniel/Desktop/VCode/Projects/LACID/Lumbar_Spine.dcm"
        ImgMan(PathImg)
    elif value==0:
        DiaWind=tk.Tk()                             #Define objeto DiaWind de la clase Tk
        DiaWind.withdraw()                          #Ejecuta función withdraw de la calse Tk
        #Genera tuple con todos los path's
        PathTup=filedialog.askopenfilenames(filetypes= [('image','dcm')],title="DICOM")
        #Warning si no se abre alguna imagen
        StrgEmp=""                  
        if PathTup is StrgEmp:
            print("Error: No seleccionó directorio."); sys.exit(0)
        for i in PathTup:                           #Lee los paths de la tuple
            ImgMan(i)
    else:
        print("Es joda ??, Lea bien !!."); sys.exit(0)


###################################
####### INICIA PROGRAMA
##################################

if __name__ == '__main__':
    main()
