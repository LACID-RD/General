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
from Class_Image import CImage
#from Class_Serie import CSerie
from Class_Study import CStudy
import Funcn_Proce

#############################
#############################
# CLASS CLoadI 01-
#############################
#############################
class CLoadI():

    Instanc=[]

    ###############
    # 01-Define variables de la clase
    ###############

    def __init__(self,resolution): #pat_name=None,type=0,time=0,slice=0,img=None,te=0,tr=0,

        CLoadI.Instanc.append(self)
        self.AllStud=[]
        self.pathFol=-4
        self.Studies=[]                                 #Etiqueta la cantidad de estudios del paciente
        self.resolution=resolution

    ###############
    # 02-Busca el path del folder de las imágenes
    ###############
    #opt 0: Cuadro de diálogo
    #opt 1: Ingreso manual
    #opt 2: Ingreso por script (terminal)
    #opt 3: Ingreso por esta función (python) 
    #opt other: Ingreso por tabla ubicada en el main
    #           opt: excel/main, path_aux: files
    
    def CL_load_img(self, opt, path_aux):

        # Define path
        if opt == 0:
            # Open dialog box and ask for folder path
            dialog_win = tk.Tk(); dialog_win.withdraw()
            self.pathFol = filedialog.askdirectory(title = "DICOM Folder")
            if not self.pathFol:
                label_log = "01-01-01 Error: No selecciono directorio"  
                Funcn_Proce.FP_error_log(0, label_log)
        elif opt == 1: 
            self.pathFol = input("Ingrese el path donde se encuentran las imagenes:")
        elif opt == 2: 
            self.pathFol = sys.argv[1]
        elif opt == 3: 
            self.pathFol = path_aux
        else:        
            path_excel = Path(opt) / "tabla.xlsx"
            var_df = pd.read_excel(path_excel) # Load the Excel file
            # Print the entire DataFrame
            print(var_df)
            study = int(input("Ingrese el numero de un estudio: "))
            row = var_df.loc[var_df['Num'] == study] # Find the value in a specific column
            # Read another value from the same row
            self.pathFol = Path(path_aux) / row['Mod'].values[0] / row['Pat'].values[0]
        
        # Check if the path contains DICOM images
        varAux1 = 0
        for root, dirs, files in os.walk(self.pathFol):
            for file in files:
                if file.endswith(".dcm"):
                    varAux1 = 1; break
        if varAux1 == 0:
            label_log = "01-01-02 Error: Path de las imagenes incorrecto"  
            Funcn_Proce.FP_error_log(0, label_log)
        else: print("Leyendo imágenes...")
        self.CL_organ_img()
        return None

    ###############
    # 03-Organiza imágenes en estudios y series
    ###############

    def CL_organ_img(self):
        cont0 = 0
        # Se cuentan las imagenes DICOM en la carpeta
        for root, dir, files in os.walk(self.pathFol):
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
                    if IdenStu not in self.Studies:
                        self.Studies.append(IdenStu)
                        varAux0 = len(self.Studies) - 1
                        # Se registra UNA UNICA VEZ el estudio
                        self.AllStud.append(CStudy(ObjtImg, IdenStu, varAux0, self.resolution))
                    # Pregunta si existe la serie, si no, la genera
                    for j in self.AllStud: #Llena las series con sus imagenes
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
            [i.CY_img_order(-2) for i in self.AllStud]
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
        for i in self.AllStud: i.CYSrAnPCs()
    '''