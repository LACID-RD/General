from email import header
import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import filedialog



def main():
    #Ingrese numero de sujeto
    num_paciente = input("Ingrese el numero de sujeto")
    orden_paciente = input("Ingrese el número de paciente: 0-100307 ... 29-130013")
    tipo_pac = input("Ingrese el tipo de sujeto: 0 si es HC, 1 si es epilepsia temporal, 2 si es epilepsia extratemporal")
    edad = input("Ingrese edad:")
    sexo = input("Ingrese el sexo: 0 para femenino, 1 para masculino")
    tipo_pac_int = int(tipo_pac)
    orden_paciente_int=int(orden_paciente)
    edad_int = int(edad)
    sexo_int=int(sexo)
    #Abre cuadro de diálogo y toma el path del archivo seleccionado de la matriz de conectividad estructural/funcional triangular superior convertida en lista (previamente se debe haber corrido el código denominado Connectivity_structural/functional_triangular_V2.py)
    cuadro = tk.Tk()
    cuadro.withdraw()
    FilePath_list_est = filedialog.askopenfilename() #Primero elegir la lista estructural
    FilePath_list_func = filedialog.askopenfilename() #Después elegir la lista funcional
    FilePath_aseg = filedialog.askopenfilename() #Elegir la tabla csv de aseg stats
    #Lee la lista de la matriz de conectividad estructural/funcional triangular superior
    df_list_est = pd.read_csv(FilePath_list_est)
    df_list_func = pd.read_csv(FilePath_list_func)
    df_aseg = pd.read_csv(FilePath_aseg, sep=',', usecols=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64])


    #Transforma los dataframes a numpy
    list_est_np = df_list_est.to_numpy()
    list_func_np = df_list_func.to_numpy()
    list_est_transp = list_est_np[:,[1]].T
    list_func_transp = list_func_np[:,[1]].T
    aseg_np = df_aseg.to_numpy()
    list_aseg = np.zeros((1,67))

    for i in range(63):
        list_aseg[0,i]=aseg_np[orden_paciente_int,i] #INDICE DE LA FILA SEGUN EL PACIENTE QUE SE DESEE ANEXAR A LA TABLA

    list_aseg[0,64]=tipo_pac_int #CAMBIAR EL PARAMETRO SEGUN SI ES HC (0), EPI TEMP (1), O EPI EXTRATEMP (2) 
    list_aseg[0,65]=edad_int
    list_aseg[0,66]=sexo_int

    result = np.hstack((list_est_transp, list_func_transp, list_aseg)) 

    

    print(result.shape)

    result_df = pd.DataFrame(result)
    result_df.to_csv(f"{num_paciente}/{num_paciente}_Tabla.csv")
    print(f"{num_paciente} FINALIZADO CON EXITO")
    

if __name__ == '__main__':
    main()