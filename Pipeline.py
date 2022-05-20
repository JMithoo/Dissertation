from PIL import Image
from SINet.MyTesting import create_mask
from DMFN.pipe import inpaint_face
import imageio
import cv2
import numpy as np
from flask import Flask
from flask import request
import os
import fnmatch
from scipy import ndimage
import skimage 

# Initialise flask
app=Flask(__name__)
# Create endpoint
@app.route("/repaint",methods=["POST"])

def repaint():
    # read in masked image
    image = cv2.imread("out/image.jpg")
    # resize the image to be 256 x 256
    image = cv2.resize(image, (256,256), interpolation = cv2.INTER_AREA)
    # create the mask from the image segmentation network
    res = create_mask(image)
    # convert the image back to uint8, with regular pixel values
    res=cv2.normalize(res,None,alpha=0,beta=255,norm_type=cv2.NORM_MINMAX,dtype=cv2.CV_32F).astype(np.uint8)
    # convert the mask to binary image
    res[res<10] =0
    res[res>=10] =255
    # post processing mask to fill potential holes
    kernel = np.ones((7,7), np.uint8)
    res = cv2.morphologyEx(res, cv2.MORPH_CLOSE, kernel)
    res = cv2.dilate(res, kernel, iterations=2)
    res = ndimage.binary_fill_holes(res,structure =kernel)
    res = ndimage.binary_fill_holes(res,structure =kernel)
    res = skimage.img_as_uint(res)
    imageio.imwrite('./out/mask.jpg', res)
    # use inpaint model to get the predicted image
    output = inpaint_face()
    # output the predicted image
    if not os.path.exists("./out"):
        os.makedirs("./out")
    count = len(fnmatch.filter(os.listdir("./out"), '*.*'))
    filepath="./out/output_"+str(count)+".jpg"
    imageio.imwrite(filepath, output)
    # Send filepath to JS
    return filepath

# Open endpoint when the file is ran
# - Is needed for when spawned as child in NodeJS
if __name__ == '__main__':
    app.run()