#from ntpath import join
#from operator import ne
#import shelve
#import pydicom
#from collections import Counter
#import gdcm
#import pandas as pd
#from scipy import ndimage,misc,signal
#from itertools import repeat
#from scipy.stats.stats import pearsonr
#import cv2
import math
#import matplotlib.pyplot as plt
#import numpy as np
import os
import pandas as pd
from pathlib import Path
import sys
from tkinter import filedialog
import tkinter as tk
### Local libraries
#from Class_Image import CImage
#from Class_Serie import CSerie
#from Class_Study import CStudy
#import Funcn_Proce

class ClassLoadImage():
    """
    Class that loads, organizes and manipulates a group of images.
    
    :param resol_int: Number of intensity levels in which the images will be processed.
    :type resol_int: int
    """

    Instanc=[]

    def __init__(self, resol_int: int = 1024):
        """
        This is the constructor function.

        :param resol_int: Number of intensity levels in which the images will be processed
        :type resol_int: int
        """
        ClassLoadImage.Instanc.append(self)
        self.studies = []
        self.path_folder = "none"
        self.study_label = []
        self.resol_int = resol_int

    def folder_path(self, code: int, error_log, path_aux = "none"):
        """
        Function that defines the path of the DCM images folder
        :param code: path by 1) path_aux, 2) python input, 3) sys.argv[1], 4) dialog box, 5) excel List.xlsx
        :type code: int
        :param error_log: Object from ClassErrorLog
        :param path_aux: default) none, folder path (code=1) or excel file path (code=5)
        """
        
        if code == 1: pass 
        elif code == 2: 
            path_aux = input("Ingrese el path donde se encuentran las imagenes: ")
        elif code == 3:
            path_aux = sys.argv[1]
        elif code == 4:
            path_aux = filedialog.askdirectory(title = "DICOM Folder")
            if not path_aux:
                line_log = "01-01-01 Error: No selecciono directorio"  
                error_log.write(0, line_log)
        elif code == 5:
            read_list = pd.read_excel(path_aux) # Load the Excel file
            # Print the entire DataFrame
            print(read_list)
            study_line = int(input("Ingrese el numero de un estudio: "))
            print("Sline:",study_line,type(study_line))
            row_number = read_list.ID[read_list['Number'] == study_line] # Find the value in a specific column
            # Read another value from the same row
            print(row_number)
            #self.folder_path = Path(path_aux) / row['Mod'].values[0] / row['Pat'].values[0]
        
        
        
        #self.folder_path = path_aux
        self.path_folder = Path(path_aux)

        # Check if the path contains DICOM images
        found_dcm = False
        for root, dirs, files in os.walk(self.path_folder):
            for file in files:
                if file.endswith(".dcm"):
                    found_dcm = True
                    break
        if found_dcm:
            line_log = "load_folder: Path de las imagenes incorrecto"

        else:
            print("Leyendo imágenes...")
        #self.CL_organ_img()
        return None
    
    """
    ###############
    # 03-Organiza imágenes en estudios y series
    ###############

    def CL_organ_img(self):
        cont0 = 0
        # Se cuentan las imagenes DICOM en la carpeta
        for root, dir, files in os.walk(self.folder_path):
            for i in files:
                if i.endswith(".dcm"):
                    if math.fmod(cont0, 1000) == 0 and cont0 > 1:
                        print("Número de imágenes analizadas:", cont0)
                    auxPath = os.path.join(root,i)
                    # Extraen características de cada imagen
                    ObjtImg = CImage(auxPath)
                    ObjtImg.CDMDcmFeat()
                    ObjtImg.D00ReNu = cont0
                    # Pregunta si existe el estudio, si no, la genera
                    IdenStu = [] #Vector con nombre paciente y Study Time/Accession Number
                    IdenStu.extend((ObjtImg.D01Name, ObjtImg.D01StTm))
                    if IdenStu not in self.study_label:
                        self.study_label.append(IdenStu)
                        varAux0 = len(self.study_label) - 1
                        # Se registra UNA UNICA VEZ el estudio
                        self.studies.append(CStudy(ObjtImg, IdenStu, varAux0, self.resol_int))
                    # Pregunta si existe la serie, si no, la genera
                    for j in self.studies: #Llena las series con sus imagenes
                        if IdenStu == j.Identif:
                            j.CY_serie_found(ObjtImg)
                    cont0 += 1
        print("Número total de imágenes:",cont0)
        return None

    ###############
    # 04-Ordena las imagenes por posicion y
    #    carga en matrices las imagenes
    ###############
    # code: -2 (all studies)

    def CL_img_order(self, code):
        
        print("Ordenando y cargando imagenes...")
        if code == -2:
            [i.CY_img_order(-2) for i in self.studies]
        else:
            label_log = "01-04-01 Error: FALTA PROGRAMAR"
            Funcn_Proce.FP_error_log(0, label_log)     
        return None

    '''
    ###############
    # Busca imagenes de PC (4DF,DWI,MRE)
    ###############

    def CLImagePC(self):

        print("Buscando imagenes PC")
        for i in self.studies: i.CYSrAnPCs()
    '''
    """