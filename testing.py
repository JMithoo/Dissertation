import torch
from torchvision import transforms
from PIL import Image
from torchmetrics import PeakSignalNoiseRatio
from torchmetrics import StructuralSimilarityIndexMeasure
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
import shutil

def repaint(img_path):
    # read in masked image
    image = cv2.imread(img_path)
    #create image for inpainting model
    dest = shutil.copyfile(img_path, "out/image.jpg")
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
    filepath="./out/output_"+"test"+".jpg"
    imageio.imwrite(filepath, output)
    # Send filepath to JS
    return filepath



# Initialise metrics
psnr = PeakSignalNoiseRatio()
ssim = StructuralSimilarityIndexMeasure()
# Paths
masked_path = "Datasets/FFHQ/images256x256_masked"
GT_path = "Datasets/FFHQ/images256x256"

# Misc vars
max_ssim=-2
max_ssim_name=""
min_ssim=2
min_ssim_name=""

min_psnr=100
min_psnr_name=""
max_psnr=-2
max_psnr_name=""

avg_psnr=0
avg_ssim=0

c=0

# Transform to tensor
trans= transforms.Compose([transforms.ToTensor()])

for file in os.listdir(masked_path):
    print(c)
    # get filepaths
    filepath = os.path.join(masked_path, file)
    GT_filepath = os.path.join(GT_path, file)
    # Retrieve images
    Original = Image.open(GT_filepath)
    im_path = repaint(filepath)
    predicted = Image.open(im_path) 
    # Add batch channel and apply transform
    Original = trans(Original).unsqueeze(0)
    predicted = trans(predicted).unsqueeze(0)

    pval = psnr(predicted, Original)
    sval = ssim(predicted, Original)
    # Update avgs
    avg_psnr+=pval
    avg_ssim+=sval
    # Update min and maxs
    if pval > max_psnr:
        max_psnr = pval
        max_psnr_name = filepath
    if pval < min_psnr:
        min_psnr = pval
        min_psnr_name = filepath

    if sval > max_ssim:
        max_ssim = sval
        max_ssim_name = filepath
    if sval < min_ssim:
        min_ssim = sval
        min_ssim_name = filepath
    c+=1
    if c>1000:
        break


avg_psnr=avg_psnr/c
avg_ssim=avg_ssim/c
# Print results
print("Avg psnr:",avg_psnr)
print("Avg ssim:",avg_ssim)
print("\n")
print("max psnr:",max_psnr)
print("max psnr path:",max_psnr_name)
print("min psnr:",min_psnr)
print("min psnr path:",min_psnr_name)
print("\n")
print("max ssim:",max_ssim)
print("max ssim path:",max_ssim_name)
print("min ssim:",min_ssim)
print("min ssim path:",min_ssim_name)
print("\n")
