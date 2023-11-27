from ntpath import join
from operator import ne
import shelve
import pydicom
import tkinter as tk
from tkinter import filedialog
import numpy as np
from collections import Counter
import gdcm
import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
#from Class_Image import CImage
#from Class_Proc import PProc
import math
from scipy import ndimage,misc,signal
from itertools import repeat
from scipy.stats.stats import pearsonr
import cv2

########## CT: 20
# 00CpTp: Media Storage

########################################
########################################
# DCM general CT
########################################
########################################

def CDMGeneCT(self):

    ########################################### Grosor de slice [21]
    self.D21SlTk=self.DcmImag[0x0018,0x0050].value
