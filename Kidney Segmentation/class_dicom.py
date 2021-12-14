import pydicom
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import numpy as np
import sys
import gdcm

class ObjetoDicom:
    def DescomDicom(self,PathD):
        reader=gdcm.ImageReader()
        reader.SetFileName(PathD)
        if not reader.Read():        
            print("Error: No se leen correctamente las imágenes.")
            sys.exit(0)
        change = gdcm.ImageChangeTransferSyntax()
        change.SetTransferSyntax( gdcm.TransferSyntax(gdcm.TransferSyntax.ImplicitVRLittleEndian) )
        change.SetInput( reader.GetImage() )
        if not change.Change():
            print("Error: No se descomprime correctamente las imágenes.")
            sys.exit(0)
        writer = gdcm.ImageWriter()
        writer.SetFileName(PathD)
        writer.SetFile(reader.GetFile())
        writer.SetImage(change.GetOutput())
        if not writer.Write():
            print("Error: No se escriben correctamente las imágenes.")
            sys.exit(0)


    def ReaderDicom(self,PathD):  #Reads DiCOM files specific  information 
        ffReDC=[]
        DcmAux=pydicom.dcmread(PathD)
        ########################################### Media Storage [0] FILE-META !!
        if DcmAux.file_meta.MediaStorageSOPClassUID == '1.2.840.10008.5.1.4.1.1.4':
            ffReDC.append(0) #En este caso es imagen normal (no captura secundaria)
        elif DcmAux.file_meta.MediaStorageSOPClassUID == '1.2.840.10008.5.1.4.1.1.4.1':
            ffReDC.append(1) #En este caso es enhanced MR Image Storage (poscontraste)
        elif DcmAux.file_meta.MediaStorageSOPClassUID == '1.2.840.10008.5.1.4.1.1.7':
            ffReDC.append(2) #En este caso es captura secundaria
        elif DcmAux.file_meta.MediaStorageSOPClassUID == '1.2.840.10008.5.1.4.1.1.4.2':
            ffReDC.append(3) #En este caso es Spectroscopy Storage
        elif DcmAux.file_meta.MediaStorageSOPClassUID == '1.2.840.10008.5.1.4.1.1.4.3':
            ffReDC.append(4) #En este caso es enhanced MR Color Image Storage
        elif DcmAux.file_meta.MediaStorageSOPClassUID == '1.2.840.10008.5.1.4.1.1.4.4':
            ffReDC.append(5) #En este caso es Legacy Converted Enhanced MR Image Storage           
        else:
            print("Error al leer el tipo de imagen - media storage (captura secundaria vs imagen normal) del file meta")
            sys.exit(0)
        ########################################### Transfer Syntax [1] FILE-META !! 
        if DcmAux.file_meta.TransferSyntaxUID == '1.2.840.10008.1.2.4.70':
            ffReDC.append(0) #JPEG Lossless, Non-Hierarchical, First-Order Prediction MIRAR http://dicom.nema.org/medical/dicom/current/output/chtml/part18/sect_8.7.3.html
        elif DcmAux.file_meta.TransferSyntaxUID == '1.2.840.10008.1.2':
            ffReDC.append(1) #Implicit VR Little Endian MIRAR http://dicom.nema.org/medical/dicom/current/output/chtml/part18/sect_8.7.3.html
        elif DcmAux.file_meta.TransferSyntaxUID == '1.2.840.10008.1.2.4.90':
            ffReDC.append(2) #JPEG 2000 Image Compression (Lossless Only) MIRAR http://dicom.nema.org/medical/dicom/current/output/chtml/part18/sect_8.7.3.html
        else:
            print("Error al leer el transfer syntax (captura secundaria vs imagen normal) del file meta")
            sys.exit(1)
        ########################################### Source Application Entity Title [2] (workstation o equipo del que salió la imagen) FILE-META !!
        #ffReDC.append(DcmAux.file_meta[0x0002,0x0016].value)
        ########################################### Modalidad [3]
        #ffReDC.append(DcmAux[0x0008,0x0060].value) # 3:Modalidad 
        #if "MR" not in ffReDC[3]:
            #print("Error 4: Las imágenes no son de MR.")
            #sys.exit(4)
        ########################################### Fabricante [4]
        #ffReDC.append(DcmAux[0x0008,0x0070].value)
        ########################################### TR [5]
        #ffReDC.append(DcmAux[0x0018,0x0080].value)
        ########################################### TE [6]
        #ffReDC.append(DcmAux[0x0018,0x0081].value)
        ########################################### Tipo de Sec [7]
        #ffReDC.append(DcmAux[0x0018,0x0020].value)
        ########################################### Grosor de slice [8]
        #ffReDC.append(DcmAux[0x0018,0x0050].value)
        ########################################### Campo externo [9]
        #ffReDC.append(DcmAux[0x0018,0x0087].value)
        ########################################### Codi. de fase [10]
        #ffReDC.append(DcmAux[0x0018,0x1312].value)
        ########################################### Acquisition Number [11]
        #ffReDC.append(DcmAux[0x0020,0x0012].value)   
        ########################################### Img in Acquisition [12]
        #ffReDC.append(DcmAux[0x0020,0x1002].value)
        ########################################### Stack ID [12]
        #ffReDC.append(DcmAux[0x0020,0x9056].value)                
        ########################################### In-Stack Position Number [12]
        #ffReDC.append(DcmAux[0x0020,0x9057].value)  
        ########################################### Num de filas [12]
        #ffReDC.append(DcmAux[0x0028,0x0010].value)
        ########################################### Num de colum [13]
        #ffReDC.append(DcmAux[0x0028,0x0011].value)
        #### 14: Posicion de la imagen, posición del centro del primer vóxel (izquierda-superior de la imágen) en mm; X: L-R,  Y: A-P,  Z: H-F  11
        #### 15: Orientación de la imagen, cosenos directores de la primer fila y columna 12
        #### 16: Tamaño de píxel: fila y columna 13
        #### 17: SOLO PHILIPS... Trigger time
        # if "SIE" in ffReDC[4]:
        #     ffReDC.append(DcmAux[0x0020,0x0032].value)
        #     #Cosenos directores de la primera fila y columna)
        #     ffReDC.append(DcmAux[0x0020,0x0037].value)
        #     ffReDC.append(DcmAux[0x0028,0x0030].value)
        # elif "GE" in ffReDC[4]:
        #     ffReDC.append(DcmAux[0x0020,0x0032].value)
        #     ffReDC.append(DcmAux[0x0020,0x0037].value)
        #     ffReDC.append(DcmAux[0x0028,0x0030].value)
        # elif "Phil" in ffReDC[4]:
        #     #ffImPo2=DcmAux[0x5200,0x9230][0]
        #     ffImPo1=ffImPo2[0x0020,0x9113][0]
        #     ffReDC.append(ffImPo1[0x0020,0x0032].value)
        #     ffSFGS=DcmAux[0x5200,0x9229][0]
        #     ffImOr1=ffSFGS[0x0020,0x9116][0]
        #     ffReDC.append(ffImOr1[0x0020,0x0037].value)
        #     #SliOri=dcm[0x2001,0x100b].value
        #     #print("SlsOri: ",SliOri)
        #     #ScaTec=dcm[0x2001,0x1020].value
        #     #print("ScaTec: ",ScaTec)
        #     ffPiSp1=ffSFGS[0x0028,0x9110][0]
        #     ffReDC.append(ffPiSp1[0x0028,0x0030].value)
        #     ############## 4DFlow
        #     #print("Aux:",str(DcmAux[0x2001,0x1020].value),DcmAux[0x2005, 0x106e].value)
        #     if  ('T1TFE' in str(DcmAux[0x2001,0x1020].value)) and ('PCA' in str(DcmAux[0x2005, 0x106e].value)): #info gral de la secuencia
        #         pcvelocity=DcmAux[0x2001, 0x101a].value
        #         print("p0",list(pcvelocity))                         # 1
        #         print("p1",int.from_bytes(pcvelocity,"big"))                         # 1
        #         print("p2",int.from_bytes(pcvelocity,"little"))                      # 256
        #         print("p3",int.from_bytes(pcvelocity,"big",signed="False"))
        #         print("p4",int.from_bytes(pcvelocity,"little",signed="False"))

        #         #arbBytesAsString = pcvelocity.decode('string')
        #         #print(arbBytesAsString)
        #         #arr=DcmAux.overlay_array(0x2001) 
        #         print("pcvel:",pcvelocity,"arr:")
        #         #phormag=str(DcmAux[0x2005, 0x106e].value)
        #         ffReDC.append(DcmAux[0x0018,0x1060].value)  #Trigger time
        #         if pcvelocity[0]>50 and pcvelocity[1]>50 and pcvelocity[2]>50:
        #             ffReDC.append(0)
        #         elif pcvelocity[0]==0 and pcvelocity[1]>50 and pcvelocity[2]==0: #AP
        #             ffReDC.append(1)
        #         elif pcvelocity[0]>50 and pcvelocity[1]==0 and pcvelocity[2]==0: #RL
        #             ffReDC.append(2)
        #         elif pcvelocity[0]==0 and pcvelocity[1]==0 and pcvelocity[2]>50: #FH
        #             ffReDC.append(3)
        #else:
        #    print("Error: Las imágenes no son de equipos Philips, ni GE, ni Siemens.")
        #    sys.exit(0)
        return ffReDC
