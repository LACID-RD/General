from inspect import CO_ITERABLE_COROUTINE
from operator import contains
import cmath
import matplotlib.pyplot as plt
from numpy.lib.npyio import save
from skimage.io import imread, imsave
import tkinter as tk
from tkinter import filedialog
import numpy as np
from pydicom.uid import generate_uid
import collections
from scipy.optimize import least_squares, minpack2
import math
from lmfit import Model
from lmfit import Parameters,minimize,fit_report



##########################################################################################
##########################################################################################
############################# CLASE Proc #################################################
##########################################################################################
##########################################################################################
'''
Clase asociada al procesamiento de la imagen 
'''
class PProc():

    ########################################
    ########################################
    # Define variables de la clase
    ########################################
    ########################################

    def __init__(self,geometry,bvalues,objprueba,final_image2): #pat_name=None,type=0,time=0,slice=0,img=None,te=0,tr=0,
        #self.geometry=geometry
        geometry=[int(x) for x in geometry]
        self.coMinX=geometry[1]
        self.coMaxX=geometry[3]
        self.coMinY=geometry[2]
        self.coMaxY=geometry[4] 
        self.sizeX=geometry[6]
        self.sizeY=geometry[7]
        self.sliceA=geometry[9]
        #print(self.sliceA,geometry[9])
        self.bvalues=np.array(bvalues)
        self.bnumber=geometry[5]
        self.dicOrdImg=objprueba
        self.dcmImagen=final_image2
        ### Variables locales
        self.corrA=100           #Corrección para la levantar (por el ln) la intensidad de señal
        self.corrB=0.01          #Corrección para disminuir los valores de b
        #self.chiCua=0.04         #Límite superior de Chi2
        #self.reChi2=0.008        #Límite superior de redChi2
        self.chiCua=100          #Límite superior de Chi2
        self.reChi2=100          #Límite superior de redChi2
        self.valMas=200          #Valor positivo de la mascara
        #self.corrD=500          #Corrección para levantar los valores del ADC(d) y de D*(D)
        maskCh2=np.zeros((self.sizeX,self.sizeY))
        maskrCh=np.zeros((self.sizeX,self.sizeY))
        maskThr=np.zeros((self.sizeX,self.sizeY))
        mapADC=np.zeros((self.sizeX,self.sizeY))
        self.maskCh2=maskCh2     #mascara para filtrar la cantidad de ajustes por Chi2
        self.maskrCh=maskrCh     #mascara para filtrar la cantidad de ajustes por redChi2
        self.mapADC=mapADC       #mapa d interno, dividido por coorB
        self.maskThr=maskThr


    def maskThrhl(self):
        ###################################################
        ########## Mascara para eliminar el ruido Gaussiano
        ###################################################
        #valormascara=67
        valormascara=40
        print('Haciendo mascara')
        print(self.dicOrdImg)
        self.sliceA=self.sliceA-1
        print("Slice:",self.sliceA)
        vaux5=list(self.dicOrdImg['Slice'+str(self.sliceA)])
        print("Slice:",self.sliceA,"vaux5:",vaux5[0][0])
        plt.imshow(self.dcmImagen[vaux5[0][0]], cmap = plt.cm.bone)
        plt.show()
        for i in range(self.sizeX):
            #print('i',i)
            for j in range (self.sizeY):
                vaux1=int(self.dcmImagen[vaux5[0][0]][i,j])
                if vaux1<valormascara:
                    #print(i.type)
                    self.maskThr[i,j]=0
                else:
                    self.maskThr[i,j]=self.valMas
                    
        print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$ ',)
        #for e in range(len(self.dcmImagen)):
        print('imagen post mascara')
        plt.imshow(self.maskThr, cmap = plt.cm.bone)
        plt.show()
    

       
    ########################################
    ########################################
    # Funcion lineal
    ########################################
    ########################################

    def FunLin(self,params,x,y):
        A = params['A']
        B = params['B']
        y_fit = B-A*x
        return y_fit-y

    
    ########################################
    ########################################
    # Funcion exponencial
    ########################################
    ########################################

    def FunExp(x,A,B,C):
        return (A*np.exp(-x*B)+C)


    ########################################
    ########################################
    # Modelo ADC(d)
    ########################################
    ########################################

    def model_adc(self):
        minMapd=0.001/self.corrB                       #mm2/s
        maxMapd=0.04/self.corrB                        #mm2/s    
        matriz2=np.zeros((self.sizeX,self.sizeY))      #mapa d externo (con ajuste para visualizacion)
        #print("PProc-Modelo_ADC bvalues",self.bvalues)
        self.bvalues=self.bvalues*self.corrB
        maskThr=self.maskThrhl()
        print("Calculando mapa ADC")       
        for i in range(self.coMinY,self.coMaxY):
            for j in range(self.coMinX,self.coMaxX):
                signal=[]
                for d in range(self.bnumber):
                    vaux0=int(list(self.dicOrdImg['Slice'+str(self.sliceA)])[0][d])
                    vaux1=int(self.dcmImagen[vaux0][i,j])
                    signal.append(vaux1)
                signal1=np.array(signal)
                if (all(x>0 for x in signal)):
                #if signal[0]>0 and signal[self.bnumber-1]>0: #Si la intensidad del primer o el último valor de b no es cero (es decir, hay señal !!!)
                    signal1=signal1*self.corrA
                    if maskThr[i,j]!=0:                    
                        resultado=self.monoExp(signal1)
                        #if resultado[0]>minMapd and resultado[0]<maxMapd and resultado[3]<self.reChi2: #Valores esperados
                        self.maskrCh[i,j]=self.valMas
                        self.mapADC[i,j]=resultado[0]  #Se guarda el resultado de ADC(d)*corrB
                        matriz2[i,j]=resultado[0]*100
                        # matriz2[i,j]=int(math.floor(0.5+511*(resultado[0]-minMapd)/(maxMapd-minMapd))) #Normaliza a niveles de gris de 512 : OJOOOOO
                        if resultado[2]<self.chiCua:       #Valores esperados para redChi2
                            self.maskCh2[i,j]=self.valMas
            
        
    

        ## Chi2
        plt.imshow(self.maskCh2,cmap=plt.cm.bone)
        plt.title('Mascara por Chi2')
        plt.show()
        ## redChi2
        plt.imshow(self.maskrCh,cmap=plt.cm.bone)
        plt.title('Mascara por redChi2')
        plt.show()
        ## ADC sin corregir
        plt.imshow(self.mapADC,cmap=plt.cm.bone)
        plt.title('ADC sin corregir')
        plt.show()
        
        return matriz2
        

    ########################################
    ########################################
    # Ajuste monoexp. (mínimos cuadrados)
    ########################################
    ########################################

    def monoExp(self,vecLin_y):
        #recibe todos los valores de b, hay que limitar el cálculo entre 200 y 800
        minb=199*self.corrB
        maxb=1001*self.corrB
        output=[]
        vecLog_x=[]
        vecLog_y=[]

        for d in range(self.bnumber):
            if self.bvalues[d]>minb and self.bvalues[d]<maxb:
                vecLog_x.append(self.bvalues[d])
                vecLog_y.append(np.log(vecLin_y[d]))
        aux0=int(len(vecLog_x))-1
        arrLog_x=np.array(vecLog_x)
        arrLog_y=np.array(vecLog_y)
        promA=(arrLog_y[0]-arrLog_y[aux0])/(arrLog_x[aux0]-arrLog_x[0])
        promB=arrLog_y[0]+promA*arrLog_x[0]
        minA=promA*0.75
        maxA=promA*1.25
        minB=promB*0.75
        maxB=promB*1.25
        if maxA>minA and maxB>minB:
            params=Parameters()
            params.add('A',value=promA,min=minA,max=maxA)  #A=D*corrB
            params.add('B',value=promB,min=minB,max=maxB)  #B=ln(So*corrA)
            #Calling the minimize function. Args contains the x and y data.
            fitted_params=minimize(self.FunLin,params,args=(arrLog_x,arrLog_y,), method='least_squares')
            output.append(fitted_params.params['A'].value) #op[0], A
            output.append(fitted_params.params['B'].value) #op[1], B
            output.append(fitted_params.chisqr)            #op[2], Chi2
            output.append(fitted_params.redchi)            #op[3], redChi2
            #plt.plot(arrLog_x,arrLog_y,'g')
            #plt.show()
            # calculate final result
            # final = arrLog_y + fitted_params.residual
            # plt.plot(arrLog_x,arrLog_y , '+')
            # plt.plot(arrLog_x, final)
            # plt.show()
        else:
            output.append(0)  #op[0]
            output.append(0)  #op[1]
            output.append(10) #op[2]
            output.append(10) #op[3]

        '''
        model=Model(self.FunLin)
        params = model.make_params()
        model.set_param_hint('A', value=promA, min=minA, max=maxA)   #A=D*corrB
        model.set_param_hint('B', value=promB, min=minB, max=maxB)   #B=ln(So*corrA)
        #params = model.make_params()

        print("Ajuste:",arrx,arry)
        #result = model.fit(vecLog_y, params, x=vecLog_x)
        result = model.fit(arry, params, x=arrx)
        parametros=list(result.best_values.values())
        aux=result.params
        output.append(parametros) # Output[0]= lista de paramteros
        output.append(result)     # Output[1]=result
        output.append(aux)        # Output[2]=result params (para sacar errores)
        '''
        return output
        

    ########################################
    ########################################
    # Modelo IVIM (S0, D* y f)
    ########################################
    ########################################

    def model_ivim(self):       
        matrices=[]
        matriz0=np.zeros((self.sizeX,self.sizeY))  #f
        matriz1=np.zeros((self.sizeX,self.sizeY))  #D*(D)
        matriz3=np.zeros((self.sizeX,self.sizeY))  #S0
        maskThr=self.maskThrhl()
        print("Calculando mapas f, D* y S0")
        for i in range(self.coMinY,self.coMaxY):
            #print("Barre por filas, i:",i,"de",self.coMaxY)    #Barre en Y
            for j in range(self.coMinX,self.coMaxX):    
                signal=[]
                for d in range(self.bnumber):
                    vaux0=int(list(self.dicOrdImg['Slice'+str(self.sliceA)])[0][d])
                    vaux1=int(self.dcmImagen[vaux0][i,j])
                    signal.append(vaux1)
                signal1=np.array(signal)
                # if self.maskrCh[i,j]>(0.95*self.valMas):
                if maskThr[i,j]!=0:
                    if self.bvalues[0]==0:         #Se extrae el valor de S0
                        valS0=signal1[0]
                    else:
                        valS0=1.15*signal1[0]
                    print("signal",signal1)
                    print("bvalues",self.bvalues)
                    print("ADC",self.mapADC[i,j])
                    print("S0:",valS0)
                    signal1=signal1*np.exp(self.bvalues*self.mapADC[i,j])
                    signal1=signal1*self.corrA 
                    valS0=signal1[0]
                    result=self.biExpo(signal1,valS0,self.mapADC[i,j])
                    matriz0[i,j]=result[0]*100
                    matriz1[i,j]=result[1]*100
                    matriz3[i,j]=result[2]*100
                    
                    #if resultado[0]>minMapd and resultado[0]<maxMapd and resultado[2]<PProc.chiCua: #Valores esperados
                    #self.redMask[i,j]=200
                    #matriz2[i,j]=int(math.floor(0.5+511*(resultado[0]-minMapd)/(maxMapd-minMapd))) #Normaliza a niveles de gris de 512  
        matrices.append(matriz0)
        matrices.append(matriz1)
        matrices.append(matriz3)
        '''
        ## Mapa f
        plt.imshow(matriz0,cmap=plt.cm.bone)
        plt.title('Mapa f')
        plt.show()
        ## Mapa D*
        plt.imshow(matriz1,cmap=plt.cm.bone)
        plt.title('Mapa D*')
        plt.show()
        ## Mapa S0
        plt.imshow(matriz3,cmap=plt.cm.bone)
        plt.title('Mapa S0')
        plt.show()
        '''
        return matrices
    

    ########################################
    ########################################
    # Ajuste biexponencial
    ########################################
    ########################################

    def biExpo(self,signal1,valS0,valADC):
        #minMapf=0.01                               #%
        maxMapf=0.9                                 #%
        #minMapD=0.0001/self.corrB                  #mm2/s
        # maxMapD=0.0018/self.corrB                   #mm2/s
        maxMapD=0.004/self.corrB  
        output=[]
        
        Aprom=valS0*0.5*maxMapf                     #A=S0*f
        Amin=0.1; Amax=valS0
        # Bprom=valADC-0.5*maxMapD                    #B=ADC-D* (d-D)
        Bprom=(0.8*maxMapD)-valADC
        Bmin=0.001; Bmax=2*Bprom
        Cprom=valS0*(1-0.5*maxMapf)                 #C=S0*(1-f)
        Cmin=0.1; Cmax=valS0
        self.bvalues=list(self.bvalues)
        signal1=list(signal1)
        self.bvalues.pop()
        signal1.pop()
        self.bvalues.pop()
        signal1.pop()
        self.bvalues=np.array(self.bvalues)
        signal1=np.array(signal1)
        model=Model(PProc.FunExp)
        model.set_param_hint('A', value=Aprom, min=Amin, max=Amax) #A
        model.set_param_hint('B', value=Bprom, min=Bmin, max=Bmax) #B
        model.set_param_hint('C', value=Cprom, min=Cmin, max=Cmax) #C
        params=model.make_params()
        result=model.fit(signal1,params,x=self.bvalues)
        valVar=list(result.best_values.values())
        #VAux0=result.params
        #vecAux.append(valVar)                      #v[0]: Lista de paramteros
        #vecAux.append(result)                      #v[1]: Result
        #vecAux.append(VAux0)                       #v[2]: Result params (para sacar errores)
        output.append(valVar[0]/(valVar[2]+valVar[0])) #out[0]: f=A/(A+C)
        #output.append(valADC-valVar[1])             #out[1]: D*=ADC-B
        output.append(valVar[1]-valADC)             #out[1]: D*=B-ADC
        output.append(valVar[0]/output[0])          #out[2]: S0=A/f
        # Start Up... deberìa estar muy cerca
        ####################################
        #qc1fitA=[]
        #for d in x0:
    #     aux=FunExp(d,Aprom,Bprom,Cprom)
    #     qc1fitA.append(aux)
        #plt.plot(x0,qc1fitA,'r')
        #result.plot_fit() 
        #plt.plot(x0,signal1,'+')
        #plt.show()

        return output