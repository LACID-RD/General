#import matplotlib.pyplot as plt
from numpy.lib.npyio import save
#import pydicom
import tkinter as tk
from tkinter import Image, filedialog
#import numpy as np
#import collections
from scipy.optimize import least_squares
#import gdcm
import sys
#import cv2 as cv
#from PIL import Image
from skimage.color import gray2rgb
from skimage import color
from skimage.util import img_as_ubyte,img_as_float
#import tempfile
#import pandas as pd
#import math
#import SimpleITK as sitk
#from lmfit import Model
#from class_dicom import ObjetoDicom
import os
#from Class_Image import CImage
from Class_Study import CStudy


######################################################################
################### Main #############################################
######################################################################

def main():
    Std1=CStudy()
    Std1.read_img(Std1.load_img())

#Ejecuta función main() 
if __name__ == '__main__':
    main()
    