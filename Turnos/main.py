import numpy as np
import pandas as pd
import os

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
            fecha = fecha.split(".",1)
            fecha = str(fecha[0])
            print("\n")
            print(fecha)
            print("\n")
            
            df.drop_duplicates(["N° Turno","Fecha Turno","Médico / Equipo"], inplace=True, keep="last")
            
            excel = df
            excel.to_excel("excel.xlsx")
            
            pacientNumberTotal = df.Estado.count()

            print("Cantidad de Pacientes " + str(pacientNumberTotal))

            df["Estado"] = df["Estado"].astype("str")
            count = df["Estado"].value_counts()
            
            print(count)
            print("\n")
            
            ausentism = round(((count[1] + count[2])/pacientNumberTotal)*100)           
            print(type(ausentism))
            print("Ausentismo todos los resonadores de FUESMEN: " + str(ausentism) + "%" + "\n")


            filteredDF = df[df.Estudio == "RMAC CARDIACA (INC CINE,VIAB Y CONT)                                                                "]
            realizedFilter = filteredDF[filteredDF.Estado == "REA"]
            cardioVals = realizedFilter[["Documento","Estudio","Fecha Turno","Arribo","Inicio Estudio","Fin Estudio"]]
            
            essenzaDf = df[df["Médico / Equipo"] == "RMAC ESSENZA 1.5 TESLA"]
            optimaDf = df[df["Médico / Equipo"] == "RMAC GE OPTIMA 450W 1.5 T 2SUB"]
            ingeniaDf = df[df["Médico / Equipo"] == "RMAC INGENIA PHILIPS 1.5 T"]

            #AUSENTISM EACH MR
            print("\n")
            essenzaCount = essenzaDf.Estado.value_counts()
            essenzaPatients = essenzaDf.Estado.count()

            print("Essenza Count")
            print(essenzaCount)

            ausentEssenza = round(((int(essenzaCount[1]) + int(essenzaCount[2]))/essenzaPatients)*100)

            print("Ausentismo Essenza: " + str(ausentEssenza) + "%")
            print("Cantidad de pacientes en equipo Essenza: " + str(essenzaPatients))            
            print("\n")
            
            optimaCount = optimaDf.Estado.value_counts()
            optimaPatients = optimaDf.Estado.count()

            print("Optima Count")
            print(optimaCount)

            ausentOptima = round(((optimaCount[1] + optimaCount[2])/optimaPatients)*100)

            print("Ausentismo Optima: " + str(ausentOptima) + "%")
            print("Cantidad de pacientes en equipo Optima: " + str(optimaPatients))
            print("\n")
            
            ingeniaCount = ingeniaDf.Estado.value_counts()
            ingeniaPatients = ingeniaDf.Estado.count()

            print("Ingenia Count")
            print(ingeniaCount)

            ausentIngenia = round(((ingeniaCount[1] + ingeniaCount[2])/ingeniaPatients)*100)

            print("Ausentismo Ingenia: " + str(ausentIngenia) + "%")
            print("Cantidad de pacientes en equipo Ingenia: " + str(ingeniaPatients))

            print("\n")

            ## TIME BRACKETS AUSENTISM ##

            ausDfEssenza = essenzaDf[essenzaDf.Estado == "AUS"]
            ausDfOptima = optimaDf[optimaDf.Estado == "AUS"]
            ausDfIngenia = ingeniaDf[ingeniaDf.Estado == "AUS"]
      
main()
