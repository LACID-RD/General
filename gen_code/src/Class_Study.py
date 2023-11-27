#from ntpath import join
#from operator import ne
#import shelve
#import pydicom
#import tkinter as tk
#from tkinter import filedialog
#import gdcm
#import os
#import pandas as pd
#import math
#from scipy import ndimage,misc,signal
#from itertools import repeat
#from scipy.stats.stats import pearsonr
#from Class_Image import CImage
#from math import comb
#import cv2
import matplotlib.pyplot as plt
from collections import Counter
import cv2
import numpy as np
import sys
# Local libraries
from Class_Image import CImage
from Class_Serie import CSerie
import Funcn_Proce

#############################
#############################
# CLASS CStudy 02-
#############################
#############################

class CStudy():

    Instanc=[]

    ###############
    # 01-Define variables de la clase
    ###############

    def __init__(self, StImRef, IdenStu, StuItem, resolution):
        
        CStudy.Instanc.append(self)
        self.StImRef = StImRef # Imagen de ref para llenar features
        self.Identif = IdenStu # D01Name,D01StTm de la img ref
        self.StuItem = StuItem # Indexado de estudio
        self.AllSers = [] # OBJETOS SERIES
        self.SeNuLst = [] # Numeros de serie
        self.resolution = resolution
        #print(self.StuList,self.StuPath)

    ###############
    # 02-Encuentra número de series originales y
    #    las caracteriza; ObjtImg es cada imagen
    ###############

    def CY_serie_found(self, ObjtImg):
        
        #Si no encuentra la serie, la genera
        if ObjtImg.D02SeNu not in self.SeNuLst:
            self.SeNuLst.append(ObjtImg.D02SeNu)
            var_aux0 = len(self.SeNuLst)-1
            self.AllSers.append(CSerie(ObjtImg.D02SeNu, self.StuItem, var_aux0, self.resolution))
            # Asigna features a las series e imprime a partir
            # de UNA SOLA imagen. [-1]:Ultimo elemento
            self.AllSers[-1].CSRCopFea(ObjtImg, 0)
        #Busca la serie para colocar la imagen
        for i in self.AllSers:
            if ObjtImg.D02SeNu == i.S02SeNu: # Llena la serie con sus imagenes
                i.AllImag.append(ObjtImg)
                ObjtImg.StuItem = i.StuItem
                ObjtImg.SerItem = i.SerItem
        return None     

    ###############
    # 03-QA de geometria entre series
    ###############
    #serie_array: Array de series a comparar
    '''
    def CY_geom_qa(self, serie_array):
        var_error = 0; vMinRes = 0

        # Verifica geometria
        for i in serie_array:
            for j in serie_array:
                var_aux1 = self.AllSers[i].S04SlTk/self.AllSers[j].S04SlTk
                var_aux2 = self.AllSers[i].S04RwNb*self.AllSers[j].S04ClNb/(self.AllSers[i].S04ClNb*self.AllSers[j].S04RwNb)
                var_aux3 = self.AllSers[i].AllImag[0].D04Slic*self.AllSers[i].AllImag[1].D04Slic/(self.AllSers[j].AllImag[0].D04Slic*self.AllSers[j].AllImag[1].D04Slic)
                var_aux4 = len(self.AllSers[i].AllImag)/len(self.AllSers[j].AllImag)
                if var_aux1 != 1 or var_aux2 != 1 or var_aux3 != 1 or var_aux4 != 1:
                    var_error = 1
        
        # Menor resolucion espacial
        if var_error == 0:
            for i in range(len(serie_array)):
                if self.AllSers[serie_array[i]].S04RwNb<self.AllSers[serie_array[vMinRes]].S04RwNb: vMinRes = i
        vMinRes = serie_array[vMinRes]
        return var_error, vMinRes
    '''
    def CY_geom_qa(self, serie_array):
        var_error = 0
        vMinRes = 0
        print("VERIFICAR !!!!!  CY GEOM")
        # Verifica geometria
        for i in serie_array:
            for j in serie_array:
                var_aux1 = self.AllSers[i].S04SlTk/self.AllSers[j].S04SlTk
                var_aux2 = self.AllSers[i].S04RwNb*self.AllSers[j].S04ClNb/(self.AllSers[i].S04ClNb*self.AllSers[j].S04RwNb)
                var_aux3 = self.AllSers[i].AllImag[0].D04Slic*self.AllSers[i].AllImag[1].D04Slic/(self.AllSers[j].AllImag[0].D04Slic*self.AllSers[j].AllImag[1].D04Slic)
                var_aux4 = len(self.AllSers[i].AllImag)/len(self.AllSers[j].AllImag)
                if any(aux != 1 for aux in [var_aux1, var_aux2, var_aux3, var_aux4]):
                    var_error = 1
                    break
            if var_error:
                break

        # Menor resolucion espacial
        if not var_error:
            vMinRes = min(serie_array, key=lambda x: self.AllSers[x].S04RwNb)

        return var_error, vMinRes

    ###############
    # 04-Ordena las imagenes por posicion y
    #    carga en matrices las imagenes
    ###############
    # code: -2 (all series)

    def CY_img_order(self, code):
        if code == -2:
            [i.CS_img_order() for i in self.AllSers]
        else:
            label_log = "02-04-01 Error: FALTA PROGRAMAR"
            Funcn_Proce.FP_error_log(0, label_log)
        return None

    ###############
    # 05-Imprime info del estudio
    ###############

    def CYPrtInfo(self):

        if self.StImRef != -4:
            print("\n************************************\nNombre:", self.StImRef.D01Name, "    Estudio:", self.StImRef.D01StTm)
        else: print("\n************************************\nNombre:", self.StImRef.D01Name)
        if self.StImRef.D01StDc != -4: print("Descripción:", self.StImRef.D01StDc)
        print("Fabricante:", self.StImRef.D01Mnfr, "    Escáner:", self.StImRef.D01MnMd)
        print("Cantidad original de series:", len(self.AllSers),"\n")
        for i in self.AllSers: i.CSPrtInfo()

    #########################
    #########################
    # Altering or modifying series
    #########################
    #########################
    # 06-Genera serie para procesamiento algebraico
    ###############
    # Siempre devuelve una serie con la resolucion espacial mas pequeña
    # 1:Item_Serie1, 2:Item_Serie2, 3:Codigo asignado a la nueva serie (StudLoc)
    # 4:Operacion (0:Se reduce la resolucion de la mas grande,1:sum,2:res
    #     3:mul,4:div,5:ceros mas pequeña). Si la operacion es 0 y las
    #     resoluciones son iguales, devuelve refSer1
    
    def CY_new_serie(self, ref_ser1, ref_ser2, new_seri, operaSr):

        #Se verifica q las series tengan mismo SlTk, dimensiones y localizacion
        serie_array = []
        serie_array.append(ref_ser1)
        serie_array.append(ref_ser2)
        QAa,MinRsSg = self.CY_geom_qa(serie_array)
        if QAa == 1:
            label_log = "02-06-01 Error: No se crea nueva serie por geometria"
            Funcn_Proce.FP_error_log(0, label_log)

        #Llena datos DCM de la serie nueva
        #var_aux1: menor resolucion espacial
        if self.AllSers[ref_ser1].S04RwNb == self.AllSers[ref_ser2].S04RwNb:
            var_aux1 = ref_ser2; var_aux2 = ref_ser1; var_aux3 = 1
        elif MinRsSg == ref_ser1:
            var_aux1 = ref_ser1; var_aux2 = ref_ser2; var_aux3 = 0
        elif MinRsSg == ref_ser2:
            var_aux1 = ref_ser2; var_aux2 = ref_ser1; var_aux3 = 1
        self.SeNuLst.append(new_seri)
        var_aux0 = len(self.SeNuLst)-1
        self.AllSers.append(CSerie(new_seri,self.StuItem,var_aux0,self.resolution)) # Crea serie nueva
        var_aux4 = len(self.AllSers)-1
        var_aux5 = self.AllSers[var_aux1].refImag # Determina imagen de referencia
        self.AllSers[var_aux4].CSRCopFea(var_aux5,1) # Llena las caracteristicas de la nueva serie

        #Calcula la nueva serie
        var_aux5 = self.AllSers[var_aux1].AllImag[0].ImgData.shape # Tamaño de la serie de salida
        if len(self.AllSers[var_aux4].AllImag) > 0:
            label_log = "02-06-02 Error: Conflicto de indexacion al crea nueva serie"
            Funcn_Proce.FP_error_log(0, label_log)
        for i in range(len(self.AllSers[var_aux1].AllImag)): # Para todas las img...
            var_aux6 = self.AllSers[var_aux2].AllImag[i].ImgData # Se iguala a la mas grande
            var_aux6 = cv2.resize(var_aux6,var_aux5)
            if operaSr == 0: pass  # Redimensionar a menor imagen
            elif operaSr == 1: # Sumar
                var_aux6 += self.AllSers[var_aux1].AllImag[i].ImgData; var_aux6 = var_aux6*0.5
            elif operaSr == 2: # Resta
                if var_aux3 == 0: var_aux6 = self.AllSers[var_aux1].AllImag[i].ImgData-var_aux6
                else: var_aux6 -= self.AllSers[var_aux1].AllImag[i].ImgData
                var_aux6 = var_aux6*0.5
            elif operaSr == 3: # Multiplicacion
                var_aux6 *= 0.01*self.AllSers[var_aux1].AllImag[i].ImgData; var_aux6=10*np.sqrt(var_aux6)
            #elif operaSr == 4: # División
            elif operaSr == 5: # Ceros
                var_aux6 = np.zeros(var_aux5,dtype=float)
            ObjtImg = CImage(-1) # Crea objetos de imagen
            #Llena caracteristicas
            ObjtImg.CIRCopFea(self.AllSers[var_aux1].AllImag[i],var_aux6,new_seri,self.StuItem,var_aux4)
            self.AllSers[var_aux4].AllImag.append(ObjtImg)

        #Llena info de las matrices de imagenes y DCM de las imagenes    
        self.AllSers[var_aux4].CSMatImag(1)                              #Carga matrices
        return var_aux4                                                  #Index de la serie nueva

    ###############
    # 07-Elimina una serie
    ###############
    #entry_type: 0 item(AllSers), 1:SerieNumber(SeNuLst)
    
    def CYRmSerie(self, entry_type, data_val):
        
        #Definen variables
        if entry_type == 0:
            vr_allSer = data_val
            vr_serNu = self.SeNuLst[data_val]
        elif entry_type == 1:
            vr_allSer = self.SeNuLst.index(data_val)
            vr_serNu=data_val
        else: raise ValueError("Error: No se elimina serie (CYRmSe).")
        varAllS = self.AllSers[vr_allSer]

        #Se eliminan objetos                                            
        self.AllSers[vr_allSer].CSRmImage(0) # Elimina imagenes
        self.SeNuLst.remove(vr_serNu); self.AllSers.remove(varAllS) # Elimina serie
        var_aux0 = 0
        for i in CSerie.Instanc: # Elimina serie de Instanc
            if var_aux0 > 0: raise ValueError("Error: Repeticion de serie (CYRmSe).")
            if i.StuItem == self.StuItem and i.S02SeNu == vr_serNu:
                CSerie.Instanc.remove(i); var_aux0 += 1

        #Se cambian items de series e imagenes
        for i, serie in enumerate(self.AllSers):
            if serie.SerItem != i:
                print("Warning: Hubo cambio de index (CYRm)")
                serie.SerItem = i
                for image in self.AllSers[i].AllImag:
                    image.SerItem = i

    ###############
    # 08-Geometry proyection of ref_ser2 in ref_ser1
    ###############

    def CY_serGeo_proj(self, ref_ser1, ref_ser2, new_seri):

        new_serie = self.CY_new_serie(ref_ser1, ref_ser1, new_seri, 5) # New black serie
        # Normal vector and transform matrices of ax-gre
        vec_norm_r10, d10_value = self.AllSers[ref_ser2].AllImag[0].CI_trans_base()
        vec_norm_r11, d11_value = self.AllSers[ref_ser2].AllImag[-1].CI_trans_base()
        print("planes:", vec_norm_r10, d10_value, vec_norm_r11, d11_value)                
        plane_equ=[]
        cross_pro=[]
        d_val = []
        for i in self.AllSers[ref_ser1].AllImag:
            vec_aux0 = []; vec_aux1 = []; vec_aux2 = []
            vec_aux0, vec_aux1 = i.CI_trans_base()
            plane_equ.append(vec_aux0)
            d_val.append(vec_aux1)
            print("crossA:", vec_aux0, vec_norm_r10)
            vec_aux3a = np.cross(vec_aux0, vec_norm_r10)
            vec_aux3b = np.cross(vec_aux0, vec_norm_r11)
            print("crossB:", vec_aux3a, vec_aux3b)
            #cross_pro.append(vec_aux2)
        print("plane full:", plane_equ)
        #vec_mm_r10 = [np.dot(self.AllSers[ref_ser2].AllImag[0].trns_MatOr,i) for i in p]
        ##ii_values = [np.dot(mti,j) for j in j_values]
        #j_values_without_last_element = [np.delete(j,-1) for j in j_values]
        #k_values = [np.dot(j,nro) for j in j_values_without_last_element]



        #Funcn_Proce.FP_serGeo_proj(self.AllSers[ref_ser1].AllImag[5],self.AllSers[ref_ser2].AllImag[11])
    '''
    ###############
    # Analiza y crea series de PC
    ###############
    
    def CYSrAnPCs(self):
        print("Buscando imágenes PC...")

        for i in range(len(self.AllSers)):
            #Identifica las series
            if self.AllSers[i].S11MRCo>109 and self.AllSers[i].S11MRCo<115:
                #Magit: 110, PhMag: 111, PhVrl: 112, PhVap: 113, PhVfh: 114
                var_aux0 = []
                #Busca si corresponde a alguna componente específica
                for j in range(len(self.AllSers[i].AllImag)):
                    var_aux0.append(self.AllSers[i].AllImag[j].D11MRCo)
                var_aux1 = Counter(var_aux0).keys()
                #
                for j in var_aux1:
                    if j>self.AllSers[i].S11MRCo:
                        self.AllSers[i].S11MRCo = j
                        self.AllSers[i].CSRCopCon(66)
    '''