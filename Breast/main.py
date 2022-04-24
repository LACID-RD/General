import numpy as np
import tkinter as tk
from tkinter import filedialog
import pydicom as dicom
from array_generator import array_generator
from myshow import *
from perfu_locator import perfu_locator
from data_trimmer import array_trimmer
import pandas as pd
import os


def main():

    dirPath = filedialog.askdirectory(title="Select the Patients root directory")
    patientPath = filedialog.askopenfile(title="Select the Patients excel")
    patientPath = patientPath.name
    df = pd.read_excel(patientPath)
    df = df.reset_index()
    infoDf = df[["Key","ID","BIRADS","LATERALIDAD","X1","Y1","X2","Y2"]]
    infoDf = infoDf.reset_index()
    
    for index,row in infoDf.iterrows():
        for dirp,dirs,files in os.walk(dirPath):
            roiDf = row[["X1","Y1","X2","Y2"]]
            roi = roiDf.values
            roiList = list(roi)
            patientCode = row["Key"]
            count = 0
            count += 1
            
            if patientCode in dirs:
                print("Patient " + patientCode)
                
            print(count)
    
    
    #print(infoDf.head)


if __name__ == "__main__":
    main()