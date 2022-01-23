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

img = cv.imread(cv.samples.findFile("4.jpg"))
if img is None:
    sys.exit("Could not read the image.")

else :
    width , height , depth = img.shape
    # # Adding noise
    # for i in range (0,int(width*height*0.2)): # Around 20 percent pixels are noise
    #     color = r.randint(0, 255) 
    #     w = r.randint(0, width-1)
    #     h = r.randint(0, height-1)
    #     img[w][h][0] = color 
    #     img[w][h][1] = color
    #     img[w][h][2] = color
    img_noisy = noisy("gauss",img)
    
    for kernal_size in range (1,40,2): 
        print(kernal_size)
        kernel = np.ones((kernal_size,kernal_size),np.float32)/(kernal_size*kernal_size)
        dst = cv.filter2D(img_noisy,-1,kernel)
        file_name = "mean_blur" + str(kernal_size) + ".png"
        cv.imwrite(file_name, dst)