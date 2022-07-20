import numpy as np
import cv2
import os
from tkinter import filedialog
import pydicom as dicom

from study_Class import *

def dcmObject_to_avi():
    output = "C:\\Users\\roalm\\OneDrive\\Escritorio\\New folder"

    obj, arr = objectGenerator()
    arr = np.array(arr)
    width, height, frame_num = np.shape(arr)
    fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
    video = cv2.VideoWriter(output, fourcc, 15, (width, height))

    #video = cv2.VideoWriter(output, fourcc, 15, (width, height)) # Initialize Video File   

    for frame in arr:
            
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        video.write(frame_rgb)
        print(frame_rgb.shape)
        print(frame_rgb)
        print(frame.shape)
        print(frame)


        #cv2.imshow('frame', frame_rgb)


    video.release()
    #cv2.destroyAllWindows() 
dcmObject_to_avi()