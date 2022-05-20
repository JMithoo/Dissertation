import torch
import torch.nn.functional as F
import torchvision.transforms as transforms
import numpy as np
import os, argparse
from scipy import misc
import cv2
from SINet.lib.Network_Res2Net_GRA_NCD import Network
from SINet.utils.data_val import test_dataset
import imageio
from torch.autograd import Variable
from PIL import Image
# parser = argparse.ArgumentParser()
# parser.add_argument('--testsize', type=int, default=352, help='testing size')
# parser.add_argument('--pth_path', type=str, default='SINet/snapshot/SINet_V2/Net_epoch_best.pth')
# opt = parser.parse_args()

# for _data_name in ['masks']:
#     data_path = './SINet/Dataset/TestDataset/{}/'.format(_data_name)
#     save_path = './res/{}/{}/'.format(opt.pth_path.split('/')[-2], _data_name)
#     model = Network(imagenet_pretrained=False)
#     model.load_state_dict(torch.load(opt.pth_path))
#     model.cuda()
#     model.eval()

#     os.makedirs(save_path, exist_ok=True)
#     image_root = '{}/Imgs/'.format(data_path)
#     gt_root = '{}/GT/'.format(data_path)
#     test_loader = test_dataset(image_root, gt_root, opt.testsize)

#     for i in range(test_loader.size):
#         image, gt, name, _ = test_loader.load_data()
#         gt = np.asarray(gt, np.float32)
#         gt /= (gt.max() + 1e-8)
#         image = image.cuda()
#         print(image.shape)
#         res5, res4, res3, res2 = model(image)
#         res = res2
#         res = F.upsample(res, size=gt.shape, mode='bilinear', align_corners=False)
#         res = res.sigmoid().data.cpu().numpy().squeeze()
#         res = (res - res.min()) / (res.max() - res.min() + 1e-8)
#         print('> {} - {}'.format(_data_name, name))
#         imageio.imwrite(save_path+name, res)
#         # If `mics` not works in your environment, please comment it and then use CV2
#         # cv2.imwrite(save_path+name,res*255)

# Initialise the model and load the saved model from training
print("Initialising binary mask network...")
state_path="SINet/snapshot/SINet_V2/Net_epoch_best.pth"
model = Network(imagenet_pretrained=False)
model.load_state_dict(torch.load(state_path))
model.cuda()
model.eval()
# transform function used in preprocessing of images when they were
# loaded from a dataset, needed to replicate image loading
trans= transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])

print("...Completed!")


# testing wrapped in a function
def create_mask(img):
    # convert cv2 numpy array image to PIL
    img=Image.fromarray(img)
    # specify RGB image type
    img = img.convert('RGB')
    # Transform image like it would have been when loaded
    image=trans(img).unsqueeze(0)
    # Load image into GPU
    image = image.cuda()
    # predict mask
    res5, res4, res3, res2 = model(image)
    res = res2
    # upsample image
    res = F.upsample(res, size=img.size, mode='bilinear', align_corners=False)
    res = res.sigmoid().data.cpu().numpy().squeeze()
    res = (res - res.min()) / (res.max() - res.min() + 1e-8)
    return res