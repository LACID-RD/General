import pydicom
import tkinter as tk
from tkinter import filedialog
import numpy as np
from collections import Counter
import gdcm
import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
from Class_Image import CImage
from Class_Proc import PProc

##########################################################################################
##########################################################################################
############################# CLASE CStudy ###############################################
##########################################################################################
##########################################################################################
'''
Clase asociada a todo lo que se hace a un BLOQUE de imágenes 
'''
class CStudy():
    Dcm_imagen=[]; Dcm_todo=[]; Geometry=[]; bvalues=[]
    Dcm_PWI=[]; Dcm_imaPWI=[]; dicOrdImg={}
  

    ########################################
    ########################################
    # Define variables de la clase
    ########################################
    ########################################

    def __init__(self,path_full): #pat_name=None,type=0,time=0,slice=0,img=None,te=0,tr=0,
        self.pathfull=path_full
        self.namf="map_f"; self.namDAs="map_D-Ast"
        self.namADC="map_ADC"; self.namS0="map_S0"
        self.pathDWI=0; self.pathPWI=0
        self.clases=[]

    ########################################
    ########################################
    # Busca imágenes y filtra las DCM
    ########################################
    ########################################

    def load_img(self,geom):  #Si PathPat es cero abre cuadro de dialogo, si no busca PathPat
        if self.pathfull==0:
            #Abre cuadro de diálogo y pregunta path del folder
            cuadro=tk.Tk(); cuadro.withdraw()
            pathDWI=filedialog.askdirectory(title="DICOM Images")
            StringVacio=""                  #Warning si no se abre algún folder
            if pathDWI is StringVacio:
                print("Error: No seleccionó directorio."); sys.exit(0)
        else:
            CStudy.Geometry.append(-2)      #G[0], totalslices
            CStudy.Geometry.append(geom[0]) #G[1], Xmin
            CStudy.Geometry.append(geom[1]) #G[2], Ymin
            CStudy.Geometry.append(geom[2]) #G[3], Xmax
            CStudy.Geometry.append(geom[3]) #G[4], Ymax
            self.pathDWI=self.pathfull+"/DWI"
            self.pathPWI=self.pathfull+"/PWI"            


    ########################################
    ########################################
    # Guarda/organiza features DWI images
    ########################################
    ########################################

    def Sec_read(self,Imag1,sec):
        cont0=0
        self.clases.clear()
        
        if sec==1: pathRead=self.pathDWI
        elif sec==2: pathRead=self.pathPWI
        for root,dirs,files in os.walk(pathRead):
            for i in files:
                if i.endswith(".dcm"):
                    PathAux=os.path.join(root,i)                   #Lee path de cada imagen
                    Imag1.DescomDicom(PathAux)
                    dcm=pydicom.dcmread(PathAux) 
                    if sec==1: CStudy.Dcm_todo.append(dcm)         #Lista con todas los datos del DICOM                 
                    elif sec==2: CStudy.Dcm_PWI.append(dcm)
                    Data_img=np.copy(dcm.pixel_array)
                    if sec==1: CStudy.Dcm_imagen.append(Data_img)  #Lista con todas las imágenes,numpy
                    elif sec==2: CStudy.Dcm_imaPWI.append(Data_img)
                    infoimag=Imag1.Reader(dcm)                     #Lista uni-imagen con informacion DICOM
                    self.clases=Imag1.sort_out(infoimag,cont0,sec) #Colecciones DWI
                    cont0+=1
        CStudy.Geometry[0]=self.clases[3]                          #G[0], totalslices
        return Imag1
                    

    ########################################
    ########################################
    # Organiza y analiza imágenes de DWI
    ########################################
    ########################################

    def DWI_org(self):
        Dcm_imgpos=self.clases[0]
        repetition=self.clases[1]
        repetitionsl=self.clases[2]
