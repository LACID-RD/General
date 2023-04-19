## Departamento de Resonancia, FUESMEN ##
## Implementación: Rodrigo A.


import os
import pydicom as dicom
import gdcm
import sys
from class_dicom import *


def main():

    #GLOB VARS:
    counter = 0
    print('''Decompressor implementation, tested in CT and MRI images.
Decompressing DICOM files... \n''')

    path = os.path.abspath('') 
    for root,dirs,files in os.walk(path):
        for file in files:
            if file.endswith(".dcm"):
                counter +=1
                filePath = os.path.join(root, file)
                decomp = ObjetoDicom()
                decomp.DescomDicom(filePath)

    print("All files have been decompressed.")
    print("\n")
    print("Gracias vuelva pronto :)")


if __name__ == "__main__":
    main()
