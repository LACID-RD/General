'''
    Prostate-MRI Image Preprocessing 
    Authors: Trinidad González Padin

    Daniel Fino
    Joaquín Capó
    Nicolás Moyano Brandi
    Federico González
'''

from operator import contains
import cmath
import matplotlib.pyplot as plt
from numpy.lib.npyio import save
from skimage.io import imread, imsave
import pydicom
import tkinter as tk
from tkinter import filedialog
import numpy as np
from pydicom.uid import generate_uid
import collections
from scipy.optimize import least_squares, minpack2
import gdcm
import sys
import time
import cv2 as cv
import random
from PIL import Image
from skimage.color import gray2rgb
from skimage import color
from skimage.util import img_as_ubyte,img_as_float
import tempfile
import pandas as pd
import math
import SimpleITK as sitk
from scipy import ndimage, misc
from lmfit import Model
from FFDICOM import decompress,Reader,position_ROI,img_ROI,bvalue
#from FFprostata import sort_out

Dcm_imagen=[]
imgT1=[]
Dcm_b_value=[]
Dcm_imagen=[]
Dcm_imgposition=[]
dcmDWI=[]
imgT1=[]
imgperfu=[]
imgT2AX=[]
imgT2SAG=[]
imgADC=[]
imgDWI=[]
info_SeriesNumber=[]
referencia=[]
corrK=6.4
corrncf=0.0
corrMag=500
corrA=3.25
corrA2=1.0       ##### CorrA2: para el segundo ajuste
c11=1.0
c21=1.0
c31=1.0
corrD=1.0
corrd=1.0


def fun10(x,A,B,d,D):
    return A*np.exp(-x*d)+B*np.exp(-x*D)


def kurtosis(x,D,K):
    # print('CorrK1',corrK1)
    return (c21*np.exp(-x*c31)+((1-c21)*np.exp(-x*D+(x*x*D*D*K/corrK)+corrncf)))

def sort_out(ffinfoimagenes,ffcont):
    '''
    Sorts out different  MRI sequences
    '''
    r=[]
    if ffinfoimagenes[3]<3 and ffinfoimagenes[2]<5:
            imgperfu.append(ffcont) 
            print('es perfu')
            r.append(imgperfu)
    elif ffinfoimagenes[3]<20 and ffinfoimagenes[2]<600:
            print('es t1')
            imgT1.append(ffcont) 
            r.append(imgT1)
    else:
        if 'ADC' in str(ffinfoimagenes[11]):
            print('es adc')
            imgADC.append(ffcont)
            r.append(imgADC)
        elif 'D'in str(ffinfoimagenes[10]) or 'V'in str(ffinfoimagenes[10]) or 'K'in str(ffinfoimagenes[10]):
                #print('es dwi')
                referencia.append(ffcont)
                imgDWI.append(ffcont)
                ImgPos=ffinfoimagenes[12][2]
                ImgPos=str(ImgPos)
                Dcm_imgposition.append(ImgPos)
                    # componentez.append(ffinfoimagenes[12][2])
                    # componentez.sort()

                r.append(Dcm_imgposition)#0 del r
                Dcm_b_value.append(ffinfoimagenes[6])
                repeticion=collections.Counter(Dcm_b_value)
                repeticionsl=collections.Counter(Dcm_imgposition)
                #nuevacoleccion=collections.Counter(componentez)
                totalslices=len(repeticionsl)
                #totalslices=len(nuevacoleccion)
                r.append(repeticion)# 1 de r
                r.append(repeticionsl)#2 de r
                    #r.append(nuevacoleccion)
                r.append(totalslices)#3 de r
                r.append(Dcm_b_value)#4 de r 
                r.append(referencia)#5  
                # dcmDWI.append(dcm)
                # Dcm_imDWI = np.copy(dcm.pixel_array)
                #imgDWI.append(Dcm_imDWI)
        elif  'TRA' in str(ffinfoimagenes[12]) or 'AX' in str(ffinfoimagenes[12]):
                imgT2AX.append(ffcont) 
                print('es t2 ax')
                r.append(imgT2AX)
        elif 'COR'in str(ffinfoimagenes[12]):
                imgperfu.append(ffcont)
                print('es coronalt2 ')
                r.append(imgperfu)
        elif 'SAG' in str(ffinfoimagenes[12]):
                imgT2SAG.append(ffcont)
                print('es t2 sag')
                r.append(imgT2SAG)
    return r



