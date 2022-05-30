from bct.algorithms.centrality import betweenness_wei
from bct.algorithms.clustering import clustering_coef_wu
from bct.algorithms.degree import degrees_und, strengths_und
from bct.algorithms.distance import distance_wei, efficiency_wei
from bct.algorithms.physical_connectivity import density_und
from bct.utils.other import weight_conversion
import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import filedialog
import bct
from timeit import default_timer as timer 


def normalizar_mat(Conn_np, waytotal): #Limpia la matriz de conectividad, manda a 0 la diagonal principal, saca los NaN e Inf y se asegura que los valores de conectividad sean positivos
    UmbralConect = 0 #Para evitar falsos positivos
    mm = Conn_np.shape[0]
    nn = Conn_np.shape[1]
    Znorm = np.zeros((mm,nn))
    for i in range(mm):
        for j in range(nn):
            if (not(isinstance(Conn_np[i,j],str))): #como hay varios elementos NaN o Inf, se fija si cada elemento es una string
                if (Conn_np[i,j]>UmbralConect):
                    Znorm[i,j] = Conn_np[i,j]/waytotal[i]
                else:
                    Znorm[i,j]= 0
            else:
                Znorm[i,j]=0
    for i in range(mm):
        for j in range(nn):
            Znorm[i,j] = (Znorm[i,j]+Znorm[j,i])/2
            Znorm[j,i] = Znorm[i,j]
            if i == j:
                Znorm[i,j] = 1
    return Znorm

def normalizar_met_mat(matriz): #Limpia la matriz, saca los NaN e Inf y se asegura que los valores de conectividad sean positivos
    mm = matriz.shape[0]
    nn = matriz.shape[1]
    matnorm = np.zeros((mm,nn))
    for i in range(mm):
        for j in range(nn):
            if (isinstance(matriz[i,j],str)): #como hay varios elementos NaN o Inf, se fija si cada elemento es una string
                matnorm[i,j]=0
    return matnorm

def normalizar_met_vec(vector): #Limpia el vector, saca los NaN e Inf
    mm = vector.shape[0]
    vecnorm = np.zeros((mm))
    for i in range(mm):
        if (isinstance(vector[i],str)): #como hay varios elementos NaN o Inf, se fija si cada elemento es una string
            vecnorm[i]=0
    return vecnorm


def metricas(W):
    # Matrix L: conversion of connection weights to connection lengths, defined as the inverse of the connection weights matrix
    L = bct.weight_conversion(W, 'lengths')

    # Fix matrix (remove all inf and NaN values, remove all self-connections, ensures that matrices are exactly symmetric.)
    # W_fix = weight_conversion(W, 'autofix')

    # Degree: number of links connected to the node
    deg = degrees_und(W)

    # Strength: sum of weights of links connected to the node
    strength = strengths_und(W)

    # Density: fraction of present connections to possible connections
    density, vert, edge = density_und(W)
    
    # Clustering coefficient: fraction of triangles around a node (fraction of node neighbors that are neighbors of each other)
    cluster_coef = clustering_coef_wu(W)

    # Global and local efficiency - Global efficiency is the average inverse shortest path length in the network and is inversely related to the characteristic path length.
    # Local efficiency: global efficiency computed on neighborhood of the node and is related to the clustering coefficient

    global_efficiency = efficiency_wei(W)
    local_efficiency = efficiency_wei(W,2)

    # Distance matrix: contains lengths of the shortest paths between all pairs of nodes. An entry (u,v) represents the length of the shortest path from node u to node v. The average shortest path length is the characteristic path length of the network.
    # Outputs:
    #   distance_matrix: distance (shortest weighted path) matrix
    #   edges_distance: number of edges in shortest weighted path matrix
    distance_matrix, edges_distance = distance_wei(L)

    # Betweenness centrality: fraction of all shortest paths in the network that contain a given node. Nodes with high values of betweenness centrality participate in a large number of shortest paths.
    BC = betweenness_wei(L)

    return L, deg, strength, density, vert, edge, cluster_coef, global_efficiency, local_efficiency, distance_matrix, edges_distance, BC


