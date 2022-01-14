from PIL import Image
import numpy as np
import pydicom
import sys
import tkinter as tk
from tkinter import filedialog


def main():
    #Abre cuadro de diálogo
    root = tk.Tk()
    root.withdraw()
    file1 = filedialog.askopenfilenames(filetypes= [('image','png')],title="Seleccionar imágenes png a convertir") #tuple
    #Error por si el archivo está vacío
    conerr=0
    EmptyString=''
    if file1 is EmptyString:
        print("Error",conerr,": No seleccionó archivo.")
        sys.exit(0)
    conerr+=1


    path_dcm_ref = input("Ingrese el path del archivo (con nombre incluido) de la imagen dicom que quiere utilizar como referencia: ")
    dcm = pydicom.dcmread(path_dcm_ref) #imagen dicom que tiene los datos de referencia del paciente, fecha, etc.
    path_carpeta_final = input("Ingrese el path del directorio final donde se guardarán las imágenes convertidas: ")
    dcm_tg_ref_path = input("Ingrese el path completo (nombre de archivo incluido) del dicom de tractografía de referencia: ")
    dcm_tg_ref = pydicom.dcmread(dcm_tg_ref_path)
    var_opcion = input("Ingrese: 1 si es tractografía axial, 2 si es tractografía coronal, 3 si es tractografía sagital, 4 para tracto axial especial: ")
    #Loop que lee y analiza las imágenes
    i=0
    for k in file1:
        i=i+1
        im_frame_png = Image.open(k)
        path_esp = f"/img_{i}.dcm" #última parte del path con que se van a guardar las imágenes dicom finales
        path_final_esp = path_carpeta_final + path_esp #path completo con que se va a guardar cada imagen dicom final
        
        np_frame = np.array(im_frame_png.getdata(),dtype=np.uint8)
        dcm.Rows = im_frame_png.height
        dcm.Columns = im_frame_png.width
        dcm.PhotometricInterpretation = "RGB"
        dcm.SamplesPerPixel = 3
        dcm.BitsStored = 8
        dcm.BitsAllocated = 8
        dcm.HighBit = 7
        dcm.PixelRepresentation = 0
        dcm.PixelData = np_frame.tobytes()
        #---------------------Etiquetas file-meta--------------------------------
        dcm.file_meta[0x0002,0x0000].value = dcm_tg_ref.file_meta[0x0002,0x0000].value
        dcm.file_meta[0x0002,0x0001].value = dcm_tg_ref.file_meta[0x0002,0x0001].value
        dcm.file_meta.MediaStorageSOPClassUID = dcm_tg_ref.file_meta.MediaStorageSOPClassUID #Esta es la 0x0002,0x0002
        dcm.file_meta[0x0002,0x0003].value = dcm_tg_ref.file_meta[0x0002,0x0003].value
        dcm.file_meta.TransferSyntaxUID = dcm_tg_ref.file_meta.TransferSyntaxUID #Esta es la 0x0002,0x0013
        dcm.file_meta[0x0002,0x0012].value = dcm_tg_ref.file_meta[0x0002,0x0012].value
        dcm.file_meta[0x0002,0x0013].value = dcm_tg_ref.file_meta[0x0002,0x0013].value
        dcm.file_meta[0x0002,0x0016].value = dcm_tg_ref.file_meta[0x0002,0x0016].value
        #---------------------Etiquetas estándar---------------------------------
        dcm.ImageType = dcm_tg_ref.ImageType #Esta es la 0x0008,0x0008
        dcm.SOPClassUID = dcm_tg_ref.SOPClassUID #Esta es la 0x0008,0x0016
        dcm.SeriesDescription = 'TRACTOGRAFIA'
        if var_opcion=='1':
            dcm.SeriesDescription = 'AX TG' #0x0008,0x103E
        elif var_opcion=='2':
            dcm.SeriesDescription = 'COR TG' #0x0008,0x103E
        elif var_opcion=='3':
            dcm.SeriesDescription = 'SAG TG' #0x0008,0x103E
        elif var_opcion=='4':
            dcm.SeriesDescription = 'AX TG ESP' #0x0008,0x103E
        else:
            print("ERROR: Ingresó mal el número de opción.")
        dcm.ScanningSequence = dcm_tg_ref.ScanningSequence #0x0018,0x0020
        dcm.SequenceVariant = dcm_tg_ref.SequenceVariant #0x0018,0x0021
        dcm.ScanOptions = dcm_tg_ref.ScanOptions #0x0018,0x0022
        dcm.MRAcquisitionType = dcm_tg_ref.MRAcquisitionType #0x0018,0x0023
        #dcm.add_new(0x00180024, 'SH', '')
        if var_opcion=='1':
            dcm.add_new(0x00181030, 'LO', 'AX TG')
        elif var_opcion=='2':
            dcm.add_new(0x00181030, 'LO', 'COR TG')
        elif var_opcion=='3':
            dcm.add_new(0x00181030, 'LO', 'SAG TG')
        elif var_opcion=='4':
            dcm.add_new(0x00181030, 'LO', 'AX TG ESP')
        dcm.save_as(path_final_esp)
        print(path_final_esp)
        
        

#Ejecuta función main() 
if __name__ == '__main__':
    main()