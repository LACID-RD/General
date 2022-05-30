import tkinter as tk
from tkinter import filedialog
from collections import Counter
import gdcm
import sys

def DescomDicom(self):
                #Abre cuadro de diálogo y pregunta path del folder
    cuadro=tk.Tk()
    cuadro.withdraw()
    FolPath=filedialog.askdirectory(title="DICOM Images")
        #Warning si no se abre algún folder
    StringVacio=""
    if FolPath is StringVacio:
        print("Error: No seleccionó directorio.")
        sys.exit(0)
        
    reader=gdcm.ImageReader()
    reader.SetFileName(self.FolPath)
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
    writer.SetFileName(self.FolPath)
    writer.SetFile(reader.GetFile())
    writer.SetImage(change.GetOutput())
    if not writer.Write():
        print("Error: No se escriben correctamente las imágenes.")
        sys.exit(0)

DescomDicom()