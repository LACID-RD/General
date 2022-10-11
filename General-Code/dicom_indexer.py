import os
import pydicom as dicom
import sys

def indexer():
    nameList = []
    pathList = []
    dirList = []
    path = os.path.abspath('') 
    for root,dirs,files in os.walk(path):
        for file in files:
            if file.endswith(".dcm"):
                
                filePath = os.path.join(root, file)
                pathList.append(filePath)
                
                ds = dicom.dcmread(filePath)
                
                name = ds.SeriesDescription
                nameList.append(name)
                print(name)
                directory = os.path.dirname(filePath)
                dirList.append(directory)
                
                for dire in dirList:
                    dir0 = dire.split("/")
                    dir0.pop()
                    dir0.append(name)
                    newPath = "/".join(dir0)
                    os.rename(directory,newPath)
    print(name)            
    print(newPath)

indexer()
