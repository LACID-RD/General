# from ntpath import join
# from operator import ne
# import shelve
# import tkinter as tk
# from tkinter import filedialog
# from collections import Counter
# import os
# import pandas as pd
# import matplotlib.pyplot as plt
# from Class_Image import CImage
# from Class_Proc import PProc
# import math
# from scipy import ndimage,misc,signal
# from itertools import repeat
# from scipy.stats.stats import pearsonr
# import cv2
# from math import comb
import gdcm
import numpy as np
import pydicom
import sys

# Local libraries
import Funcn_Proce

# from Class_DcmRd_MR import CDMGenMRI
# from Class_DcmRd_CT import CDMGeneCT


#############################
#############################
# CLASE CDcmRd 05-
#############################
#############################


class CDcmRd:
    ###############
    # 01-Define variables de la clase
    ###############
    ##### Metadata: 00
    # 00CpTp: Media Storage
    # 00TfSy: JPEG Lossless, Non-Hierarchical, First-Order Prediction
    # 00Sour: Source Application Entity Title
    ##### Study: 01
    # 01Name: Name
    # 01StTm: Study Time
    # 01StDc: Study description
    # 01Mnfr: Fabricante
    # 01MnMd: Modelo
    # 01Mdly: Modalidad
    ##### Serie: 02
    # 02SeNu: Series number
    ##### Image: 03
    # 03AcNb: Acquisition number
    ##### Geometry: 04
    # 04Slic: Slice: location/number
    # 04SlTk: Slice thickness
    # 04RwNb: Rows number
    # 04ClNb: Columns number
    # 04ImPo: Image position
    # 04DiCo: Director cosines
    # 04PiSp: Pixel spacing
    # 04stid: Stack ID
    # 04stpo: InStack position
    # 04wict: Window Center
    # 04wiwd: Window Width
    ##### Pending
    # (0008, 0021) Series Date

    def __init__(
        self, PathImg
    ):  # pat_name=None,type=0,time=0,slice=0,img=None,te=0,tr=0,
        self.PathImg = PathImg
        self.DcmImag = -2

        # Metadata y numero
        self.D00CpTp = -2
        self.D00TfSy = -2
        self.D00Sour = -2
        self.D00ReNu = -2
        # Data: paciente, fabricante, escaner
        self.D01Name = -2
        self.D01StTm = -2
        self.D01StDc = -2
        self.D01Mnfr = -2
        self.D01MnMd = -2
        self.D01Mdly = -2
        # Serie y adquisicion
        self.D02SeNu = -2
        self.D03AcNb = -2
        # Geometria y contraste
        self.D04Slic = -2
        self.D04SlTk = -2
        self.D04RwNb = -2
        self.D04ClNb = -2
        self.D04ImPo = -2
        self.D04DiCo = -2
        self.D04PiSp = -2
        self.D04stid = -2
        self.D04stpo = -2
        self.D04wict = -2
        self.D04wiwd = -2
        # MR
        self.D10ExFd = -2
        self.D10SqTp = -2
        self.D10AdTy = -2
        self.D11TsTr = -2
        self.D11TsTe = -2
        self.D11TsTi = -2
        self.D11FlAn = -2
        self.D11MRCo = -2
        self.D12ETLg = -2
        self.D12PhCd = -2
        self.D12AcPl = -2
        self.D12TrTm = -2
        self.D15bVal = -2

    from Class_DcmRd_MR import CDMGenMRI
    from Class_DcmRd_MR import CDMContMR
    from Class_DcmRd_MR import CDMMRwDWI
    from Class_DcmRd_MR import CDMMRPhCo
    from Class_DcmRd_CT import CDMGeneCT

    ###############
    # 02-Read DICOM Features: llama a CDMDcmGeom
    ###############
    # Por simplicidad esta separada de la
    # geometria, proxima funcion

    def CDMDcmFeat(self):
        log_str = "0502"
        self.DcmImag = pydicom.dcmread(self.PathImg)
        # print("DICOM:",self.DcmImag)

        # Media Storage FILE-META !!
        # http://dicom.nema.org/dicom/2013/output/chtml/part04/sect_I.4.html
        if (
            self.DcmImag.file_meta.MediaStorageSOPClassUID
            == "1.2.840.10008.5.1.4.1.1.4"
        ):
            self.D00CpTp = 0  # Normal
        elif (
            self.DcmImag.file_meta.MediaStorageSOPClassUID
            == "1.2.840.10008.5.1.4.1.1.4.1"
        ):
            self.D00CpTp = 1  # Enhanced MR Image Storage
        elif (
            self.DcmImag.file_meta.MediaStorageSOPClassUID
            == "1.2.840.10008.5.1.4.1.1.7"
        ):
            self.D00CpTp = 2  # Captura secundaria
            self.D11MRCo = -4  # Llena la casilla contraste
        else:
            label_log = log_str + "01 Error: Media Storage"
            Funcn_Proce.FP_error_log(0, label_log)

        # Transfer syntax FILE-META
        if self.DcmImag.file_meta.TransferSyntaxUID == "1.2.840.10008.1.2.4.70":
            self.D00TfSy = 0  # JPEG Lossless, Non-Hierarchical, First-Order Prediction http://dicom.nema.org/medical/dicom/current/output/chtml/part18/sect_8.7.3.html
        elif self.DcmImag.file_meta.TransferSyntaxUID == "1.2.840.10008.1.2":
            self.D00TfSy = 1  # Implicit VR Little Endian http://dicom.nema.org/medical/dicom/current/output/chtml/part18/sect_8.7.3.html
        elif self.DcmImag.file_meta.TransferSyntaxUID == "1.2.840.10008.1.2.4.90":
            self.D00TfSy = 2  # JPEG 2000 Image Compression (Lossless Only) http://dicom.nema.org/medical/dicom/current/output/chtml/part18/sect_8.7.3.html
        else:  # Agregar BIOBOX
            label_log = log_str + "02 Error: Transfer syntax"
            Funcn_Proce.FP_error_log(0, label_log)

        # Source application entity title (workstation o equipo del que salió la imagen) FILE-META !!
        try:
            self.D00Sour = self.DcmImag.file_meta[0x0002, 0x0016].value
        except:
            label_log = log_str + "03 Warning: Source entity title"
            Funcn_Proce.FP_error_log(1, label_log)

        # Name
        try:
            self.D01Name = self.DcmImag[0x0010, 0x0010].value
        except:
            self.D01Name = -4
            label_log = log_str + "04 Warning: Source entity title"
            Funcn_Proce.FP_error_log(1, label_log)

        # Study Time/Accession Number
        try:
            self.D01StTm = (
                self.DcmImag[0x0008, 0x0050].value or self.DcmImag[0x0008, 0x0020].value
            )
        except:
            self.D01StTm = -4
            label_log = log_str + "05 Warning: Study time/accesion number"
            Funcn_Proce.FP_error_log(1, label_log)

        # Study description
        try:
            self.D01StDc = self.DcmImag[0x0008, 0x1030].value
        except:
            self.D01StDc = -4
            label_log = log_str + "06 Warning: Study description"
            Funcn_Proce.FP_error_log(1, label_log)

        # Fabricante
        self.D01Mnfr = self.DcmImag[0x0008, 0x0070].value
        if (
            "GE" not in self.D01Mnfr
            and "Phil" not in self.D01Mnfr
            and "SIE" not in self.D01Mnfr
            and "TOS" not in self.D01Mnfr
        ):
            self.D01Mnfr = -4
            label_log = log_str + "07 Warning: Fabricante"
            Funcn_Proce.FP_error_log(1, label_log)

        # Modelo [6a]
        try:
            self.D01MnMd = self.DcmImag[0x0008, 0x1090].value
        except:
            self.D01MnMd = -4
            label_log = log_str + "08 Warning: Modelo"
            Funcn_Proce.FP_error_log(1, label_log)

        # Series Number
        try:
            self.D02SeNu = self.DcmImag[0x0020, 0x0011].value
        except:
            label_log = log_str + "09 Error Series Number"
            Funcn_Proce.FP_error_log(0, label_log)

        # Acquisition number
        try:
            self.D03AcNb = self.DcmImag[0x0020, 0x0012].value  # 3T
        except:
            self.D03AcNb = -4
            label_log = log_str + "10 Warning: Acquisition number"
            Funcn_Proce.FP_error_log(1, label_log)

        # Modalidad
        try:
            self.D01Mdly = self.DcmImag[0x0008, 0x0060].value
        except:
            label_log = log_str + "11 Error Series Number"
            Funcn_Proce.FP_error_log(0, label_log)

        # Llena geometría
        self.CDMDcmGeom()
        # Llama funciones específicas
        if "MR" in self.D01Mdly:
            self.CDMGenMRI()
        elif "CT" in self.D01Mdly:
            self.CDMGeneCT()
        else:
            label_log = log_str + "12 Error: Imagenes no son de MR/CT"
            Funcn_Proce.FP_error_log(0, label_log)

    ###############
    # 03-Read DICOM Geometry
    ###############

    def CDMDcmGeom(self):
        log_str = "0503"
        # Slice: number/location
        try:
            self.D04Slic = self.DcmImag[0x0020, 0x0050].value  # location
        except:
            try:
                self.D04Slic = self.DcmImag[0x0020, 0x1041].value  # location
            except:
                try:
                    self.D04Slic = self.DcmImag[0x2001, 0x100B].value  # number
                except:
                    self.D04Slic = -4
                label_log = log_str + "01 Warning: Slice"
                Funcn_Proce.FP_error_log(1, label_log)

        # Grosor de slice
        try:
            self.D04SlTk = self.DcmImag[0x0018, 0x0050].value
        except:
            label_log = log_str + "02 Error: Grosor de slice"
            Funcn_Proce.FP_error_log(0, label_log)

        # Num de filas
        try:
            self.D04RwNb = self.DcmImag[0x0028, 0x0010].value
        except:
            label_log = log_str + "03 Error: Numero de filas"
            Funcn_Proce.FP_error_log(0, label_log)

        # Num de colum
        try:
            self.D04ClNb = self.DcmImag[0x0028, 0x0011].value
        except:
            label_log = log_str + "04 Error: Numero de columnas"
            Funcn_Proce.FP_error_log(0, label_log)

        # Image position
        try:
            self.D04ImPo = np.array([float(x) for x in self.DcmImag[0x0020, 0x0032]])
        except:
            try:
                ffImPo2 = self.DcmImag[0x5200, 0x9230][0]
                ffImPo1 = ffImPo2[0x0020, 0x9113][0]
                self.D04ImPo = ffImPo1[0x0020, 0x0032].value
            except:
                label_log = log_str + "05 Error: Image position"
                Funcn_Proce.FP_error_log(0, label_log)

        # Director cosine
        try:
            self.D04DiCo = np.array([float(x) for x in self.DcmImag[0x0020, 0x0037]])
        except:
            try:
                ShFuGS = self.DcmImag[0x5200, 0x9229][0]
                ImgOri1 = ShFuGS[0x0020, 0x9116][0]
                self.D04DiCo = ImgOri1[0x0020, 0x0037].value
            except:
                label_log = log_str + "06 Error: Director cosines"
                Funcn_Proce.FP_error_log(0, label_log)

        # Pixel spacing
        try:
            self.D04PiSp = np.array([float(x) for x in self.DcmImag[0x0028, 0x0030]])
        except:
            try:
                PixSpa1 = ShFuGS[0x0028, 0x9110][0]
                self.D04PiSp = PixSpa1[0x0028, 0x0030].value
            except:
                self.D04PiSp = -4
                raise ValueError("Error al leer pixel spacing (CDMDcmGeo)")

        # StackID
        try:
            self.D04stid = self.DcmImag[0x0020, 0x9056].value
        except:
            self.D04stid = -4
            label_log = "Warning: No se lee StackID (CDMDcmGeo)"
        ###### InStack position number
        try:
            self.D04stpo = self.DcmImag[0x0020, 0x9057].value
        except:
            self.D04stpo = -4
            label_log = "Warning: No se lee InStack (CDMDcmGeo)"
        ###### Window Center
        try:
            self.D04wict = self.DcmImag[0x0028, 0x1050].value
        except:
            self.D04wict = -4
            label_log = "Warning: No se lee Window Center (CDMDcmGeo)"
        ###### Window Width
        try:
            self.D04wiwd = self.DcmImag[0x0028, 0x1051].value
        except:
            self.D04wiwd = -4
            label_log = "Warning: No se lee Windwo Width (CDMDcmGeo)"