def calculoerror(resultparams):
    lista2=[]
    for l in resultparams:
        try:
            r=resultparams[l].stderr/resultparams[l].value
            r=r*100
            r=int(r)
            if r>10000:
                r=10000
            lista2.append(r)
        except:
            lista2=[10000 for i in range(6)]
    return(lista2)

def ajuste1(x0,y0):
    output=[]
    minf=0.01*corrA             #%
    maxf=0.8*corrA                #%
    mind=0.001*corrMag      #mm2/s
    maxd=0.04*corrMag       #mm2/s  
    minD=0.0001*corrMag     #mm2/s
    maxD=0.0018*corrMag     #mm2/s
    minA=y0[0]*minf*corrA
    maxA=y0[0]*maxf*corrA
    minB=y0[0]*(1-maxf)*corrA
    maxB=y0[0]*(1-minf)*corrA
    promd=(maxd-mind)/2
    promD=(maxD-minD)/2
    promA=(maxA-minA)/2
    promB=(maxB-minB)/2
    model=Model(fun10)
    model.set_param_hint('A', value=promA, min=minA, max=maxA)   #a=SO*F
    model.set_param_hint('B', value=promB, min=minB, max=maxB)   #B=So(1-f)
    model.set_param_hint('d', value=promd, min=mind, max=maxd)    #d=D*-ivim
    model.set_param_hint('D', value=promD, min=minD, max=maxD)    #D-ivim
    params = model.make_params()
    result = model.fit(y0, params, x=x0)
    parametros=list(result.best_values.values())
    aux=result.params
    output.append(parametros) # Output[0]= lista de paramteros
    output.append(result)     # Output[1]=result
    output.append(aux)        # Output[2]=result params (para sacar errores)
    # print(result.fit_report())
    #result.plot_fit() 
    #plt.show()
    return output
    # # promncf=(maxncf-minncf)/2
    
    # ###### PARAMETROS MODELO MODIFICADO
    # output=[]
    # # minf=0.09
    # # maxf=1
    # # mind=0.03
    # # maxd=9.0
    # # minD=0.01
    # # maxD=0.18
    # # mink=0.02
    # # maxk=20
    # #######PARAMETROS PARA MODELO ORIGNIAL
    # #cin b normal
    # # corrK1=corrK
    # # corrd1=corrd
    # # print('CorrK1A',corrK1)
    # model=Model(fun10)
    # model.set_param_hint('A', value=promA, min=minA, max=maxA)
    # model.set_param_hint('B', value=promB, min=minB, max=maxB) 
    # # model.set_param_hint('SO', value=y0[0], min=0.80*y0[0], max=1.20*y0[0]+0.5)
    # # model.set_param_hint('f', value=promf, min=minf, max=maxf)   #f-ivim
    # model.set_param_hint('d', value=promd, min=mind, max=maxd) #d=D*-ivim
    # model.set_param_hint('D', value=promD, min=minD, max=maxD) #D-ivim
    # # model.set_param_hint('K', value=promk, min=mink, max=maxk)   #K-kurtosis
    # # model.set_param_hint('corrK', value=corrK, min=0.98*corrK, max=corrK) 
    # #model.set_param_hint('ncf', value=promncf, min=minncf, max=maxncf) 

    # # #### Con b/100
    # # model=Model(triexp)
    # # model.set_param_hint('SO', value=s0, min=0.80*s0, max=1.20*s0+0.5) #   parametros[0]
    # # model.set_param_hint('f', value=0.2, min=minf, max=maxf)    #f-ivim                         parametros[1]
    # # model.set_param_hint('d', value=0.7, min=mind, max=maxd)    #d=D*-ivim                      parametros[2]
    # # model.set_param_hint('D', value=0.1, min=minD, max=maxD)    #D-ivim                         parametros[3]
    # # model.set_param_hint('K', value=3.0, min=mink, max=maxk)    #K-kurtosis                     parametros[4]
    # params = model.make_params()
    # result = model.fit(y0, params, x=x0)
    # parametros=list(result.best_values.values())
    # aux=result.params
    # # aux1=result.params.stderr
    # # aux2=result.params.value
    # output.append(parametros) # Output[0]= lista de paramteros
    # output.append(result)     # Output[1]=result
    # output.append(aux)        # Output[2]=result params (para sacar errores)
    # print(result.fit_report())
    # result.plot_fit() 
    # plt.show()
    # return output

