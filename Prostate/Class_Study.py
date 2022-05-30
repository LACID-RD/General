#from gdcm.gdcmswig import Object
import pydicom
import tkinter as tk
from tkinter import filedialog
import numpy as np
import operator 
from collections import Counter
import gdcm
import sys
import os
from Class_Image import CImage

class CStudy():

    ########################################
    # Busca imágenes y filtra las DCM
    ########################################

    def load_img(self):
        #Abre cuadro de diálogo y pregunta path del folder
        cuadro=tk.Tk()
        cuadro.withdraw()
        FolPath=filedialog.askdirectory(title="DICOM Images")
        #Warning si no se abre algún folder
        StringVacio=""
        if FolPath is StringVacio:
            print("Error: No seleccionó directorio.")
            sys.exit(0)
        return FolPath

    ########################################
    # Guarda características de las imagenes
    ########################################

    def read_img(self,PathAux):
        Img_list,m=[],0
        for root,dirs,files in os.walk(PathAux):
            for i in files:
                if i.endswith(".dcm"):
                    PathAux=os.path.join(root,i)                  #Lee path de cada imagen
                    Img1=CImage(PathAux)
                    Img1.DescomDicom()
                    Img1.ReaderDicom()
                    Img_list=Img1.SortDicom()
                    print(Img_list)
                    #print(Img1.capture_type, Img1.tr_syn, Img1.modality, Img1.mnfcr, Img1.tr, Img1.te, Img1.seq_type, Img1.sl_thick, Img1.ext_field, Img1.phase_cod, Img1.acq_number, Img1.im_number, Img1.stack_id, Img1.n_of_rows, Img1.n_of_cols)
                    m+=1


#     root = tk.Tk()
#     root.withdraw()

#     file_name = filedialog.askopenfilenames()

#     Dcm_todo = []
       
#     for i in file_name:
#         Dcm = pydicom.dcmread(i)
#         Dcm_todo.append(Dcm)

#     print('Total de archivos Dicom cargadas:', len(Dcm_todo))
#     return Dcm_todo    

    # def loadimagesProstate(self):    
    #     root = tk.Tk()
    #     root.withdraw()

    #     file_name = filedialog.askopenfilenames()

    #     Dcm_prostate = []

        # for i in file_name:
        #     Dcm = pydicom.dcmread(i)
        #     Dcm_prostate.append(Dcm)

        # print('Total de archivos Dicom cargadas:', len(Dcm_prostate))
        # return Dcm_prostate
 
###IMPRIMIR DICOM###
# imagenes = Patient()
# print(imagenes.loadimages())
###################

# class Brain(Patient):
#     pass

# class Prostate(Patient):
#     def __init__(self,bvalue):
#         self.bvalue=bvalue

# class Liver(Patient):
#     pass

    #print(Dcm)

    #class imginfo:

    #    def __init__(self, name, age):
    #        self.name = name
    #        self.age = age

    #    def info(self, Dcm_todo):
    #        print('Patient name:' , )

            
#    def info(Dcm_todo):
#        for x in range(len(Dcm_todo)): 
#            print('Patient name:' , Dcm_todo[x][0x0010,0x0010].value)
#            print('Scanner:' , Dcm_todo[x][0x0008,0x0070].value)
#            print('Patient name:' , Dcm_todo[x][0x0010,0x0010].value)

