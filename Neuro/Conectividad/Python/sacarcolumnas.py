import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import filedialog

def main():
    #Ingrese numero de sujeto
    num_paciente = input("Ingrese el numero de sujeto")
    #Abre cuadro de diálogo y toma el path del archivo conn_csv que tiene las 3 columnas de más
    cuadro = tk.Tk()
    cuadro.withdraw()
    FilePath_conncsv = filedialog.askopenfilename() #Elegir la matriz conn crudo
    #Lee la matriz conn csv cruda
    df_conncsv = pd.read_csv(FilePath_conncsv, header=None)
    conncsv = df_conncsv.to_numpy()

    print(conncsv.shape)
    
    conn_cuadrada = np.zeros((120,120))

    for i in range(120):
        for j in range(120):
            conn_cuadrada[i,j] = conncsv[i,j]

    print(conn_cuadrada.shape)

    Conn_cuadrada_df = pd.DataFrame(conn_cuadrada)
    Conn_cuadrada_df.to_csv(f"{num_paciente}/{num_paciente}_conn_cuadrada.csv")
    

if __name__ == '__main__':
    main()