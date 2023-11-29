#from ntpath import join
#from operator import ne
#import shelve
#import pydicom
#import tkinter as tk
#from tkinter import filedialog
#import numpy as np
#from collections import Counter
#import gdcm
#import os
#import pandas as pd
#import matplotlib.pyplot as plt
#from Class_Image import CImage
#from Class_Proc import PProc
#import math
#from scipy import ndimage,misc,signal
#from itertools import repeat
#from scipy.stats.stats import pearsonr
#import cv2
import sys

########## MR: 10
##### General
# 10ExFd: B0
# 10SqTp: Tipo de Secuencia
# 10AdTy: Acquisition type
##### Contrast: 11
# 11TsTr: TR
# 11TsTe: TE
# 11TsTi: TI
# 11FlAn: Flip Angle
# 11MRCo: Contraste
##### Design: 12
# 12ETLg: Echo Train Length
# 12PhCd: Codificacion de fase
# 12AcPl: Acquisition plane (Ax:0, Sag:1, Cor:2)
# 12TrTm: Trigger Time
##### DWI: 15
# 15bVal: DWI b-value

###################
# DCM general RM 05-30
###################

def CDMGenMRI(self):

    ########## Campo externo
    try: self.D10ExFd = self.DcmImag[0x0018,0x0087].value
    except: self.D10ExFd = -4
    ########## Tipo de Sec
    try: self.D10SqTp = self.DcmImag[0x0018,0x0020].value
    except: self.D10SqTp = -4
    ########## Acquisition type
    try: self.D10AdTy = self.DcmImag[0x0018,0x0023].value
    except: self.D10AdTy = -4
    ########################################### TR
    try: self.D11TsTr=self.DcmImag[0x0018,0x0080].value
    except: print("Error: No se puede determinar Tr de las imagenes."); sys.exit(0)
    ########################################### TE
    try:self.D11TsTe=self.DcmImag[0x0018,0x0081].value
    except: print("Error: No se puede determinar Te de las imagenes."); sys.exit(0)
    ########################################### TI
    try: self.D11TsTi=self.DcmImag[0x0018,0x0082].value
    except: self.D11TsTi=-4
    ########################################### Flip angle
    try: self.D11FlAn=self.DcmImag[0x0018,0x1314].value
    except: self.D11FlAn=-4
    ########################################### Echo Train Lenghth
    try: self.D12ETLg=self.DcmImag[0x0018,0x0091].value
    except: self.D12ETLg=-4
    ########################################### Codi. de fase
    try: self.D12PhCd=self.DcmImag[0x0018,0x1312].value
    except: self.D12PhCd=-4
    ########################################### Acquisition Plane
    try:
        varAux1=self.DcmImag[0x2001,0x100b].value
        if 'sag' in str(varAux1) or 'Sag' in str(varAux1) or 'SAG' in str(varAux1): self.D12AcPl=1
        elif 'cor' in str(varAux1) or 'Cor' in str(varAux1) or 'COR' in str(varAux1): self.D12AcPl=2
        else: self.D12AcPl=0
    except:
        try:
            varAux1=self.DcmImag[0x0008,0x103e].value
            if 'sag' in str(varAux1) or 'Sag' in str(varAux1) or 'SAG' in str(varAux1): self.D12AcPl=1
            elif 'cor' in str(varAux1) or 'Cor' in str(varAux1) or 'COR' in str(varAux1): self.D12AcPl=2
            else: self.D12AcPl=0
        except: self.D12AcPl=-4

    #No llenar si es segunda captura dcm
    if self.D11MRCo != -4:
        self.CDMContMR()
        #Phase Contrast
        varAux1=[]
        if self.D11MRCo == 10:
            if "Phil" in self.D01Mnfr:
                try: varAux0=str(self.DcmImag[0x2005,0x116e].value)
                except: varAux0=-4
                try:
                    varAux1.append(self.DcmImag[0x2001,0x101a].value[0])
                    varAux1.append(self.DcmImag[0x2001,0x101a].value[1])
                    varAux1.append(self.DcmImag[0x2001,0x101a].value[2])
                except: varAux1.append(0)
                varAux2=varAux1[0]+varAux1[1]+varAux1[2]
                #print(varAux0,len(varAux1),varAux2)
                if ("PCA" in varAux0 or "FFE" in varAux0) and len(varAux1)>2 and varAux2>1:
                    self.CDMMRPhCo(varAux0)
        #DWI
        elif self.D11MRCo == 20: self.CDMMRwDWI()

