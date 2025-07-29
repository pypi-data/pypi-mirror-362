import torch
import torchvision.transforms as transforms
import numpy as np
from PIL import Image

from ....utils import path_to_rgb
from .utils import *

def inference(model, iml, img, opts):
    # Start the verification mode of the model.
    model.eval()

    # Read LR image and HR image
    lr_image = np.array(path_to_rgb(iml)) / 255.0
    
    # Get Y channel image data
    lr_y_image = rgb2ycbcr(lr_image, True)

    # Get Cb Cr image data from hr image
    lr_ycbcr_image = rgb2ycbcr(lr_image, False)
    [_, lr_cb_image, lr_cr_image] = [lr_ycbcr_image[:,:,i] for i in range(3)]

    # Convert RGB channel image format data to Tensor channel image format data
    lr_y_tensor = image2tensor(lr_y_image, False, False).unsqueeze_(0)

    # Transfer Tensor channel image format data to CUDA device
    lr_y_tensor = lr_y_tensor.to(device=opts.device)

    # Only reconstruct the Y channel image data.
    with torch.no_grad():
        sr_y_tensor = model(lr_y_tensor).clamp_(0, 1.0)

    # Save image
    sr_y_image = tensor2image(sr_y_tensor, False, False)
    sr_y_image = sr_y_image.astype(np.float32) / 255.0
    sr_ycbcr_image = np.stack([sr_y_image[:,:,0], lr_cb_image, lr_cr_image],axis=-1)
    sr_image = ycbcr2rgb(sr_ycbcr_image)
    sr_image = (np.clip(sr_image*255.0, 0, 255)).astype(np.uint8) # Important!
    sr_image = Image.fromarray(np.array(sr_image))
    return transforms.ToTensor()(sr_image)
