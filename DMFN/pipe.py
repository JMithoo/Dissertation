import os
from DMFN.utils import get_config, _write_images
import torch
from DMFN.data import create_dataset, create_dataloader
from DMFN.models.networks import define_G
from DMFN.data.util import tensor2img
import skimage.io as sio
import numpy as np
from PIL import Image
import torchvision.transforms as transforms


print(torch.cuda.is_available())
os.environ["CUDA_VISIBLE_DEVICES"] = '1'

# Load experiment setting
config = get_config('DMFN/configs/celeba-hq-regular_list.yaml')
print(torch.cuda.is_available())
device = torch.device('cuda')
# Setup model and data loader

# Load model and trained state
model = define_G(config).to(device)
# Weights trained on celebA with random bboxs
model.load_state_dict(torch.load('DMFN/outputs/celebahq-regular/checkpoints/latest_G.pth'), strict=True)
# Weights trained on FFHQ with facemask masks
#model.load_state_dict(torch.load('DMFNtensorboard/outputs/ffhq/checkpoints/latest_G.pth'), strict=True)
model.eval()

# Transformer that would have been applied anyway
transform_list = [transforms.ToTensor(),
                          transforms.Normalize((0.5, 0.5, 0.5),
                                               (0.5, 0.5, 0.5))]  # [0, 1] --> [-1, 1]
transform = transforms.Compose(transform_list)

def inpaint_face():
        # Load images into dataset, as they would have been in testing
        # This also results in loading the image as a tensor         
        dataset_opt = config['datasets']['test']
        test_set = create_dataset(dataset_opt)
        test_loader = create_dataloader(test_set, dataset_opt)
                        
    # Start prediction
        for index, test_data in enumerate(test_loader):
                v_input, v_output, v_target = [], [], []
                visual_images = []
                # get variables from generated dataset
                var_input, var_mask, var_target, img_paths = test_data['input'], test_data['mask'], test_data['target'], \
                                                        test_data['paths']
                # Add variables to device
                var_input = var_input.to(device)
                var_mask = var_mask.to(device)
                var_target = var_target.to(device)
                # Predict Output
                var_output = var_mask.detach() * model(torch.cat([var_input, var_mask], dim=1)) + (
                        1 - var_mask.detach()) * var_input.detach()
                # Convert outputs to images
                v_input.append(var_input.detach()[0].float().cpu())
                v_output.append(var_output.detach()[0].float().cpu())
                v_target.append(var_target.detach()[0].float().cpu())
                visual_images.extend(v_input)
                visual_images.extend(v_output)
                visual_images.extend(v_target)
                saved_output = tensor2img(v_output)
                # Return predicted output
                return saved_output[0]
                

