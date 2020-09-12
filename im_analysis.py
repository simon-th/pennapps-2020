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
#plt.show() #show the image

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



# mod_im now holds smaller color range values
"""K Means Algo: from Wikipedia:
k-means clustering is a method of vector quantization, 
originally from signal processing, that aims to partition 
n observations into k clusters in which each observation belongs 
to the cluster with the nearest mean (cluster centers or cluster centroid), 
serving as a prototype of the cluster"""

# resize image so not that many pixels to iterate through:
mod_im = cv2.resize(image, (400, 400), interpolation = cv2.INTER_AREA)

mod_im = mod_im.reshape(mod_im.shape[0]*mod_im.shape[1], 3)

clf = KMeans(n_clusters = 8) # just use default clusters

labels = clf.fit_predict(mod_im) #label with fit predict

# question is = what color corresponds with what - 1,2,3...8
counts = Counter(labels) # partititions data into different fit_pred sections

# sort to ensure correct color percentage
counts = dict(sorted(counts.items()))
#print(counts) # all clusters.

# The center of the cluster is the average of all points (elements) that belong to that cluster
center_colors = clf.cluster_centers_
# gives us weighted RGBs of each cluster :)
print(center_colors)
""""
def get_colors(image, number_of_colors, show_chart):
    
    modified_image = cv2.resize(image, (400, 400), interpolation = cv2.INTER_AREA)
    modified_image = modified_image.reshape(modified_image.shape[0]*modified_image.shape[1], 3)
    
    # user decides how many clusters to use for n choose K means
    clf = KMeans(n_clusters = number_of_colors)

    # predict closest cluster each sample belongs to
    # carefuly not to apply too many times
    # each time yields futher predict fit?
    # WARNING do not use huge num of colors - use default 8 clusters
    labels = clf.fit_predict(modified_image)
    

    counts = Counter(labels)
    # sort to ensure correct color percentage
    counts = dict(sorted(counts.items()))
    
    center_colors = clf.cluster_centers_
    # We get ordered colors by iterating through the keys
    ordered_colors = [center_colors[i] for i in counts.keys()]
    hex_colors = [RGB2HEX(ordered_colors[i]) for i in counts.keys()]
    rgb_colors = [ordered_colors[i] for i in counts.keys()]

    if (show_chart):
        plt.figure(figsize = (8, 6))
        plt.pie(counts.values(), labels = hex_colors, colors = hex_colors)
    
    return rgb_colors
"""