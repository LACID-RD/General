import math
import pandas as pd
import numpy as np
import os
from matplotlib import pyplot as plt
pd.set_option("display.max_rows", None, "display.max_columns", None)



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
            fecha = fecha.split(".", 1)
            fecha = str(fecha[0])
            print("\n")
            print(fecha)
            print("\n")

            df.drop_duplicates("N° Turno", inplace=True)
            pacientNumber = df.Estado.count()

            print("Cantidad de Pacientes " + str(pacientNumber))
            
            filteredDFCardio = df[df.Estudio == "RMAC CARDIACA (INC CINE,VIAB Y CONT)                                                                "]
            
            index = list(filteredDFCardio.index)
            nextIndex = [i+1 for i in index]

            indexList = [*index,*nextIndex]
            indexList.sort()



            cardioTimeDf = df.filter(items = indexList, axis = 0)
            #print(cardioTimeDf)
            
            cardioTimeDf["Month"] = cardioTimeDf["Fecha Turno"].dt.month
            cardioTimeDf["Day"] = cardioTimeDf["Fecha Turno"].dt.day
            cardioTimeDf["Hour"] = cardioTimeDf["Fecha Turno"].dt.hour
            cardioTimeDf["Minute"] = cardioTimeDf["Fecha Turno"].dt.minute
            
            #print(cardioTimeDf[["Fecha Turno","Hour","Minute"]])
            
            monthList = cardioTimeDf["Month"].to_list()
            dayList = cardioTimeDf["Day"].to_list()
            hourList = cardioTimeDf["Hour"].to_list()
            minuteList = cardioTimeDf["Minute"].to_list()
            #print(hourList)
            #print("\n")
            #print(minuteList)


            cardioTimeDf.drop_duplicates("N° Turno", inplace=True)
            cardioTimeDf.to_excel("testa.xlsx")


main()