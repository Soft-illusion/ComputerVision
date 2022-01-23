import cv2 as cv
import sys
import numpy as np
import random as r

img = cv.imread(cv.samples.findFile("4.jpg"))
if img is None:
    sys.exit("Could not read the image.")

else :
    width , height , depth = img.shape
    # Adding noise
    for i in range (0,1000000):
        w = r.randint(0, width-1)
        h = r.randint(0, height-1)
        img[w][h][0] = 0 
        img[w][h][1] = 0
        img[w][h][2] = 0
    
    for kernal_size in range (1,61,2):
        print(kernal_size)
        dst = cv.GaussianBlur(img,(kernal_size,kernal_size),0)
        # print( cv.getGaussianKernel(kernal_size,3))
        file_name = "gaussian_blur" + str(kernal_size) + ".png"
        cv.imwrite(file_name, dst)
