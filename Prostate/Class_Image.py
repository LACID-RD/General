#from gdcm.gdcmswig import Object
import pydicom
import tkinter as tk
from tkinter import filedialog
import numpy as np
import operator 
from collections import Counter
import gdcm
import sys


class CImage():

    ########################################
    # Define variables de la clase
    ########################################

    def __init__(self, path_name): #pat_name=None,type=0,time=0,slice=0,img=None,te=0,tr=0,
        self.path_name = path_name
        # self.type = type
        # self.time = time
        
    ########################################
    # Descomprime y reescribe imágenes
    ########################################

    def DescomDicom(self):
        reader=gdcm.ImageReader()
        reader.SetFileName(self.path_name)
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
        writer.SetFileName(self.path_name)
        writer.SetFile(reader.GetFile())
        writer.SetImage(change.GetOutput())
        if not writer.Write():
            print("Error: No se escriben correctamente las imágenes.")
            sys.exit(0)

    ########################################
    # Guarda variables DICOM
    ########################################

    def ReaderDicom(self):  #Reads DiCOM files specific  information 
        DcmAux=pydicom.dcmread(self.path_name)
        ########################################### Media Storage [0] FILE-META !!
        if DcmAux.file_meta.MediaStorageSOPClassUID == '1.2.840.10008.5.1.4.1.1.4':
            self.capture_type = 0 #En este caso es imagen normal (no captura secundaria)
        elif DcmAux.file_meta.MediaStorageSOPClassUID == '1.2.840.10008.5.1.4.1.1.4.1':
            self.capture_type = 1 #En este caso es es Enhanced MR Image Storage (con contraste) http://dicom.nema.org/dicom/2013/output/chtml/part04/sect_I.4.html
        elif DcmAux.file_meta.MediaStorageSOPClassUID == '1.2.840.10008.5.1.4.1.1.7':
            self.capture_type = 2 #En este caso es captura secundaria
        else:
            print("Error al leer el tipo de imagen - media storage (captura secundaria vs imagen normal) del file meta")
            sys.exit(0)
        ########################################### Transfer Syntax [1] FILE-META !!
        if DcmAux.file_meta.TransferSyntaxUID == '1.2.840.10008.1.2.4.70':
            self.tr_syn = 0 #JPEG Lossless, Non-Hierarchical, First-Order Prediction MIRAR http://dicom.nema.org/medical/dicom/current/output/chtml/part18/sect_8.7.3.html
        elif DcmAux.file_meta.TransferSyntaxUID == '1.2.840.10008.1.2':
            self.tr_syn = 1 #Implicit VR Little Endian MIRAR http://dicom.nema.org/medical/dicom/current/output/chtml/part18/sect_8.7.3.html
        elif DcmAux.file_meta.TransferSyntaxUID == '1.2.840.10008.1.2.4.90':
            self.tr_syn = 2 #JPEG 2000 Image Compression (Lossless Only) MIRAR http://dicom.nema.org/medical/dicom/current/output/chtml/part18/sect_8.7.3.html
        else: #Agregar BIOBOX
            print("Error al leer el transfer syntax (captura secundaria vs imagen normal) del file meta")
            sys.exit(1)
        ########################################### Source Application Entity Title [2] (workstation o equipo del que salió la imagen) FILE-META !!
        self.bla = DcmAux.file_meta[0x0002,0x0016].value
        ########################################### Modalidad [3]
        self.modality = DcmAux[0x0008,0x0060].value # 3:Modalidad
        if "MR" not in self.modality:
            if "CT" not in self.modality:
                print("Error: Las imágenes no son de MR ni de CT.")
                sys.exit(0)
        ########################################### Fabricante [4]
        # obj = Image(DcmAux[0x0008,0x0070].value)
        self.mnfcr = DcmAux[0x0008,0x0070].value
        ########################################### TR [5]
        self.tr = DcmAux[0x0018,0x0080].value
        ########################################### TE [6]
        self.te = DcmAux[0x0018,0x0081].value
        ########################################### Tipo de Sec [7]
        self.seq_type = DcmAux[0x0018,0x0020].value
        ########################################### Grosor de slice [8]
        self.sl_thick = DcmAux[0x0018,0x0050].value
        ########################################### Campo externo [9]
        self.ext_field = DcmAux[0x0018,0x0087].value
        ########################################### Codi. de fase [10]
        self.phase_cod = DcmAux[0x0018,0x1312].value
        ########################################### Acquisition Number [11]
        self.acq_number = DcmAux[0x0020,0x0012].value   
        ########################################### Img in Acquisition [12]
        #self.im_number = DcmAux[0x0020,0x1002].value
        ########################################### Stack ID [12]
        #self.stack_id = DcmAux[0x0020,0x9056].value                
        ########################################### In-Stack Position Number [12]
        #ffReDC.append(DcmAux[0x0020,0x9057].value  
        ########################################### Num de filas [12]
        self.n_of_rows = DcmAux[0x0028,0x0010].value
        ########################################### Num de colum [13]
        self.n_of_cols = DcmAux[0x0028,0x0011].value
        ########################################### Num de slice [14]
        self.slice = DcmAux[0x2001,0x100a].value

    ########################################
    # Ordena DICOM en lista
    ########################################

    def SortDicom(self):
        Dcm_list=[]
        Dcm_list.append(self.tr)
        Dcm_list.append(self.te)
        Dcm_list.append(self.slice)
        return Dcm_list