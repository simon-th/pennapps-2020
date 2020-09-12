# https://pillow.readthedocs.io/en/stable/handbook/tutorial.html#more-on-reading-images
"""
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
# comp vision
import cv2
from collections import Counter
from skimage.color import rgb2lab, deltaE_cie76
import os

#%matplotlib inline # for ipython
image = cv2.imread('sam.jpg') # linting issue fixed in settings

print("The type of this input is {}".format(type(image))) # as numpy.ndarray

print("Shape: {}".format(image.shape)) # 2 dims and teh 3rd is the RGB dimension

image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # convert to rgb instead of grb

#breakpoint()