#       referencia=clases[5]
        bValues0=repetition.keys()
        CStudy.bvalues=list(bValues0)
        CStudy.Geometry.append(len(CStudy.bvalues))                       #G[5], bnumber
    
        ########### Se crea y llena diccionario
        obj2={}                                      
        for k in range(CStudy.Geometry[0]):
            obj2['Slice'+str(k)]=[]
        cont0=0
        for i in range(len(Dcm_imgpos)):
            vaux0=Dcm_imgpos[i]; vaux0=str(vaux0)
            t=[]
            for g in range(len(repetitionsl)):
                vaux1=list(repetitionsl.keys())[g]
                vaux1=str(vaux1)
                if vaux0==vaux1:
                    t=obj2["Slice"+str(g)]
                    t.append(cont0)
            cont0+=1

        ########### Reordenamiento
        for k in range(CStudy.Geometry[0]):
            CStudy.dicOrdImg['Slice'+str(k)]=[]
        for l in obj2.keys():
            laux0=obj2.get(str(l))
            vaux0=len(laux0); laux1=[0]*vaux0
            for d in range(CStudy.Geometry[5]):
                Img2=CImage()
                laux2=[]
                laux2=Img2.Reader(CStudy.Dcm_todo[laux0[d]])
                cont0=0
                for i in range(CStudy.Geometry[5]):
                    laux3=Img2.Reader(CStudy.Dcm_todo[laux0[i]])
                    if laux3[6]<laux2[6]:
                        cont0+=1
                laux1[cont0]=laux0[d]
            CStudy.dicOrdImg[str(l)].append(laux1)
        
        ########### Se calcula el size de la matriz original (DWI)
        img_shape0=[]; img_shape0=CStudy.Dcm_imagen[0]
        img_shape=img_shape0.shape
        CStudy.bvalues.sort()
        CStudy.Geometry.append(img_shape[0])       ## G[6] ImgShapeX
        CStudy.Geometry.append(img_shape[1])       ## G[7] ImgShapeY
        CStudy.Geometry.append(-5)                 ## G[8] Numero de slice sistema VMPacs
        CStudy.Geometry.append(-7)                 ## G[9] Numero de slice coordenada python
        
        '''       
        ## Seleccion de corte para el ROI
        g=0
        for g in range(CStudy.Geometry[0]):
            print('Slice',g)
            plt.imshow(CStudy.Dcm_imagen[g], cmap = plt.cm.bone)
            plt.show()
            g=g+1
        INCorte=input('Pick a slice to perform the ROI from images above (B0 DWI)')
        for d in range(CStudy.Geometry[5]):
            vaux0=int(list(CStudy.dicOrdImg['Slice'+str(INCorte)][0])[d])
            BOutaux=CStudy.Dcm_todo[vaux0][0x0043,0x1039]
            BOut=BOutaux.value
            BOut1=str(BOut)
            BOut2=list(BOut1)
            if int(BOut2[2])==0:
                B0Ref=vaux0
                x1=0
            else:
                x1=int(BOut2[11])+10*int(BOut2[10])+100*int(BOut2[9])+1000*int(BOut2[8])

        final_image=[]
        for d in range(CStudy.Geometry[5]):
            vaux0=int(list(CStudy.dicOrdImg['Slice'+str(INCorte)][0])[d])
        # print('Imagen de B:',CStudy.bvalues[d])   
            Final_ROI=CStudy.Dcm_imagen[vaux0]
        # print(d)
            final_image.append(Final_ROI)
    # a=general_ROI
    # a=list(a)
        img_shapefinal=Final_ROI.shape
        img_shapefinal=list(img_shapefinal)
        print("Tamaño del ROI:",img_shapefinal[0],img_shapefinal[1])
    #Paso de la lista al diccionario otra vez para poder ajustar
    #Diccionario para analisis multislice,ahora para un unico corte
        obj3={}
        for k in range(CStudy.Geometry[0]):
            obj3[k]=[]
        cont0=0
        cont1=0
        for e in range(len(final_image)):
            vaux0=obj3[cont1]
            vaux0.append(e)
            cont0+=1
            if cont0==CStudy.Geometry[5]:
                cont0=0
                cont1+=1
        
        '''
        return 0

    ########################################
    ########################################
    # Posición del slice de DWI
    ########################################
    ########################################

    def DWI_sliPo(self,selSlice):
        #G[8] Numero de slice, sistema de referencia VMPacs
        #Espacio guardado en la función dwi_org
        CStudy.Geometry[8]=selSlice

        #Se analiza el orden de los slices. Se incrementan en
        #sentido FH (caudal-craneal), EN SENTIDO INVERSO AL VMPACS
        zImgPos=[]
        for k in range(CStudy.Geometry[0]):
            vAux0=int(CStudy.dicOrdImg['Slice'+str(k)][0][0])
            vAux1=CStudy.Dcm_todo[vAux0]
            vAux2=vAux1[0x0020,0x0032].value
            vAux3=vAux2[2]
            print("vaux3:",vAux3)
            zImgPos.append(vAux3)
        zImgPos1=np.array(zImgPos)
        zImgPos.sort()
        print('Poscion en Z',zImgPos)
        vAux4=int(CStudy.Geometry[0]-CStudy.Geometry[8])       #Cambio de sistema de ref, del VMPacs a python
        zSliPos=zImgPos[vAux4]
        for k in range(CStudy.Geometry[0]):
            if zImgPos1[k]==zImgPos[vAux4]:
                CStudy.Geometry[9]=k                           #G[9] Numero de slice coordenada python
        print('CStudy.Geometry[8]: selSlice',CStudy.Geometry[8])
        print('CStudy.Geometry[9]: coorPyth',CStudy.Geometry[9])
        return zSliPos


    ########################################
    ########################################
    # Administra y solicita ajustes, crea mapas
    ########################################
    ########################################

    def fit_mngnt(self,PathFull,Imag1):

        ########### Ajusta y genera mapas
        #No olvidar q G[5] es bnumber
        Adj1=PProc(CStudy.Geometry,CStudy.bvalues,CStudy.dicOrdImg,CStudy.Dcm_imagen)
        matriz2=Adj1.model_adc()
        matrices=Adj1.model_ivim()

        ########### Borra imagenes existentes de IVIM
        pathImage=self.pathfull+"/IVIM"
        Imgfile=pathImage+"/"+self.namf+".dcm"
        if os.path.isfile(Imgfile): os.remove(Imgfile)
        Imgfile=pathImage+"/"+self.namDAs+".dcm"
        if os.path.isfile(Imgfile): os.remove(Imgfile)
        Imgfile=pathImage+"/"+self.namADC+".dcm"
        if os.path.isfile(Imgfile): os.remove(Imgfile)
        Imgfile=pathImage+"/"+self.namS0+".dcm"
        if os.path.isfile(Imgfile): os.remove(Imgfile)

        ########### Exporta a DICOM       
        vAux1=int(CStudy.dicOrdImg['Slice'+str(CStudy.Geometry[9])][0][0]) #Se busca coordenada de referencia     
        path_full=PathFull+"/IVIM"
        Imag1.addDCM(CStudy.Dcm_todo[vAux1],path_full,self.namf,CStudy.Geometry,matrices[0])
        Imag1.addDCM(CStudy.Dcm_todo[vAux1],path_full,self.namDAs,CStudy.Geometry,matrices[1])
        Imag1.addDCM(CStudy.Dcm_todo[vAux1],path_full,self.namADC,CStudy.Geometry,matriz2)
        Imag1.addDCM(CStudy.Dcm_todo[vAux1],path_full,self.namS0,CStudy.Geometry,matrices[2])
        
        vAux2=CStudy.Dcm_todo[vAux1]
        print("Imageposition:",vAux2[0x0020,0x0032].value)     #QA
        return Imag1

    ########################################
    ########################################
    # Organiza y analiza imágenes de PWI
    ########################################
    ########################################

    def PWI_org(self,zSliPos):
        obj2={}
        '''
        Dcm_imgpos=
        repetition=self.clases[1]
        repetitionsl=self.clases[2]
        totalslices=self.clases[3]
        '''
        ########### Se crea y llena diccionario                                  
        for k in range(self.clases[3]):
            obj2['Slice'+str(k)]=[]
        cont0=0
        for i in range(len(self.clases[0])):
            vaux0=self.clases[0][i];vaux0=str(vaux0);t=[]
            for g in range(len(self.clases[2])):
                vaux1=list(self.clases[2].keys())[g]
                vaux1=str(vaux1)
                if vaux0==vaux1:
                    t=obj2["Slice"+str(g)]
                    t.append(cont0)
            cont0+=1

        ########### Se busca valor más cercano
        minval=99999; h=-2
        print("Obj2:",obj2)
        for k in range(self.clases[3]):
            vAux0=int(obj2['Slice'+str(k)][0])
            vAux1=CStudy.Dcm_PWI[vAux0]
            vAux2=vAux1[0x0020,0x0032].value
            vAux3=vAux2[2]
            diff=abs(vAux3-zSliPos)
            if diff<minval:
                print("vaux3:",vAux3)
                print("diff:",diff)
                minval=diff
                h=k
                print("h:",h)

        
        vAux0=int(obj2['Slice'+str(h)][0])
        vAux1=CStudy.Dcm_imaPWI[vAux0]
        #print("vAux1",vAux1)
        plt.imshow(vAux1,cmap=plt.cm.bone)
        plt.title('Pefu')
        plt.show()