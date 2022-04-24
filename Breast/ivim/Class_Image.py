#from gdcm.gdcmswig import Object
import pydicom
import tkinter as tk
from tkinter import filedialog
import numpy as np
import collections 
import gdcm
import sys
import pandas as pd
import matplotlib.pyplot as plt
import time
import random

##########################################################################################
##########################################################################################
############################# CLASE CImage ###############################################
##########################################################################################
##########################################################################################
'''
 Clase asociada a todo lo que se hace a UNA imagen 
'''

class CImage():

    imgDWI=[]

    ########################################
    ########################################
    # Define variables de la clase
    ########################################
    ########################################

    def __init__(self): #pat_name=None,type=0,time=0,slice=0,img=None,te=0,tr=0,
        self.Dcm_imgpos=[]
        self.Dcm_auxV=[]
        # self.time = time
        

    ########################################
    ########################################
    # Descomprime y reescribe imágenes
    ########################################
    ########################################

    def DescomDicom(self,PathAux):
        reader=gdcm.ImageReader()
        #reader.SetFileName(self.path_name)
        reader.SetFileName(PathAux)
        if not reader.Read():        
            print("Error: No se leen correctamente las imágenes.")
            sys.exit(0)
        change = gdcm.ImageChangeTransferSyntax()
        change.SetTransferSyntax(gdcm.TransferSyntax(gdcm.TransferSyntax.ImplicitVRLittleEndian))
        change.SetInput( reader.GetImage() )
        if not change.Change():
            print("Error: No se descomprime correctamente las imágenes.")
            sys.exit(0)
        writer = gdcm.ImageWriter()
        writer.SetFileName(PathAux)
        writer.SetFile(reader.GetFile())
        writer.SetImage(change.GetOutput())
        if not writer.Write():
            print("Error: No se escriben correctamente las imágenes.")
            sys.exit(0)


    ########################################
    ########################################
    # Lee/guarda variables DICOM
    ########################################
    ########################################

    def Reader(self,fimg):
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
        try:
            ffReDC.append(fimg[0x0018,0x9087].value) #6:b-value (CASO PARTICULAR PORQUE NO ESTA SIEMPRE)
        except:
            ffReDC.append(0.0)
        ffReDC.append(fimg[0x020,0x011].value)      #7:series number, lo voy a tener que hacer por fuera
        ffReDC.append(fimg[0x0028,0x0010].value)   #8:Num de filas
        ffReDC.append(fimg[0x0028,0x0011].value)   # 9:Num de colum 
        ffReDC.append(fimg[0x0008,0x103e].value)  #10:Series description  
        listimtype=fimg[0x0008,0x0008].value
        imgtype = list(filter(lambda x: 'ADC' in x, listimtype))
        ffReDC.append(imgtype)                  #11:tipo de imagen 
        if "SIE" in ffReDC[1]:
            ffReDC.append(fimg[0x0020,0x0032].value)# 12:Slice
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
            if 3.0 == ffReDC[5]:
                out=fimg[0x0043,0x1039].value
                out1=str(out)
                out2=list(out1)
                if int(out2[2]) ==0:
                    x1=0
                    ffReDC.insert(6,x1)
                else:
                    x1=int(out2[11])+10*int(out2[10])+100*int(out2[9])+1000*int(out2[8])
                    ffReDC.insert(6,x1)
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
            corte=fimg[0x2001,0x100b].value
            ffReDC.append(corte)
        else:
            print("Error 5: Las imágenes no son de equipos Philips, ni GE, ni Siemens.")
            sys.exit(5)
        ffReDC.append(fimg[0x0020,0x0013].value) #14:orden
        return ffReDC


    ########################################
    ########################################
    # Clasifica/Ordena imagenes por secuencia
    ########################################
    ########################################

    def sort_out(self,ffinfoImg,ffcont,sec):
        r=[]; referencia=[]; imgperfu=[]; imgT1=[]
        imgADC=[]; imgT2AX=[]; imgT2COR=[]; imgT2SAG=[]

        ########### Se inicializa cuando hay una secuencia nueva
        if ffcont==0:
            r.clear();referencia.clear();imgperfu.clear()
            imgT1.clear();imgADC.clear();imgT2AX.clear()
            imgT2COR.clear();imgT2SAG.clear()
            self.Dcm_imgpos.clear();self.Dcm_auxV.clear()
        
        ########### Se llena vector r
        #Perfu
        if ffinfoImg[3]<3 and ffinfoImg[2]<5:
            imgperfu.append(ffcont);sec0=2
            ImgPos=ffinfoImg[12][2]; ImgPos=str(ImgPos)
            ImgMap=ffinfoImg[10]#[2]#;ImgMap=str(ImgMap)
            self.Dcm_auxV.append(ImgMap)
            self.Dcm_imgpos.append(ImgPos)          
            r.append(self.Dcm_imgpos)                        #r[0]
            repeticion=collections.Counter(self.Dcm_auxV)
            totalmaps=len(repeticion)
            repeticionsl=collections.Counter(self.Dcm_imgpos)
            totalslices=len(repeticionsl)
            r.append(repeticion);r.append(repeticionsl)      #r[1],r[2]
            r.append(totalslices);r.append(self.Dcm_auxV)    #r[3],r[4]
            r.append(referencia)                             #r[5]
        #wT1
        elif ffinfoImg[3]<20 and ffinfoImg[2]<600:
            imgT1.append(ffcont); r.append(imgT1); sec0=3
        else:
            #ADC
            if 'ADC' in str(ffinfoImg[11]):
                imgADC.append(ffcont); r.append(imgADC); sec0=4
            #DWI
            elif 'D'in str(ffinfoImg[10]) or 'V'in str(ffinfoImg[10]) or 'K'in str(ffinfoImg[10]):
                referencia.append(ffcont); sec0=1
                CImage.imgDWI.append(ffcont)
                ImgPos=ffinfoImg[12][2]
                ImgPos=str(ImgPos)
                self.Dcm_imgpos.append(ImgPos)
                r.append(self.Dcm_imgpos)                    #r[0]
                self.Dcm_auxV.append(ffinfoImg[6])
                repeticion=collections.Counter(self.Dcm_auxV)
                repeticionsl=collections.Counter(self.Dcm_imgpos)
                totalslices=len(repeticionsl)
                r.append(repeticion);r.append(repeticionsl)  #r[1],r[2]
                r.append(totalslices);r.append(self.Dcm_auxV)#r[3],r[4]
                r.append(referencia)                         #r[5]
            #T2Ax
            elif  'TRA' in str(ffinfoImg[12]) or 'AX' in str(ffinfoImg[12]):
                imgT2AX.append(ffcont); r.append(imgT2AX); sec0=5
            #T2Cor
            elif 'COR'in str(ffinfoImg[12]):
                imgT2COR.append(ffcont); r.append(imgT2COR); sec0=6
            #T2Sag
            elif 'SAG' in str(ffinfoImg[12]):
                imgT2SAG.append(ffcont); r.append(imgT2SAG); sec0=7
        if sec0!=sec:
            print("Error: Las imágenes no son de la secuencia.")
            sys.exit(0)
        return r


    ########################################
    ########################################
    # Ordena DICOM en lista
    ########################################
    ########################################

    def SortDicom(self):
        Dcm_list=[]
        Dcm_list.append(self.tr)
        Dcm_list.append(self.te)
        #Dcm_list.append(self.slice)
        return Dcm_list
    

    ########################################
    ########################################
    # Hereda features DICOM
    ########################################
    ########################################
    
    def addDCM(self,DCMorigen,PathFull,nameMap,geometry,mapa):

        arr=np.zeros((geometry[6],geometry[7]),dtype=np.int16)
        for i in range(geometry[6]):
            for j in range (geometry[7]):
                arr[i,j]=mapa[i,j]
        
        ds=DCMorigen
        plt.imshow(arr,cmap=plt.cm.bone)
        plt.show()
        
        modificationTime=time.strftime("%H%M%S")
        pathFinal=PathFull+"/"+nameMap+".dcm"#path completo con que se va a guardar cada imagen dicom final
        #np_frame1=listofmaps[k]
        #ds.Rows=geometry[6] #np_frame1.shape[0]
        #ds.Columns=geometry[7] #np_frame1.shape[1]
        ds[0x0020,0x0011].value=random.randint(200,500)
        ds.PhotometricInterpretation="MONOCHROME2"
        #ds.SamplesPerPixel=1
        #ds.BitsStored=16
        #ds.BitsAllocated=16
        #ds.HighBit=15
        #ds.PixelRepresentation=1
        #ds.PixelData=arrMapa.tobytes()
        ds.SeriesDescription=nameMap #'MAP'+str(k)
        ds.SeriesInstanceUID=pydicom.uid.generate_uid()
        ds[0x008,0x0031].value=modificationTime
        ds[0x008,0x0018].value=ds[0x008,0x0018].value+str(1)
        ds[0x008,0x0008].value='SECONDARY'
        ds.PixelData=arr.tobytes()
        ds.save_as(pathFinal)
        print("path final:",pathFinal)