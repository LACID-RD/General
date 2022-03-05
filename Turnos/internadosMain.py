import pandas as pd
import numpy as np
import os


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

            df.drop_duplicates(["N° Turno","Fecha Turno","Médico / Equipo"], inplace=True, keep="last")
            pacientNumber = df.Estado.count()

            print("Cantidad de Pacientes " + str(pacientNumber))
            
            intDf = df[df["Tipo Turno"] == "INT"]
            count = intDf.Estado.value_counts()
            print(count)
            ausentism = round((count[1]+count[2])/count[0]*100)

            print("Ausentismo Internados: " + str(ausentism) + "%")



main()