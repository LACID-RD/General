#from inspect import CO_ITERABLE_COROUTINE
#from operator import contains
#import cmath
#from numpy.lib.npyio import save
#from skimage.io import imread, imsave
#import tkinter as tk
#from tkinter import filedialog
#from pydicom.uid import generate_uid
#import collections
#from scipy.optimize import least_squares, minpack2
#import math
#from lmfit import Model
#from lmfit import Parameters,minimize,fit_report
#from scipy.signal import lfilter, lfilter_zi, filtfilt, butter
#from matplotlib.pyplot import plot, legend, show, grid, figure, savefig
import matplotlib.pyplot as plt
import numpy as np
import sys
#NO IMPORT LOCAL CLASS !!!!
ERROR_LOG = " "

#############################
#############################
# Funciones Proce
#############################
#############################
# Main path
###################

def FP_main_path(path_main):
    global ERROR_LOG
    ERROR_LOG = path_main / "error_log.txt"
    with open(ERROR_LOG, 'w'):
        pass  # Doing nothing in the block effectively clears the file if it exists

###################
# Error log
###################
# code: 0-error, 1-warning

def FP_error_log(code, label_log):
    with open(ERROR_LOG, 'a') as log_file:
        log_file.write(label_log+"\n")  # Write a string to the file
    if code == 0:
        raise ValueError("Output Error. See error_log.txt")

###################
# Histogram analysis
###################
#1: Datos, 2:bins, 3:tamaño del filtro, 4:Transf, 5:Coef, 6:plt.show(n:0,y:1)
#4: 0)None, 1)Exp, 2)Log, 3)InvLog
#https://scipy-cookbook.readthedocs.io/items/FiltFilt.html

def FP_hist_analysis(hist_data, bins_num, window, transform, a_coef, var_print):
    if transform == 1: #y=Ae(Bx)
        b_coef = np.log(bins_num/a_coef)/bins_num
        hist_data = a_coef*np.exp(b_coef*hist_data)
    elif transform == 2: #y=Alog(Bx+1)
        b_coef = (np.exp(0.005*bins_num/a_coef)-1)/bins_num
        hist_data = 200*a_coef*np.log(b_coef*hist_data+1)
    elif transform != 0:
        raise ValueError("Error: No se realiza histograma (FPHist).")

    # Histogram
    count_vec, bins_vec = np.histogram(hist_data, bins=bins_num)
    bins_vec = np.delete(bins_vec, 0)

    # Zero filling
    zero_indices = count_vec == 0 # elements of count_vec that are zero
    for i in np.where(zero_indices)[0]: # zero_indices array where the value is True [0]:1D
        #Slice of count_vec from the start index to the end index.
        var_aux1 = count_vec[max(0,i-int(bins_num/10)):min(len(count_vec),i+int(bins_num/10))]
        var_aux1 = var_aux1[var_aux1 > 0][:window]
        count_vec[i] = np.mean(var_aux1)
    
    #print with plt
    if var_print == 1:
        plt.plot(bins_vec, count_vec)
        #plt.xlim([0, 30000])
        #plt.ylim([0, 30000])
        plt.show()

    return bins_vec, count_vec

###################
# Proyecta una imagen en otra
###################
# refSer2 en refSer1

def FP_serGeo_proj(ref_img1, ref_img2):

    plt.imshow(ref_img1.ImgData, cmap=plt.cm.bone)
    plt.show()
    plt.imshow(ref_img2.ImgData, cmap=plt.cm.bone)
    plt.show()
    print("Items:",ref_img1.StuItem,ref_img1.SerItem,ref_img2.StuItem,ref_img2.SerItem)
    #print()