########################################
########################################
# RM: Analiza y define contraste
########################################
########################################
# 50MRCo - Contraste de la imagen
#-4: Segunda captura
#10: GRE-T1
#11: PC: 110 FFE, 111 PCA-Mg, 112 PCA-x, 113 PCA-y, 114 PCA-z - CDMMRGRT1()
#15: wT1
#20: wT2
#21: DWI - CDMMRwDWI()
#25: GRE-T2
#26: fMRI
#30: IR-STIR
#31: T2-FLAIR
#32: T1-FLAIR
#66: Not found
#67: Postprocessing

def CDMContMR(self):

    if self.D11MRCo != 0:
        if   self.D11TsTi>100  and self.D11TsTi<200:  self.D11MRCo=30
        elif self.D11TsTi>1500 and self.D11TsTi<3200: self.D11MRCo=31
        elif self.D11TsTi>700  and self.D11TsTi<1100: self.D11MRCo=32
        elif self.D11TsTr<50   and self.D11TsTe<20 and self.D11FlAn<45:  self.D11MRCo=10
        elif self.D11TsTr<750  and self.D11TsTe<30 and self.D11FlAn>55:  self.D11MRCo=15
        elif self.D11TsTr>250  and self.D11TsTe<45 and self.D11FlAn<45:  self.D11MRCo=25
        elif self.D11TsTr>2000 and self.D11TsTe<70 and self.D11FlAn==90: self.D11MRCo=26
        elif self.D11TsTr>600  and self.D11TsTe>50 and self.D11FlAn>80:  self.D11MRCo=20
        else: self.D11MRCo=66
        #else: print("Error: No se determino contraste de imagen."); sys.exit(0)


########################################
########################################
# RM: Phase contrast
########################################
########################################
#Magit: 110
#PhMag: 111
#PhVrl: 112
#PhVap: 113
#PhVfh: 114

def CDMMRPhCo(self,varAux0):

    if "PCA" in str(varAux0):
        #print(self.DcmImag[0x2001,0x101a].value[0],self.DcmImag[0x2001,0x101a].value[1],self.DcmImag[0x2001,0x101a].value[2])
        if self.DcmImag[0x2001,0x101a].value[0]>50 and self.DcmImag[0x2001,0x101a].value[1]>50 and self.DcmImag[0x2001,0x101a].value[2]>50:
            self.D11MRCo=111 #Magnitud de la velocidad
        elif self.DcmImag[0x2001,0x101a].value[0]>50 and self.DcmImag[0x2001,0x101a].value[1]==0 and self.DcmImag[0x2001,0x101a].value[2]==0:
            self.D11MRCo=112 #RL (X)
        elif self.DcmImag[0x2001,0x101a].value[0]==0 and self.DcmImag[0x2001,0x101a].value[1]>50 and self.DcmImag[0x2001,0x101a].value[2]==0:
            self.D11MRCo=113 #AP (Y)
        elif self.DcmImag[0x2001,0x101a].value[0]==0 and self.DcmImag[0x2001,0x101a].value[1]==0 and self.DcmImag[0x2001,0x101a].value[2]>50:
            self.D11MRCo=114 #FH (Z)
        else: print("Error: No se lee correctamente las imágenes PCA (PC)."); sys.exit(0)
    elif "FFE" in str(varAux0): self.D11MRCo=110 #Magnitud
    else: self.D11MRCo=self.D11MRCo
    if self.D11MRCo>109 and self.D11MRCo<115: self.D12TrTm=self.DcmImag[0x0018,0x1060].value
    print("TrTm:",self.D12TrTm)
    #print(self.D11MRCo)


########################################
########################################
# RM: DWI
########################################
########################################

def CDMMRwDWI(self):
    
    ########################################### DWI b-value
    try: self.D15bVal=self.DcmImag[0x0018,0x9087].value
    except:
        try: self.D15bVal=self.DcmImag[0x0019,0x100c].value
        except:
            try:
                out=self.DcmImag[0x0043,0x1039].value
                out1=str(out)
                out2=list(out1)
                if int(out2[2])==0:
                    x1=0; self.D15bVal=x1
                else:
                    x1=int(out2[11])+10*int(out2[10])+100*int(out2[9])+1000*int(out2[8])
                    self.D15bVal=x1
            except: self.D15bVal=-4
    ########################################### Contraste
    if self.D15bVal>0: self.D11MRCo=21
