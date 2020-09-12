# image and url librarie
import urllib.request
import PIL
from PIL import Image
import requests
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

"""input: direct image url
   outupt: a danceability score and a tempo score as a 2-list"""
def image_to_color_norm(image_url):

    # get image
    response = requests.get(image_url)
    file = open("image.jpg", "wb")
    file.write(response.content)
    file.close()

    # set image to array read in by opencv
    # TODO: get link from firebase
    image = cv2.imread("image.jpg") # linting issue fixed in settings

    # use cv2 to convert to R-G-B, default is B-R-G
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # convert to rgb instead of grb


    # Color Identification Section
    #converts labels from RGB to HEX
    # takes in a list of 3 for rgb
    def rgb_to_hex(color):
        r = int(color[0])
        g = int(color[1])
        b = int(color[2])

        return "#{:02x}{:02x}{:02x}".format(r,g,b)


    # K Means Algo: from Wikipedia:
    # k-means clustering is a method of vector quantization, 
    # originally from signal processing, that aims to partition 
    # n observations into k clusters in which each observation belongs 
    # to the cluster with the nearest mean (cluster centers or cluster centroid), 
    # serving as a prototype of the cluster

    # resize image so not that many pixels to iterate through:
    # not sure what interarea is but it = 3
    # mod_im now holds smaller color range values
    mod_im = cv2.resize(image, (400, 400), interpolation = cv2.INTER_AREA)

    mod_im = mod_im.reshape(mod_im.shape[0]*mod_im.shape[1], 3)

    kmean_obj = KMeans(n_clusters = 8) # just use default clusters

    # fit predict groups all members in a different clusters in KMean
    sections = kmean_obj.fit_predict(mod_im) # label with fit predict

    # The center of the cluster is the average of all points (elements) that belong to that cluster
    center_clust = kmean_obj.cluster_centers_
    # gives us weighted RGBs of each cluster :) 8 different lists

    # question is = what color corresponds with what - 1,2,3...num clus = 8
    ct = Counter(sections) # partititions data into different fit_pred sections
    # turns count of sections and members into ordered dictionary :)
    ct = dict(sorted(ct.items()))

    # order color sections by iterating through keys in the count dictionary
    sorted_list = [center_clust[i] for i in ct.keys()]

    hex_colors = [rgb_to_hex(sorted_list[i]) for i in ct.keys()]
    rgb_colors = [sorted_list[i] for i in ct.keys()]




    # tempo and dance
    # must be between 0 and 1 and 80 and 120
    # should just average the 8 sections and correspond to color
    # Step 1 : iterate through first of each 8 means, second of 8 means, 3 of 8 means
    # get "total " RGB
    # divide by 8 
    # norm the tempo
    r_vals = 0
    g_vals = 0
    b_vals = 0

    for arr in rgb_colors:
        r_vals += arr[0]
        g_vals += arr[1]
        b_vals += arr[2]

    overall_color = [r_vals, g_vals, b_vals]
    # divide by number of clusters to get overall image color
    overall_color = [(overall_color[0] / 8),(overall_color[1]/8), (overall_color[2]/8)]
    print(overall_color)

    color_norm = [x / 255 for x in overall_color]
    dance_color_norm = (color_norm[0] + color_norm[1] + color_norm[2]) / 3
    tempo_color_norm = (dance_color_norm * 40) + 80
    print(dance_color_norm, "and", tempo_color_norm)
    return [dance_color_norm, tempo_color_norm]



# driver code:
image_to_color_norm("https://i.imgur.com/F7JsReR.jpeg")
image_to_color_norm("https://i.imgur.com/R67FHau.jpg")