def ajuste2(x0,y0,c2,c3):
    output=[]
    # global c11
    global c21
    global c31
    # c11=c1     #S0
    c21=c2       #f
    c31=c3   
    #print('c11,cc21,c31',c11,c21,c31)  #D*
    mink=0.3*6.0/corrK
    maxk=4.0*6.0/corrK
    minD=0.0001*corrMag     #mm2/s
    maxD=0.0018*corrMag   
    mind=0.001*corrMag      #mm2/s
    maxd=0.04*corrMag   #mm2/s
    promD=(maxD-minD)/2
    promk=(maxk-mink)/2
    promd=(maxd-mind)/2
    model2=Model(kurtosis)
    model2.set_param_hint('D', value=promD, min=minD, max=maxD)   #D
    model2.set_param_hint('K', value=promk, min=mink, max=maxk)   #K
    params = model2.make_params()
    result2 = model2.fit(y0, params, x=x0)
    parametros=list(result2.best_values.values())
    aux=result2.params
    output.append(parametros)                                   #Output[0]= lista de paramteros
    output.append(result2)                                      #Output[1]=result
    output.append(aux)                                          #Output[2]=result params (para sacar errores)
    # print(result.fit_report())
    # result2.plot_fit() 
    # plt.show
    # plt.close()
    return output


def addDCM(DCMorigen,listofmaps):
###################################################################
    ##### HEREDAR DICOM
    modification_time = time.strftime("%H%M%S")
    #dcm = pydicom.dcmread(Dcm_todo[B0Ref])
    dcm =DCMorigen
    path_carpeta_final = input("Ingrese el path del directorio final donde se guardarán las imágenes convertidas: ")
    #Loop que lee y analiza las imágenes
    # i=0
    mapsnumber=6
    for k in range(mapsnumber):
        print(k)
        path_esp = f"/MAPA{k}.dcm" #última parte del path con que se van a guardar las imágenes dicom finales
        path_final_esp = path_carpeta_final + path_esp #path completo con que se va a guardar cada imagen dicom final
        np_frame1=listofmaps[k]
        dcm.Rows = np_frame1.shape[0]
        dcm.Columns = np_frame1.shape[1]
        dcm[0x0020,0x0011].value=random.randint(200,500)+k 
        dcm.PhotometricInterpretation = "MONOCHROME2"
        dcm.SamplesPerPixel = 1
        dcm.BitsStored = 16
        dcm.BitsAllocated = 16
        dcm.HighBit = 15
        dcm.PixelRepresentation = 1
        dcm.PixelData = np_frame1.tobytes()
        dcm.SeriesDescription = 'MAP'+str(k)
        dcm.SeriesInstanceUID = pydicom.uid.generate_uid()
        dcm[0x008,0x0031].value=modification_time
        dcm[0x008,0x0018].value=dcm[0x008,0x0018].value+str(1)
        dcm[0x008,0x0008].value='SECONDARY'
        dcm.save_as(path_final_esp)
        print(path_final_esp)

def triexp(x,SO,f,d,D,K):
    return (SO*f*np.exp(-x*d))+(SO*(1-f)*np.exp(-x*D+(x*x*D*D*K/6)))

def triexp2(x,A1,A2,d,D,K):
    return (A1*np.exp(-x*d))+(A2*np.exp(-x*D+(x*x*D*D*K)))

def gausiana(x,A,B,C,D,E):
    return A+B*x+C*np.exp(-D*((x-E)*(x-E)))

def gausiana2(x,A,B,C,D,E,F,G,H):
    return A+B*x+C*np.exp(-D*((x-E)*(x-E)))+F*np.exp(-G*((x-H)*(x-H)))

def gausiana3(x,F,G,H):
    return F*np.exp(-G*((x-H)*(x-H)))

def gausiana4(x,C,D,E):
    return C*np.exp(-D*((x-E)*(x-E)))


