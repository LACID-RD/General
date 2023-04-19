import gdcm
import sys
import pydicom as dicom


class ObjetoDicom:
    
    
    def DescomDicom(self, PathD):
        reader = gdcm.ImageReader()
        reader.SetFileName(PathD)
        
        if not reader.Read():
            print("Error: No se leen correctamente las imágenes.")
            sys.exit(0)
        
        change = gdcm.ImageChangeTransferSyntax()
        change.SetTransferSyntax(gdcm.TransferSyntax(
            gdcm.TransferSyntax.ImplicitVRLittleEndian))
        change.SetInput(reader.GetImage())
        
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


    def ReaderDicom(self, PathD):  # Reads DiCOM files specific  information
        tagList = []
        DcmAux = dicom.dcmread(PathD)
        #Image Type
        tagList.append(DcmAux[0x0008, 0x0008].value)
        #
        tagList.append(DcmAux[0x7fe0, 0x0010].value)
        return tagList