def main():
    #Ingrese numero de sujeto
    num_paciente = input("Ingrese el numero de sujeto")
    #Abre cuadro de diálogo y toma el path del archivo seleccionado de la matriz de conectividad estructural
    cuadro = tk.Tk()
    cuadro.withdraw()
    FilePath_matriz = filedialog.askopenfilename() #Primero seleccionar el archivo fdt_network_matrix
    FilePath_waytotal = filedialog.askopenfilename() #Después seleccionar el waytotal
    #Lee la matriz de conectividad estructural (fdt_network_matrix) y el archivo waytotal
    df_Conn = pd.read_csv(FilePath_matriz, sep='\s+', header=None)
    df_waytotal = pd.read_csv(FilePath_waytotal, sep='\s+', header=None)
    #Transforma los dataframes a numpy
    Conn_np = df_Conn.to_numpy()
    waytotal_np = df_waytotal.to_numpy()

    Znorm =normalizar_mat(Conn_np, waytotal_np) #Llama a la función para normalizar la matriz de conectividad
    #Calcula las métricas de conectividad:
    L, deg, strength, density, vert, edge, cluster_coef, global_efficiency, local_efficiency, distance_matrix, edges_distance, BC = metricas(Znorm)
    #Normalizo metricas que son matrices:
    distmat_norm = normalizar_met_mat(distance_matrix)
    edgdist_norm = normalizar_met_mat(edges_distance)
    #Normalizo metricas que son vectores:
    BC_norm = normalizar_met_vec(BC)
    clustercoef_norm = normalizar_met_vec(cluster_coef)
    deg_norm = normalizar_met_vec(deg)
    localeff_norm = normalizar_met_vec(local_efficiency)
    str_norm = normalizar_met_vec(strength)

    mat_conn_tri = np.triu(Znorm) #Extrae la matriz triangular superior de la matriz de conectividad normalizada
    mat_conn_tri_cerebro = np.zeros((94,94))

    for i in range(94):
        for j in range(94):
            mat_conn_tri_cerebro[i,j] = mat_conn_tri[i,j] #Sacamos regiones del cerebelo, nos quedamos solo con cerebro

    #print(mat_conn_tri_cerebro.shape)

    list_mat_conn_tri = list(mat_conn_tri_cerebro[np.triu_indices(94, k=1)]) #Convierte la matriz triangular superior en una lista, que es la que vamos a cargar en la tabla para IA

    Conn_ord_df = pd.DataFrame(Znorm)
    deg_ord_df = pd.DataFrame(deg_norm)
    strength_ord_df = pd.DataFrame(str_norm)
    cluster_coef_ord_df = pd.DataFrame(clustercoef_norm)
    local_efficiency_ord_df = pd.DataFrame(localeff_norm)
    distance_matrix_ord_df = pd.DataFrame(distmat_norm)
    edges_distance_ord_df = pd.DataFrame(edgdist_norm)
    BC_ord_df = pd.DataFrame(BC_norm)
    mat_tri_df = pd.DataFrame(mat_conn_tri)
    mat_tri_cerebro_df = pd.DataFrame(mat_conn_tri_cerebro)
    list_mat_tri_df = pd.DataFrame(list_mat_conn_tri)


    Conn_ord_df.to_csv(f"{num_paciente}/MCS_{num_paciente}.csv")
    deg_ord_df.to_csv(f"{num_paciente}/degS_{num_paciente}.csv")
    strength_ord_df.to_csv(f"{num_paciente}/strS_{num_paciente}.csv")
    cluster_coef_ord_df.to_csv(f"{num_paciente}/ccS_{num_paciente}.csv")
    local_efficiency_ord_df.to_csv(f"{num_paciente}/loceffS_{num_paciente}.csv")
    distance_matrix_ord_df.to_csv(f"{num_paciente}/dmatS_{num_paciente}.csv")
    edges_distance_ord_df.to_csv(f"{num_paciente}/edistS_{num_paciente}.csv")
    BC_ord_df.to_csv(f"{num_paciente}/BCS_{num_paciente}.csv")
    mat_tri_df.to_csv(f"{num_paciente}/MTriS_{num_paciente}.csv")
    mat_tri_cerebro_df.to_csv(f"{num_paciente}/MTriBrainS_{num_paciente}.csv")
    list_mat_tri_df.to_csv(f"{num_paciente}/ListTriS_{num_paciente}.csv")

    print(f"{num_paciente} FINALIZADO CON EXITO")



if __name__ == '__main__':
    main()