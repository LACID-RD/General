import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import filedialog


def main():
    
    cuadro = tk.Tk()
    cuadro.withdraw()
    FilePath_tabla = filedialog.askopenfilename() #Seleccionar tabla general
    

    Tabla_df = pd.read_csv(FilePath_tabla,usecols=range(1,8810))
    

    print(f"Shape tabla= {Tabla_df.shape}")
    #print(Tabla_df)
    

    Tabla_df.to_csv("TablaGeneralLimpia.csv",index=False)

    connectivity_data = pd.read_csv("TablaGeneralLimpia.csv",usecols=range(8806))
    connectivity_target = Tabla_df["8806"]

    connectivity_data.to_csv("Connectivity_data_nuevo.csv",index=False)
    connectivity_target.to_csv("Connectivity_target_nuevo.csv", index=False)
    

if __name__ == '__main__':
    main()