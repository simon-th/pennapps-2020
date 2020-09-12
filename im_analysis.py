# https://pillow.readthedocs.io/en/stable/handbook/tutorial.html#more-on-reading-images
"""
# this was the first attempt lol

import urllib.request
import PIL
from PIL import Image
#breakpoint()

# get image
#image_url='https://imgur.com/a/KcK0oKQ.png'
image_url='https://imgur.com/a/7wAlncp'

urllib.request.urlretrieve(image_url, "im.jpg")
#breakpoint()
img = PIL.Image.open("im.jpg")
# show im
img.show()
"""
# clustering 
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
# computer vision
import cv2
from collections import Counter
from skimage.color import rgb2lab, deltaE_cie76
import os

#%matplotlib inline # for ipython
image = cv2.imread('sam.jpg') # linting issue fixed in settings

print("The type of this input is {}".format(type(image))) # as numpy.ndarray

print("Shape: {}".format(image.shape)) # 2 dims and teh 3rd is the RGB dimension

image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # convert to rgb instead of grb

plt.imshow(image) 
plt.show() #show the image

# to resize image in future:
# resized_image = cv2.resize(image, (1200, 600))
#plt.imshow(resized_image)

"""Color Identification Section"""
#converts labels from RGB to HEX
#def RGB2HEX(color):
    #return "#{:02x}{:02x}{:02x}".format(int(color[0]), int(color[1]), int(color[2]))

# reads image into RGB color space - condenses what we had above
def get_image(image_path):
    # turn into npy array as before
    image = cv2.imread(image_path)
    # convert to rgb as before
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image

# resize image so not that many pixels to iterate through:
mod_im = cv2.resize(image, (400, 400), interpolation = cv2.INTER_AREA)
#breakpoint()
mod_im = mod_im.reshape(mod_im.shape[0]*mod_im.shape[1], 3)
#breakpoint()

# mod_im now holds smaller color range values
"""K Means Algo:
k-means clustering is a method of vector quantization, 
originally from signal processing, that aims to partition 
n observations into k clusters in which each observation belongs 
to the cluster with the nearest mean (cluster centers or cluster centroid), 
serving as a prototype of the cluster"""

