import numpy as np
import cv2 as cv

def arrs_gen():
    arrs = []
    for i in range(800):
        aux = np.random.rand(420,420)
        arrs.append(1000*aux)
    print(len(arrs))
    return arrs


def video_from_array(arrs, width, height):
    fourcc = cv.VideoWriter_fourcc(*'XVID')
    video = cv.VideoWriter('video.avi', fourcc, 1, (width, height))
    for arr in arrs:
        video.write(arr)
    cv.destroyAllWindows()
    video.release()

arrs = arrs_gen()
shape = np.shape(arrs)
video_from_array(arrs,shape[0],shape[1])
