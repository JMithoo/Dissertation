import cv2
import numpy as np 
from PIL import Image
import os

# Input and output paths
path    = "test"
outlinepath = path+"_outline/"
    
# Create directory if doesn't allready exist   
try:
    os.mkdir(outlinepath)
except OSError as err:
    print("Output Dir exists, skipping creation")

# Iterate through all binary mask files
for file in os.listdir(path):
    # get filepath
    filepath = os.path.join(path, file)
    # read in the image
    im = cv2.imread(filepath, 0)
    # convert image to a binary image
    im[im<50] =0
    im[im>=50] =255
    # get the contours from  the image, RETR_EXTERNAL signifies the outline and CHAIN_APPROX_NONE
    # signifies all points rather than simplified points.
    contours, hierarchy = cv2.findContours(im.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # Create empty numpy array the size of the image
    out = np.zeros_like(im)
    # draw contours on the empty numpy array
    cv2.drawContours(out, contours, -1, 255, 1)
    # overwrite the original image with the binary image
    cv2.imwrite(filepath, im)
    # write the contour file to the folder
    outpath = os.path.join(outlinepath, file)
    cv2.imwrite(outpath, out)

