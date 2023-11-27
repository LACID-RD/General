# from ntpath import join
# from operator import ne
# import shelve
# import pydicom
# from collections import Counter
# import gdcm
# import os
# import pandas as pd
# import math
# from scipy import ndimage,misc,signal
# from itertools import repeat
# from scipy.stats.stats import pearsonr
# import cv2
# from Class_Image import CImage
# from Class_DcmRd import CDcmRd
# from Class_Proc import PProc
# from math import comb
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import sys

### Local libraries
from Class_Image import CImage

#############################
#############################
# CLASS CSerie 03-
#############################
#############################


class CSerie:
    Instanc = []

    ###############
    # 01-Inicializa Clase
    ###############

    def __init__(self, SeriNum, StuItem, SerItem, resolution):
        CSerie.Instanc.append(self)
        self.InsIndx = int(len(CSerie.Instanc) - 1)
        self.StuItem = StuItem  # Estudio al q pertenece la serie
        self.SerItem = SerItem  # Item de la serie
        self.S02SeNu = SeriNum
        self.pathFol = 0
        self.refImag = -4
        self.AllImag = []  # Contiene objetos de las imagenes
        self.Image3D = []  # Recontruccion 3D
        self.trns_mat = []
        # Meta, modalidad y study
        self.S00CpTp = -2
        self.S00TfSy = -2
        self.S00Sour = -2
        self.S01Mdly = -2
        self.S03AcNb = -2
        # Geometry
        self.S04SlTk = -2
        self.S04RwNb = -2
        self.S04ClNb = -2
        self.S04DiCo = -2
        self.S04PiSp = -2
        # MR
        self.S10ExFd = -2
        self.S10SqTp = -2
        self.S10AdTy = -2
        self.S11TsTr = -2
        self.S11TsTe = -2
        self.S11TsTi = -2
        self.S11FlAn = -2
        self.S12ETLg = -2
        self.S12PhCd = -2
        self.S12AcPl = -2
        self.S11MRCo = -2
        self.SLa11MR = -2
        self.SLa12Ac = -2
        self.resolution = resolution

    ###############
    # 02-Copia características desde una imagen
    ###############
    # RefImag: Imagen de referencia para definir caracteristicas de la serie
    # ImgType: 0 si es adquirida, 1 si es resultado de un posprocesamiento

    def CSRCopFea(self, RefImag, img_type):
        self.refImag = RefImag

        if img_type == 0:
            self.pathFol = Path(self.refImag.PathImg).parent
            # Meta, modalidad y study
            self.S00CpTp = self.refImag.D00CpTp
            self.S00TfSy = self.refImag.D00TfSy
            self.S00Sour = self.refImag.D00Sour
            self.S03AcNb = self.refImag.D03AcNb
            # MR
            self.S10SqTp = self.refImag.D10SqTp
            self.S10AdTy = self.refImag.D10AdTy
            self.S11TsTr = self.refImag.D11TsTr
            self.S11TsTe = self.refImag.D11TsTe
            self.S11TsTi = self.refImag.D11TsTi
            self.S11FlAn = self.refImag.D11FlAn
            self.S12ETLg = self.refImag.D12ETLg
            self.S12PhCd = self.refImag.D12PhCd
        # Modality
        self.S01Mdly = self.refImag.D01Mdly
        # Geometry
        self.S04SlTk = self.refImag.D04SlTk
        self.S04RwNb = self.refImag.D04RwNb
        self.S04ClNb = self.refImag.D04ClNb
        self.S04PiSp = self.refImag.D04PiSp
        self.S04DiCo = self.refImag.D04DiCo
        # MR
        self.S10ExFd = self.refImag.D10ExFd
        self.S12AcPl = self.refImag.D12AcPl

        # Transformation matix
        vec_rwo = np.array(self.S04DiCo[0:3])  # X
        vec_clo = np.array(self.S04DiCo[3:6])  # Y
        vec_nor = np.cross(vec_rwo, vec_clo)
        var_qa = (
            np.sum(np.square(vec_rwo))
            * np.sum(np.square(vec_clo))
            * np.sum(np.square(vec_nor))
        )
        if var_qa < 0.999 or var_qa > 1.001:
            raise ValueError("Error: Problemas con los cosenos directores (CSRCop).")
        self.trns_mat = [
            [
                vec_rwo[0] * self.S04PiSp[0],
                vec_clo[0] * self.S04PiSp[1],
                vec_nor[0] * self.S04SlTk,
            ],
            [
                vec_rwo[1] * self.S04PiSp[0],
                vec_clo[1] * self.S04PiSp[1],
                vec_nor[1] * self.S04SlTk,
            ],
            [
                vec_rwo[2] * self.S04PiSp[0],
                vec_clo[2] * self.S04PiSp[1],
                vec_nor[2] * self.S04SlTk,
            ],
            [0, 0, 0],
        ]
        self.CSSlicPln(img_type)  # Determina plano de corte
        return None

    ###############
    # 03-Determina plano de corte
    ###############

    def CSSlicPln(self, img_type):
        var_aux_AcP = []
        var_aux_Pla = -4

        # Por cosenos directores
        var_aux_AcP.append(abs(self.S04DiCo[0] * self.S04DiCo[4]))
        var_aux_AcP.append(abs(self.S04DiCo[1] * self.S04DiCo[5]))
        var_aux_AcP.append(abs(self.S04DiCo[0] * self.S04DiCo[5]))
        if var_aux_AcP[0] == max(var_aux_AcP):
            self.SLa12Ac = "Ax-"
            var_aux_Pla = 0
        elif var_aux_AcP[1] == max(var_aux_AcP):
            self.SLa12Ac = "Sag-"
            var_aux_Pla = 1
        elif var_aux_AcP[2] == max(var_aux_AcP):
            self.SLa12Ac = "Cor-"
            var_aux_Pla = 2
        else:
            self.SLa12Ac = "Ind-"

        # Por Acquisition plane
        if self.S12AcPl == 0:
            self.SLa12Ac += "Ax"
        elif self.S12AcPl == 1:
            self.SLa12Ac += "Sag"
        elif self.S12AcPl == 2:
            self.SLa12Ac += "Cor"
        elif self.S12AcPl == -4:
            self.SLa12Ac += "Ind"
        else:
            raise ValueError(
                "Error: No se determina variable DCM Acquisition plane (CSSlic)."
            )

        # Analiza si los dos anteriores son iguales
        if var_aux_Pla == self.S12AcPl:
            if self.S12AcPl == 0:
                self.SLa12Ac = "Ax"
            elif self.S12AcPl == 1:
                self.SLa12Ac = "Sag"
            elif self.S12AcPl == 2:
                self.SLa12Ac = "Cor"
            elif self.S12AcPl == -4:
                raise ValueError("Error: No se determina plano de corte (CSSlic).")
            else:
                print("Error en el plano de corte (CSSlic).")
        else:
            print("Warning: No coinciden planos de corte (CSSlic).")

        # Determina contraste
        if img_type == 0:
            self.CSRCopCon(self.refImag.D11MRCo)
        else:
            self.S11MRCo = 67
            self.SLa11MR = "Post_Proc"
        return None

    ###############
    # 04-Ordena las imagenes por posicion y
    #    carga en matrices las imagenes
    ###############

    def CS_img_order(self):
        self.AllImag.sort(key=lambda x: x.D04Slic)
        self.CSMatImag(0)
        return None

    ###############
    # 05-Copia caracteristicas de contraste
    ###############

    def CSRCopCon(self, var_aux0):
        if self.S11MRCo < 0:
            self.S11MRCo = var_aux0
        # Contraste
        if self.S11MRCo == 10:
            self.SLa11MR = "GRE-T1"
        elif self.S11MRCo == 15:
            self.SLa11MR = "wT1"
        elif self.S11MRCo == 20:
            self.SLa11MR = "wT2"
        elif self.S11MRCo == 21:
            self.SLa11MR = "DWI"
        elif self.S11MRCo == 25:
            self.SLa11MR = "GRE-T2"
        elif self.S11MRCo == 26:
            self.SLa11MR = "fMRI"
        elif self.S11MRCo == 30:
            self.SLa11MR = "IR o STIR"
        elif self.S11MRCo == 31:
            self.SLa11MR = "T2-FLAIR"
        elif self.S11MRCo == 32:
            self.SLa11MR = "T1-FLAIR"
        elif self.S11MRCo == 110:
            self.SLa11MR = "PC-Mag"
        elif self.S11MRCo == 111:
            self.SLa11MR = "PC_PhM"
        elif self.S11MRCo == 112:
            self.SLa11MR = "PC_PhX"
        elif self.S11MRCo == 113:
            self.SLa11MR = "PC_PhY"
        elif self.S11MRCo == 114:
            self.SLa11MR = "PC-PhZ"
        elif self.S11MRCo == 66:
            self.SLa11MR = "Not found"
        elif self.S11MRCo == 67:
            self.SLa11MR = "Post_Proc"
        elif self.S11MRCo == -4:
            self.SLa11MR = "Sec. capture"
        else:
            raise ValueError("Error: No se determina contraste de la serie.")
        return None

    #########################
    # Cambian info ya existente
    #########################
    # 06-Carga y normaliza en matrices las imagenes
    #    de una serie. Las deja en FORMATO FLOAT
    ###############
    # 0: Carga y normaliza
    # 1: Solo normaliza

    def CSMatImag(self, optAuxi):
        lowValu = np.inf
        maxValu = np.NINF

        if optAuxi == 0:
            for i in self.AllImag:
                i.CIDescDCM(i.PathImg)  # Decompress Image
                i.ImgData = i.DcmImag.pixel_array.astype(float)
                i.DcmImag = -2  # Delete header to save memory

        # Normalize the images in a serie
        lowValu = np.min([np.min(i.ImgData) for i in self.AllImag])
        maxValu = np.max([np.max(i.ImgData) for i in self.AllImag])
        if maxValu > lowValu:
            var_aux3 = self.resolution / (maxValu - lowValu)
            for i in self.AllImag:
                i.ImgData = ((i.ImgData - lowValu) * var_aux3).astype(float)
        elif maxValu == lowValu:
            for i in self.AllImag:
                i.ImgData = i.ImgData.astype(float)
        else:
            raise ValueError("Error: No se normalizan las imagenes (CS_mat).")
        return None

    ###############
    # 07-Tranformada exponencial o logaritmica
    ###############

    def CSImgTrns(self, Bin, Trf, CoA):
        var_aux1 = 0
        for i in range(len(self.AllImag)):
            if Trf == 0:
                pass
            elif Trf == 1:  # y=Ae(Bx)
                CoB = np.log(Bin / CoA) / Bin
                var_aux2 = CoA * np.exp(CoB * self.AllImag[i].ImgData)
            elif Trf == 2:  # y=Alog(Bx+1)
                CoB = (np.exp(0.005 * Bin / CoA) - 1) / Bin
                var_aux2 = 200 * CoA * np.log(CoB * self.AllImag[i].ImgData + 1)
            else:
                raise ValueError("Error: No se realiza transformada (CSImgT).")
            self.AllImag[var_aux1].ImgData = var_aux2
            var_aux1 += 1
        return None

    ###############
    # Elimina las imagenes de la serie
    ###############
    # EntType: 0 borra todas, 1 es un array

    def CSRmImage(self, EntType):
        varRefr = []
        if EntType == 0:
            self.AllImag = []
            for i in CImage.Instanc:
                if i.StuItem == self.StuItem and i.SerItem == self.SerItem:
                    varRefr.append(i)
        elif EntType == 1:
            for i in CImage.Instanc:
                if (
                    i.StuItem == self.StuItem
                    and i.SerItem == self.SerItem
                    and i.ImgItem in EntType
                ):
                    varRefr.append(i)
                    print("PENDIENTE POR VERIFICAR")
        else:
            raise ValueError("Error: No se eliminan imagenes (CSRmIm).")
        for i in varRefr:
            CImage.Instanc.remove(i)
        return None

    ########################################
    ########################################
    # Recontruccion en 3D MultiPlanar Reconsturction
    ########################################
    ########################################
    # https://stackoverflow.com/questions/57497695/2d-x-ray-reconstruction-from-3d-dicom-images
    # DireCos: Coseno director de la reconstrucción. Si es 0, se
    # realiza reconstruccion ortogonal en un plano y 1 en otro plano

    def CS3DRecon(self, DireCos):
        # Se crea array-3D de ceros
        vaShape = list(self.AllImag[0].ImgData.shape)
        vaShape.append(len(self.AllImag))
        self.Image3D = np.zeros(vaShape)

        # Llena Image3D con las imagenes
        for i in range(len(self.AllImag)):
            self.Image3D[:, :, i] = self.AllImag[i].ImgData
        print("3D:", self.S04RwNb, self.S04ClNb, vaShape)

        # plot 3 orthogonal slices
        ss = self.S04SlTk
        ps = self.S04PiSp
        ax_aspect = ps[1] / ps[0]
        sag_aspect = ps[1] / ss
        cor_aspect = ss / ps[0]
        a1 = plt.subplot(111)
        plt.imshow(self.Image3D[:, :, vaShape[2] // 2], cmap=plt.cm.bone)
        a1.set_aspect(ax_aspect)
        plt.title("Org")
        plt.show()
        a2 = plt.subplot(111)
        plt.imshow(self.Image3D[:, vaShape[1] // 2, :], cmap=plt.cm.bone)
        a2.set_aspect(sag_aspect)
        plt.title("MPR")
        plt.show()
        a3 = plt.subplot(111)
        plt.imshow(self.Image3D[vaShape[0] // 2, :, :].T, cmap=plt.cm.bone)
        a3.set_aspect(cor_aspect)
        plt.title("MPR")
        plt.show()
        # FALTA TERMINAR !!!!!!!
        return None

    #########################
    # Otros
    #########################
    # Imprime info del estudio
    ###############

    def CSPrtInfo(self):
        print(
            "Ser:",
            self.S02SeNu,
            ",Imgs:",
            len(self.AllImag),
            ",Sec:",
            self.S10SqTp,
            ",Type:",
            self.S10AdTy,
            self.S04RwNb,
            "x",
            self.S04ClNb,
            self.SLa11MR,
            self.SLa12Ac,
        )
        if self.S11TsTi < 0:
            print("    TR:", self.S11TsTr, ",TE:", self.S11TsTe)
        else:
            print("    TR:", self.S11TsTr, ",TE:", self.S11TsTe, ",TI:", self.S11TsTi)
        return None

    ###############
    # Une o concatena todas las imagenes de una serie
    ###############
    # Se utiliza e.g. histogramas

    def CSUneSres(self):
        var_aux0 = len(self.AllImag) - 1
        vaArray = self.AllImag[0].ImgData
        for i in range(var_aux0):
            vaArray = np.concatenate((vaArray, self.AllImag[i + 1].ImgData), axis=0)
        return vaArray
