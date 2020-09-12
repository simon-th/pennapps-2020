# https://pillow.readthedocs.io/en/stable/handbook/tutorial.html#more-on-reading-images
"""
# this was the first attempt lol - dint work
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
# Import KMeans from SciKit Learn cluster lib 
from sklearn.cluster import KMeans
# for plotting
import matplotlib.pyplot as plt
# turn image into array
import numpy as np
# computer vision
import cv2
# use dictionary to count cluster members at the end
from collections import Counter
# use skimage to convert to hex and rgb2
from skimage.color import rgb2lab, deltaE_cie76
import os


# set image to array read in by opencv
image = cv2.imread('sam.jpg') # linting issue fixed in settings

#print("The type of this input is {}".format(type(image))) # as numpy.ndarray
#print("Shape: {}".format(image.shape)) # 2 dims and teh 3rd is the RGB dimension

# use cv2 to convert to R-G-B, default is B-R-G
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # convert to rgb instead of grb

plt.imshow(image) # make image pop up - remove later on
#plt.show() #show the image

# to resize image in future:
# resized_image = cv2.resize(image, (1200, 600))
#plt.imshow(resized_image)

"""Color Identification Section"""
#converts labels from RGB to HEX
# takes in a list of 3 for rgb
def rgb_to_hex(color):
    r = int(color[0])
    g = int(color[1])
    b = int(color[2])

    return "#{:02x}{:02x}{:02x}".format(r,g,b)

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
# not sure what interarea is but it = 3
mod_im = cv2.resize(image, (400, 400), interpolation = cv2.INTER_AREA)

mod_im = mod_im.reshape(mod_im.shape[0]*mod_im.shape[1], 3)

kmean_obj = KMeans(n_clusters = 8) # just use default clusters

# fit predict groups all members in a different clusters in KMean
sections = kmean_obj.fit_predict(mod_im) # label with fit predict

# The center of the cluster is the average of all points (elements) that belong to that cluster
center_clust = kmean_obj.cluster_centers_
# gives us weighted RGBs of each cluster :) 8 different lists
#print(center_colors)

# question is = what color corresponds with what - 1,2,3...num clus = 8
ct = Counter(sections) # partititions data into different fit_pred sections
# turns count of sections and members into ordered dictionary :)
ct = dict(sorted(ct.items()))
#print(counts) # all clusters.


# order color sections by iterating through keys in the count dictionary
sorted_list = [center_clust[i] for i in ct.keys()]
#breakpoint()
hex_colors = [rgb_to_hex(sorted_list[i]) for i in ct.keys()]
rgb_colors = [sorted_list[i] for i in ct.keys()]
print(rgb_colors)

plt.figure(figsize = (8, 6))
plt.pie(counts.values(), labels = hex_colors, colors = hex_colors)
plt.show()

# tempo prototype
# must be between 0 and 1 
# should just average the 8 sections and correspond to color