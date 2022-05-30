import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import filedialog


def main():
    
    cuadro = tk.Tk()
    cuadro.withdraw()
    FilePath_controles = filedialog.askopenfilenames() #Seleccionar tablas controles
    FilePath_pacientes = filedialog.askopenfilenames() #Seleccionar tablas pacientes
    
    df_00 = pd.read_csv(FilePath_pacientes[0])
    df_01 = pd.read_csv(FilePath_pacientes[1])
    df_02 = pd.read_csv(FilePath_pacientes[2])
    df_03 = pd.read_csv(FilePath_pacientes[3])
    df_04 = pd.read_csv(FilePath_pacientes[4])
    df_05 = pd.read_csv(FilePath_pacientes[5])
    df_06 = pd.read_csv(FilePath_pacientes[6])
    df_07 = pd.read_csv(FilePath_pacientes[7])
    df_08 = pd.read_csv(FilePath_pacientes[8])
    df_09 = pd.read_csv(FilePath_pacientes[9])
    df_10 = pd.read_csv(FilePath_pacientes[10])
    df_11 = pd.read_csv(FilePath_pacientes[11])
    df_12 = pd.read_csv(FilePath_pacientes[12])
    df_13 = pd.read_csv(FilePath_pacientes[13])
    df_14 = pd.read_csv(FilePath_pacientes[14])
    df_15 = pd.read_csv(FilePath_pacientes[15])
    df_16 = pd.read_csv(FilePath_pacientes[16])
    #El 17 no tenemos el foco
    df_18 = pd.read_csv(FilePath_pacientes[17])
    df_19 = pd.read_csv(FilePath_pacientes[18])
    df_20 = pd.read_csv(FilePath_pacientes[19])
    df_21 = pd.read_csv(FilePath_pacientes[20])
    df_22 = pd.read_csv(FilePath_pacientes[21])
    #El 23 no tenia T1, lo excluimos
    df_24 = pd.read_csv(FilePath_pacientes[22])
    df_25 = pd.read_csv(FilePath_pacientes[23])
    df_26 = pd.read_csv(FilePath_pacientes[24])
    df_27 = pd.read_csv(FilePath_pacientes[25])
    df_28 = pd.read_csv(FilePath_pacientes[26])
    df_29 = pd.read_csv(FilePath_pacientes[27])
    df_30 = pd.read_csv(FilePath_pacientes[28])
    df_31 = pd.read_csv(FilePath_pacientes[29])
    df_32 = pd.read_csv(FilePath_pacientes[30])
    df_33 = pd.read_csv(FilePath_pacientes[31])
    #El 34 y 35 no tenemos el foco
    df_36 = pd.read_csv(FilePath_pacientes[32])
    #El 37 no tenemos el foco
    df_38 = pd.read_csv(FilePath_pacientes[33])
    df_39 = pd.read_csv(FilePath_pacientes[34])
    #El 40 y 41 no tenemos el foco


    df_HC_00 = pd.read_csv(FilePath_controles[0])
    df_HC_01 = pd.read_csv(FilePath_controles[1])
    df_HC_02 = pd.read_csv(FilePath_controles[2])
    df_HC_03 = pd.read_csv(FilePath_controles[3])
    df_HC_04 = pd.read_csv(FilePath_controles[4])
    df_HC_05 = pd.read_csv(FilePath_controles[5])
    df_HC_06 = pd.read_csv(FilePath_controles[6])
    df_HC_07 = pd.read_csv(FilePath_controles[7])
    df_HC_08 = pd.read_csv(FilePath_controles[8])
    df_HC_09 = pd.read_csv(FilePath_controles[9])
    df_HC_10 = pd.read_csv(FilePath_controles[10])
    df_HC_11 = pd.read_csv(FilePath_controles[11])
    df_HC_12 = pd.read_csv(FilePath_controles[12])
    df_HC_13 = pd.read_csv(FilePath_controles[13])
    df_HC_14 = pd.read_csv(FilePath_controles[14])
    df_HC_15 = pd.read_csv(FilePath_controles[15])
    df_HC_16 = pd.read_csv(FilePath_controles[16])
    df_HC_17 = pd.read_csv(FilePath_controles[17])
    df_HC_18 = pd.read_csv(FilePath_controles[18])
    df_HC_19 = pd.read_csv(FilePath_controles[19])
    df_HC_20 = pd.read_csv(FilePath_controles[20])
    df_HC_21 = pd.read_csv(FilePath_controles[21])
    df_HC_22 = pd.read_csv(FilePath_controles[22])
    df_HC_23 = pd.read_csv(FilePath_controles[23])
    df_HC_24 = pd.read_csv(FilePath_controles[24])
    df_HC_25 = pd.read_csv(FilePath_controles[25])
    df_HC_26 = pd.read_csv(FilePath_controles[26])
    df_HC_27 = pd.read_csv(FilePath_controles[27])
    df_HC_28 = pd.read_csv(FilePath_controles[28])
    df_HC_29 = pd.read_csv(FilePath_controles[29])
    df_HC_30 = pd.read_csv(FilePath_controles[30])
    df_HC_31 = pd.read_csv(FilePath_controles[31])
    df_HC_32 = pd.read_csv(FilePath_controles[32])
    df_HC_33 = pd.read_csv(FilePath_controles[33])
    df_HC_34 = pd.read_csv(FilePath_controles[34])
    df_HC_35 = pd.read_csv(FilePath_controles[35])
    df_HC_36 = pd.read_csv(FilePath_controles[36])
    df_HC_37 = pd.read_csv(FilePath_controles[37])
    df_HC_38 = pd.read_csv(FilePath_controles[38])
    df_HC_39 = pd.read_csv(FilePath_controles[39])
    df_HC_40 = pd.read_csv(FilePath_controles[40])

    print(f"Shape paciente= {df_00.shape}")
    print(f"Shape controles= {df_HC_00.shape}")

    
    vertical_stack_completo = pd.concat([df_00, df_01,df_02,df_03,df_04,df_05,df_06,df_07,df_08,df_09,df_10,df_11,df_12,df_13,df_14,df_15,df_16,df_18,df_19,df_20,df_21,df_22,df_24,df_25,df_26,df_27,df_28,df_29,df_30,df_31,df_32,df_33,df_36,df_38,df_39, df_HC_00,df_HC_01,df_HC_02,df_HC_03,df_HC_04,df_HC_05,df_HC_06,df_HC_07,df_HC_08,df_HC_09,df_HC_10,df_HC_11,df_HC_12,df_HC_13,df_HC_14,df_HC_15,df_HC_16,df_HC_17,df_HC_18,df_HC_19,df_HC_20,df_HC_21,df_HC_22,df_HC_23,df_HC_24,df_HC_25,df_HC_26,df_HC_27,df_HC_28,df_HC_29,df_HC_30,df_HC_31,df_HC_32,df_HC_33,df_HC_34,df_HC_35,df_HC_36,df_HC_37,df_HC_38,df_HC_39,df_HC_40],axis=0)
    vertical_stack_completo.to_csv("TablaGeneralNueva.csv",index=False)
    print(f"Shape = {vertical_stack_completo.shape}")
    

if __name__ == '__main__':
    main()