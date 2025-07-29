import torch
import torchvision.transforms as transforms

from .utils import *

def inference(model,im1,im2,opts): # im1 ir, im2 vis
    trans = transforms.Compose([
        transforms.ToTensor(),
    ])

    [im1, im2] = [path_to_gray(im) for im in [im1,im2]]
    assert(im1.size == im2.size)
    [im1, im2] = [torch.unsqueeze(trans(im), 0)for im in [im1,im2]] # type: ignore
    [im1, im2] = [im.to(opts.device) for im in [im1,im2]]

    model.eval()
    with torch.no_grad():
        imf = model(im2,im1)
    
    imf = torch.clamp(imf, 0, 1)
    
    return imf[0,:,:,:]