def printmaps(matriz,mapa,cROI,sizex,sizey):
    listofmaps=[]
    z=0
    mapnumber=4
    for i in range(sizex):
        for j in range (sizey):
            mapa[(i+cROI[1]),(j+cROI[0])]=matriz[z][i][j]
    plt.imshow(mapa, cmap = plt.cm.bone)
    plt.title('map')
    plt.show()
    return mapa


##########################################
##########################################
################# Funcion principal
##########################################
##########################################

def main():
    root = tk.Tk()#Abre cuadro de diálogo
    root.withdraw()
    file_name = filedialog.askopenfilenames(filetypes= [('image','dcm')],title="Archivos")
    #Error por si el archivo está vacío
    conerr=0
    EmptyString=''
    if file_name is EmptyString:
        print("Error",conerr,": No seleccionó archivo.")
        sys.exit(0)
    conerr+=1
    ############################
    Dcm_todo=[]
    cont0=0
    #####################
    #Gestion de Imagen DICOM
    #####################
    for i in file_name:
        file_name=decompress(i)                     #Descomprimo imagenes
        dcm=pydicom.dcmread(i)               
        Dcm_todo.append(dcm)                        #Lista con todas los datos del DICOM
        Data_img=np.copy(dcm.pixel_array)
        Dcm_imagen.append(Data_img)                 #Lista con todas las imágenes,numpy
        infoimagenes=Reader(dcm)                    #Lista uni-imagen con informacion DICOM
        conerr+=2       
        clases=sort_out(infoimagenes,cont0)         #Colecciones DWI
        cont0+=1
    # print(clases)
    Dcm_imgposition=clases[0]
    repeticion=clases[1]
    repeticionsl=clases[2]
    totalslices=clases[3]
    referencia=clases[5]
    bvalues=repeticion.keys()
    bvalues=list(bvalues)
    bnumber=len(bvalues)

    ##################
    #Creo y lleno diccionario para organizar DWI
    ###############
    obj2={}                                      
    for k in range(totalslices):
        obj2['Slice'+str(k)]=[]
    cont0=0
    for i in range(len(Dcm_imgposition)):
        vaux0=Dcm_imgposition[i]
        vaux0=str(vaux0)
        t=[]
        for g in range(len(repeticionsl)):
            vaux1=list(repeticionsl.keys())[g]
            vaux1=str(vaux1)
            if vaux0==vaux1:
                t=obj2["Slice"+str(g)]
                t.append(cont0)
        cont0+=1
    #print(obj2)

####################REORDENAMIENTO###########
    objprueba={}
    for k in range(totalslices):
        objprueba['Slice' + str(k)]=[]
    print(objprueba)
    for l in obj2.keys():
        print(l)
        laux0=obj2.get(str(l))
        vaux0=len(laux0)
        laux1=[0]*vaux0
        #print('esta es laux0 y laux1',laux0,laux1)
        for d in range(bnumber):
            laux2=[]
            laux2=Reader(Dcm_todo[laux0[d]])
            cont0=0
            for i in range(bnumber):
                laux3=Reader(Dcm_todo[laux0[i]])
                if laux3[6]<laux2[6]:
                    cont0+=1
            #print("Componente lista:",laux0[d],laux2[6],cont0)
            laux1[cont0]=laux0[d]
        #print("laux1:",laux1)
        objprueba[str(l)].append(laux1)
        #CREAR OBJETO !!!!!!!
    #print(objprueba)
    
    #############
    #Calculamos el size de la matriz original DWI
    ############
    img_shape = Dcm_imagen[0].shape 
    bvalues=np.array(bvalues)
    print('Valores de B',bvalues)
    bvalues.sort()
    ##############
    #Seleccion de corte para el ROI
    #Almacenamiento de B0
    ##############
    g=0
    for g in range(totalslices):
        print('Slice',g)
        plt.imshow(Dcm_imagen[g], cmap = plt.cm.bone)
        plt.show()
        g=g+1
    print('The study has',totalslices,'slices')
    INCorte=input('Pick a slice to perform the ROI from images above (B0 DWI)')
    for d in range(bnumber):
        vaux0=int(list(objprueba['Slice'+str(INCorte)][0])[d])
        BOut=Dcm_todo[vaux0][0x0043,0x1039].value
        BOut1=str(BOut)
        BOut2=list(BOut1)
        if int(BOut2[2])==0:
            B0Ref=vaux0
            x1=0
        else:
            print('para BOut2',vaux0)
            x1=int(BOut2[11])+10*int(BOut2[10])+100*int(BOut2[9])+1000*int(BOut2[8])
        print(x1)
    # print("B0 index:",B0Ref)


    final_image=[]
    for d in range(bnumber):
        vaux0=int(list(objprueba['Slice'+str(INCorte)][0])[d])
        # print('Imagen de B:',bvalues[d])   
        Final_ROI=Dcm_imagen[vaux0]
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
    for k in range(totalslices):
        obj3[k]=[]
    cont0=0
    cont1=0
    for e in range(len(final_image)):
        vaux0=obj3[cont1]
        vaux0.append(e)
        cont0+=1
        if cont0==bnumber:
            cont0=0
            cont1+=1
    # print(obj3)
