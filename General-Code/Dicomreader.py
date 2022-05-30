import pydicom
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import numpy as np

root = tk.Tk()
root.withdraw()

file_name = filedialog.askopenfilenames()

for i in file_name:
    Dcm = pydicom.dcmread(i)
    Dcm_im = np.copy(Dcm.pixel_array)
    plt.imshow(Dcm_im, cmap = plt.cm.bone)
    plt.show() 
   
    # print(Dcm)