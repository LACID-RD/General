#from gdcm.gdcmswig import Object
#import pydicom
#import numpy as np
#import collections 
#import pandas as pd
#import matplotlib.pyplot as plt
#import time
#import random
import csv
import gdcm
import numpy as np
from numpy.linalg import inv
import sys
### Local libraries
from Class_DcmRd import CDcmRd

#############################
#############################
# CLASS CImage 04-
#############################
#############################

class CImage(CDcmRd):#Hereda de clase DcmRd
    """Class that nnn"""
    Instanc=[]

    ###############
    # Define variables de la clase
    ###############

    def __init__(self,PathImg):

        #pat_name=None,type=0,time=0,slice=0,img=None,te=0,tr=0,
        CImage.Instanc.append(self)
        self.StuItem = -4 # Estudio a la q pertenece
        self.SerItem = -4 # Serie a la que pertenece
        self.ImgItem = 4  # Indexado de la imagen
        self.ImgData = [] # Matriz de datos de la imagen
        #self.Dcm_imgpos = []
        self.trns_MatOr = [] # Matriz de transformacion espacial pixel-mm
        self.trns_MatZc = [] # Inv de la matriz de transformacion espacial con Z
        self.PathImg = PathImg
        # self.time = time
        CDcmRd.__init__(self,PathImg)

    ###############
    # Descomprime y reescribe imágenes
    ###############

    def CIDescDCM(self, PathAux):

        reader = gdcm.ImageReader()
        #reader.SetFileName(self.path_name)
        reader.SetFileName(PathAux)
        if not reader.Read():        
            print("Error: No se leen las imágenes (CIDes)."); sys.exit(0)
        change = gdcm.ImageChangeTransferSyntax()
        change.SetTransferSyntax(gdcm.TransferSyntax(gdcm.TransferSyntax.ImplicitVRLittleEndian))
        change.SetInput( reader.GetImage() )
        if not change.Change():
            print("Error: No se descomprime las imágenes (CIDes)."); sys.exit(0)
        writer = gdcm.ImageWriter(); writer.SetFileName(PathAux)
        writer.SetFile(reader.GetFile()); writer.SetImage(change.GetOutput())
        if not writer.Write():
            print("Error: No se escriben las imágenes (CIDes)."); sys.exit(0)

    ###############
    # Copia características desde otra imagen
    ###############
    #RefImag: Imagen de referencia para definir caracteristicas de la imagen
    #ImgMatx: Matriz de datos de la imagen

    def CIRCopFea(self, RefImag, ImgMatx, SerNumb, StuItem, SerItem):

        self.ImgData=ImgMatx
        self.StuItem=StuItem
        self.SerItem=SerItem
        self.D00CpTp=0; self.D01Name=RefImag.D01Name; self.D01StDc=RefImag.D01StDc
        #self.D00TfSy=-2; self.D00Sour=-2
        #self.D01StTm=-2; self.D01Mnfr=-2
        #self.D01MnMd=-2
        self.D01Mdly=RefImag.D01Mdly; self.D04SlTk=RefImag.D04SlTk; self.D04RwNb=RefImag.D04RwNb
        self.D04ClNb=RefImag.D04ClNb; self.D04PiSp=RefImag.D04PiSp; self.D04DiCo=RefImag.D04DiCo
        self.D04Slic=RefImag.D04Slic; self.D04ImPo=RefImag.D04ImPo; self.D10ExFd=RefImag.D10ExFd
        self.D12AcPl=RefImag.D12AcPl; self.D02SeNu=SerNumb
        #self.D03AcNb=-2
        #self.CIBaseTrf()                                #Matriz de transformacion 


    ###############
    # Matriz de transformacion pixel a mm
    ###############
    #https://dicom.innolitics.com/ciods/rt-dose/image-plane/00200037

    def CI_trans_base(self):
        # Auxiliar variables
        vec_rwo = np.array(self.D04DiCo[0:3]) # X
        vec_clo = np.array(self.D04DiCo[3:6]) # Y
        vec_nor = np.cross(vec_rwo,vec_clo)
        print("CITR", vec_rwo, vec_clo, vec_nor)
        var_qa = np.sum(np.square(vec_rwo)) * np.sum(np.square(vec_clo)) * np.sum(np.square(vec_nor))
        if not 0.999 < var_qa < 1.001:
            raise ValueError("Error: Problemas con los cosenos directores (CItrans).")
        
        # Transformation matrix
        self.trns_MatOr = np.array([[vec_rwo[i]*self.D04PiSp[0], vec_clo[i]*self.D04PiSp[1], vec_nor[i]*self.D04SlTk, self.D04ImPo[i]] for i in range(3)] + [[0, 0, 0, 1]])
        self.trns_MatZc = np.linalg.inv(self.trns_MatOr)
        '''
        img_point = [[0, 0, 0, 1], [self.D04RwNb - 1, self.D04ClNb - 1, 0, 1]]
        vec_mm = []
        for i in img_point:
            vec_mm.append(np.dot(self.trns_MatOr, i))
        vec_mm = [lst[:-1] for lst in vec_mm]
        vec_d=[]
        for i in vec_mm:
            vec_d.append(np.dot(i,vec_nor))
        if (vec_d[0]/vec_d[1]) < 0.999 or (vec_d[0]/vec_d[1]) > 1.0001:
            raise ValueError("Error: Problemas con D del plano (CItrans).")
        '''
        img_point = [[0, 0, 0, 1], [self.D04RwNb - 1, self.D04ClNb - 1, 0, 1]]
        vec_mm = [np.dot(self.trns_MatOr, i)[:-1] for i in img_point]
        vec_d = [np.dot(i, vec_nor) for i in vec_mm]
        if (vec_d[0]/vec_d[1]) < 0.999 or (vec_d[0]/vec_d[1]) > 1.0001:
            raise ValueError("Error: Problemas con D del plano (CItrans).")
        return vec_nor, vec_d[0]
        
    ###############
    # Genera un string de titulo
    ###############
    #PrtType: 0 para titulos de graficas, 1: nombre de archivos exportados

    def CIFTitles(self, PrtType):

        TitleSt=""
        if PrtType==0:
            TitleSt+="Stu:"+str(self.StuItem)+" Ser:"+str(self.SerItem)+" Img:"+str(self.ImgItem)
        elif PrtType==1:
            TitleSt+="Img_"; varAux0=str(self.D01Name)
            TitleSt+=varAux0[:4]+"_S"+str(self.StuItem)+"_R"+str(self.SerItem)+"_I"
            print("Name:",TitleSt,self.ImgItem)
        return TitleSt

    ########################################
    ########################################
    # Exporta a formato CSV
    ########################################
    ########################################

    def CICSVExpo(self):
        
        FleName=self.CIFTitles(1); FleName+=".csv"
        print("ImaName:",FleName)
        with open(FleName,'w',newline='') as varFile:
            vWriter=csv.writer(varFile)
            vWriter.writerows(self.ImgData)
    #Fiji: Import -> Text image

    