###################################################
####Calculo de histogramas y ajuste de Gaussiana
# ##################################################

#     # print('Ultimo b',)
#     # plt.imshow(final_image[len(bvalues)-1], cmap = plt.cm.bone)
#     # plt.show()
#     aux=plt.hist(final_image[len(bvalues)-1].ravel(),'sqrt')
#     plt.show()
#     plt.close()
#     counts=list(aux[0])
#     bins=list(aux[1])
#     counts.pop(0)
#     bins.pop(0)
#     bins.pop()
#     counts1=counts
#     bins1=bins
#     # print(len(counts1))
#     #print(bins)
   
#     #k=0
#     baux=[]
#     for m in range(len(counts)):
#         if counts[m]==0:
#             k=m
#             baux.append(k)
#     # print(baux)
#     # print(len(baux))
#     cont0=0
#     for f in baux:
#         #print(f)
#         counts1.pop(f-cont0)
#         bins1.pop(f-cont0)
#         #print('lista actallizada',counts1)
#         cont0+=1
    
#     # print('listas que entran al ajuste')
#     # print('counts1',counts1)
#     # print('bins1',bins1)
#     a=counts1.index(max(counts1))
#     # print('pico max altura',counts1[a])
#     # print('punto medio',bins1[a])
#     #### Maximos y minimos para inicializar ajuste
#     minA=0
#     maxA=20
#     minB=0.001
#     maxB=0.5
#     minC=0.5*max(counts1)
#     maxC=1.2*max(counts1)
#     minD=0.001
#     maxD=0.2
#     minE=bins1[a]-15
#     maxE=bins1[a]+15
#     minF=0.5*minC
#     maxF=0.7*maxC
#     minG=0.001
#     maxG=0.2
#     minH=bins1[a]
#     maxH=1.3*bins1[a]+0.5
#     ruido2=Model(gausiana2)
#     ruido2.set_param_hint('A', value=0.1, min=minA, max=maxA)
#     ruido2.set_param_hint('B', value=0.2, min=minB, max=maxB)               #f-ivim
#     ruido2.set_param_hint('C', value=0.8*max(counts1), min=minC, max=maxC)  #d=D*-ivim                 #  ruido.set_param_hint('D', value=0.001, min=minD, max=maxD) #D-ivim
#     ruido2.set_param_hint('D', value=0.0022, min=minD, max=maxD) 
#     ruido2.set_param_hint('E', value=bins1[a]-10, min=minE, max=maxE)
#     ruido2.set_param_hint('F', value=0.5*max(counts1), min=minF, max=maxF)    
#     ruido2.set_param_hint('G', value=0.0022, min=minG, max=maxG)  
#     ruido2.set_param_hint('H', value=bins1[a]*1.20, min=1.1*minH, max=1.1*maxH)  
#     variables2 = ruido2.make_params()
#     resultado2 = ruido2.fit(counts1, variables2, x=bins1)
#     Voptimos2=list(resultado2.best_values.values())
#     print(resultado2.fit_report())                                #Imprime resultados del reporte
   # print(resultado2.fit_report())                                #Imprime resultados del reporte
    #######Imprime resultados del ajuste
    # resultado2.plot_fit()                                          
    # # plt.plot(edges, hist, marker='o', ls="")
    # # plt.show()
    # holamundo=gausiana3(bins1,Voptimos2[5],Voptimos2[6],Voptimos2[7])
    # holamundo2=gausiana4(bins1,Voptimos2[2],Voptimos2[3],Voptimos2[4])
    # # # x,y=interse()ction()
    # # #print(holamundo)
    # plt.plot(bins,holamundo,'g' ,label='Prostate pixel infromation')
    # plt.plot(bins,holamundo2,'r',label='Gaussian noise')
    # plt.grid()
    # plt.xlabel('Pixels Intensity')
    # plt.ylabel('Counts')
    # plt.title('Histogram Method (max b = value)')
    # plt.xlim(0,35)
    # plt.savefig("graph.png")
    # plt.show() 
    # holamundo2=gausiana4(bins1,Voptimos2[2],Voptimos2[3],Voptimos2[4])
    # print(holamundo2)
    # plt.plot(bins,holamundo2,'b')
    # plt.show() 
    # #Saco interseccion entre curvas
    # a1=Voptimos2[3]-Voptimos2[6]
    # b1=2*(Voptimos2[6]*Voptimos2[7]-Voptimos2[4]*Voptimos2[3])
    # c1=(Voptimos2[3]*Voptimos2[4]*Voptimos2[4])-(Voptimos2[6]*Voptimos2[7]*Voptimos2[7])-(np.log(Voptimos2[2]/Voptimos2[5]))
    # d=(b1**2)-(4*a1*c1)
    # sol1=(-b1-cmath.sqrt(d))/(2*a1)
    # sol2=(-b1+cmath.sqrt(d))/(2*a1)
    # sol2=(-b1+cmath.sqrt(d))/(2*a1)
    # inter=sol2
    # inter=int(inter)
    # media=Voptimos2[4]                #Media del ajuste
    # dopt=Voptimos2[3]
    # desv2=cmath.sqrt(1/(2*dopt))
    # suma=media+desv2
    # listaaux1=[suma,inter]
    # valormascara=int(min(listaaux1))
    # for e in range(len(final_image)):
    #     print('imagen pre mascara',e)
    #     plt.imshow(final_image[e], cmap = plt.cm.bone)
    #     plt.show()
    valormascara=27
    ###################################################
    ########## Mascara para eliminar el ruido Gaussiano
    ###################################################
    l=0
    for i in range(img_shape[0]):
        for j in range (img_shape[1]):
            for d in range(bnumber):
                vaux5=obj3[l][d]
                if final_image[vaux5][i,j]<valormascara:
                    final_image[vaux5][i,j]=0

   
    ## HAGO EL ROI
    general_ROI=position_ROI(final_image[0])
    final_image2=[] ######Tiene las imagenes finales para ajustar
    for d in range(bnumber):
        # vaux0=int(list(obj3[l])[d])
        # print(d,l)
        print('Imagen de B:',bvalues[d])   
        Final_ROI=img_ROI(final_image[d],general_ROI)
        # print(d)
        final_image2.append(Final_ROI)
    tgp=general_ROI #Coordenadas del ROI
    tgp=list(tgp)
    img_shapefinal=Final_ROI.shape
    img_shapefinal=list(img_shapefinal)


