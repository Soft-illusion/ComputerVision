import cv2 as cv
import sys
import numpy as np
import random as r
import os 
from PIL import Image as im

def noisy(noise_typ,image):
    if noise_typ == "gauss":
        # Generate Gaussian noise
        gauss = np.random.normal(0,1,image.size)
        print(gauss)
        gauss = gauss.reshape(image.shape[0],image.shape[1],image.shape[2]).astype('uint8')
        # Add the Gaussian noise to the image
        img_gauss = cv.add(image,gauss)
        cv.imwrite("Noise.png", gauss)
        return img_gauss

    elif noise_typ == "s&p":
      row,col,ch = image.shape
      s_vs_p = 0.5
      amount = 0.004
      out = np.copy(image)
      # Salt mode
      num_salt = np.ceil(amount * image.size * s_vs_p)
      coords = [np.random.randint(0, i - 1, int(num_salt))
              for i in image.shape]
      out[coords] = 1

      # Pepper mode
      num_pepper = np.ceil(amount* image.size * (1. - s_vs_p))
      coords = [np.random.randint(0, i - 1, int(num_pepper))
              for i in image.shape]
      out[coords] = 0
      return out
    elif noise_typ == "poisson":
        vals = len(np.unique(image))
        vals = 2 ** np.ceil(np.log2(vals))
        noisy = np.random.poisson(image * vals) / float(vals)
        return noisy
    elif noise_typ =="speckle":
        row,col,ch = image.shape
        gauss = np.random.randn(row,col,ch)
        gauss = gauss.reshape(row,col,ch)        
        noisy = image + image * gauss
        return noisy

img = cv.imread(cv.samples.findFile("3.png"))
if img is None:
    sys.exit("Could not read the image.")

else :
    width , height , depth = img.shape
    img_noisy = noisy("gauss",img)

    for kernal_size in range (1,71,2):
        print(kernal_size)
        dst = cv.GaussianBlur(img_noisy,(kernal_size,kernal_size),0)
        # print( cv.getGaussianKernel(kernal_size,0))
        file_name = "gaussian_blur" + str(kernal_size) + ".png"
        cv.imwrite(file_name, dst)

    #     dst = img_noisy
    # for kernal_no in range (0,200):
    #     print(kernal_no)
    #     dst = cv.GaussianBlur(dst,(3,3),1)
    #     # print( cv.getGaussianKernel(kernal_size,3))
    #     file_name = "gaussian_blur" + str(kernal_no) + ".png"
    #     cv.imwrite(file_name, dst)

    for kernal_size in range (1,71,2):
        print(kernal_size)
        dst = cv.bilateralFilter(img_noisy,kernal_size,300,300)
        # print( cv.getGaussianKernel(kernal_size,0))
        file_name = "bilateral_blur" + str(kernal_size) + ".png"
        cv.imwrite(file_name, dst)
