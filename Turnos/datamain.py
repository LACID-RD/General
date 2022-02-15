import numpy as np
import pandas as pd

import os
from methods import *
def main():
    path = os.path.abspath('') 
    files = os.listdir(path)
    ausentAvg = []
    patientList = []
    for file in files:
        if file.endswith(".xls"):
            
            originalData = pd.read_excel(file)
            df = originalData
            fecha = str(file)
            fecha = fecha.split(".",1)
            fecha = str(fecha[0])
            print("\n")
            print(fecha)
            print("\n")

            df.drop_duplicates("N° Turno",inplace=True)
            
            index = df.index
            patientQuantity = len(index)
 
            #df["hour"] = df["Fecha Turno"].dt.hour
            #print(df["hour"])
            
            datetimes = pd.to_datetime(df["Fecha Turno"])
            df["Fecha Turnos"] = datetimes
            #print(df["Fecha Turnos"].dt.minute)
            
            df["Hour"] = df["Fecha Turnos"].dt.hour
            df["Minute"] = df["Fecha Turnos"].dt.minute
            
            i = 0
            usedCancelations = 0

            hourList = []
            minuteList = []
            for index, row in df.iterrows():
                
                hour, minute = row["Hour"], row["Minute"]        
                
                hourList.append(hour)
                minuteList.append(minute)

            matrix = np.stack([hourList,minuteList])
            matrix = np.rollaxis(matrix,-1)
            shape = np.shape(matrix)    
            tolerance = 5
            
            for m in range(shape[0] - 1):
                for n in range(1):
                    if matrix[m][n] == matrix[m+1][n]:
                        value = (matrix[m+1][n+1] - matrix[m][n+1])
                        if abs(int(value)) < tolerance:
                            usedCancelations +=1
            
            counts = df["N°"].value_counts()
            ausentPatients = counts[0]
            ausentism = int(ausentPatients - usedCancelations)/int(patientQuantity)
            ausentism = round(ausentism*100)

            studyCount = df["Estudio"].value_counts()

            ausentAvg.append(ausentPatients)
            patientList.append(patientQuantity)

            print("Conteo de Pacientes: " + str(patientQuantity))
            print("Pacientes Ausentes: " + str(ausentPatients))
            print("Porcentaje de Ausentismo: " + str(ausentism) + "%")
            
            #print("Conteo de Estudios: ")
            #print(studyCount)            

    print(len(patientList))
    print(len(ausentAvg))
    mean = np.average(ausentAvg,weights=patientList)
    print(round(mean))


    #return patientQuantity, ausentism      

            
main()