####################################################
    

####################################################
########### Ajuste de las funciones
####################################################
    minf=0.01            #%
    maxf=0.8             #%
    mind=0.001*corrMag   #mm2/s
    maxd=0.04*corrMag    #mm2/s  
    minD=0.0001*corrMag  #mm2/s
    maxD=0.0018*corrMag  #mm2/s
    mink=0.3*6.0/corrK
    maxk=4.0*6.0/corrK
    promd=(maxd-mind)/2
    promD=(maxD-minD)/2
    # promA=(maxA-minA)/2
    # promB=(maxB-minB)/2
    matriz0=np.zeros((totalslices,img_shapefinal[0],img_shapefinal[1]))  #f depejado
    matriz1=np.zeros((totalslices,img_shapefinal[0],img_shapefinal[1]))  #D*
    matriz2=np.zeros((totalslices,img_shapefinal[0],img_shapefinal[1]))  #D
    matriz3=np.zeros((totalslices,img_shapefinal[0],img_shapefinal[1]))  #S0
    matriz4=np.zeros((totalslices,img_shapefinal[0],img_shapefinal[1]))  #D: de la ecuacion
    matriz5=np.zeros((totalslices,img_shapefinal[0],img_shapefinal[1]))  #Kurtosis
    #matriz4=np.zeros((totalslices,img_shapefinal[0],img_shapefinal[1])) 
    #for l in obj3.keys():      
    bvalues=bvalues/corrMag                                                                      #Para multiples Slices
    l=0                                                                                             #Para un unico Slice
    for i in range(img_shapefinal[0]):
        print("i:",i,"de",img_shapefinal[0])
        for j in range(img_shapefinal[1]):
            # print("j:",j,"de",img_shapefinal[1])
            signal=[]
            for d in range(bnumber):
                vaux0=int(list(obj3[l])[d])
                #vaux0=int(vaux0)
                vaux1=int(final_image2[vaux0][i,j])
                signal.append(vaux1)
            # print('signal',signal)
            signal1=np.array(signal)
            signal2=np.array(signal)
            if signal[bnumber-1]>0:
                signal1=signal1*corrA
                # print('es prom D',promD,promA,promB,)
                # for c in (signal1):
                #     aux33=fun10(c,promA,promB,promd,promD)
                #     prueba.append(aux33)
                # plt.plot(bvalues,prueba,'y')
                # plt.plot(bvalues,signal1,'b')
                # plt.show()
                # print('valoresB',bvalues)
                # print('signal',signal1)
                resultado=ajuste1(bvalues,signal1)
                parametros=resultado[0]
                #errores=calculoerror(resultado[2])
                auxS0=(parametros[0]+parametros[1])/corrA
                auxf=parametros[0]/(parametros[0]+parametros[1])
                auxd=parametros[2]
                # print('auxf  auxd auxs0',auxf,auxd,auxS0)
                # print('Signal2',signal2)
                # signal2=signal2/auxS0
                # resultado2=ajuste2(bvalues,signal2,auxf,auxd)
                # plt.plot(bvalues,signal2,'g')
                # plt.show()
                # print('entro aca parte 2')
                # parametros2=resultado2[0]
                matriz3[l,i,j]=auxS0      
                if auxf<minf or auxf>maxf:
                    matriz0[l,i,j]=0
                else:
                    matriz0[l,i,j]=int(math.floor(0.5+511*(auxf-minf)/(maxf-minf)))
                    print('f-original',auxf,'f-modi',matriz0[l,i,j])
                if parametros[2]<mind or parametros[2]>maxd:
                    matriz1[l,i,j]=0
                else:
                    matriz1[l,i,j]=int(math.floor(0.5+511*(parametros[2]-mind)/(maxd-mind)))
                    print('d-original',auxf,'d-modi',matriz1[l,i,j])
                if parametros[3]<minD or parametros[3]>maxD:
                    matriz2[l,i,j]=0
                else:
                    matriz2[l,i,j]=int(math.floor(0.5+511*(parametros[3]-minD)/(maxD-minD))) 
                    print('D-original',auxf,'D-modi',matriz2[l,i,j])


            else:
                matriz0[l,i,j]=-8
                matriz1[l,i,j]=-8
                matriz2[l,i,j]=-8
                matriz3[l,i,j]=-8
                # matriz2[l,i,j]=0
                # matriz3[l,i,j]=0
                # matriz4[l,i,j]=0
                # matriz5[l,i,j]=0
            #print('###############################################################')
    listamatrices=[]
    listamatrices.append(matriz0)
    listamatrices.append(matriz1)
    listamatrices.append(matriz2)
    listamatrices.append(matriz3)
    listamatrices.append(matriz4)
    listamatrices.append(matriz5)
    #print(len(listamatrices))
    l=0
    #Genero mapas en negro
    mapsnumber=6
    listamapas=[]
    for t in range(mapsnumber):
        map=np.zeros((img_shape[0],img_shape[1]),dtype=np.int16)
        listamapas.append(map)
    mapascoef=[]
    #### Pego matriz en los mapas
    for r in range(mapsnumber):
        map=printmaps(listamatrices[r],listamapas[r],tgp,img_shapefinal[0],img_shapefinal[1])
        mapascoef.append(map)
        print(len(mapascoef))
    ### Le agrego DICOM a los mapas
    addDCM(Dcm_todo[B0Ref],mapascoef)

        

# #Ejecuta función main() 
if __name__ == '__main__':
    main()