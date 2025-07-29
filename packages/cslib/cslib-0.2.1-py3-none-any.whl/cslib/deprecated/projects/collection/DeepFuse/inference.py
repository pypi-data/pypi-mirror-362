import torchvision.transforms as transforms
import torch

from .utils import *

def inference(model,im1,im2,opts):
    # Load the Image
    trans = transforms.Compose([
        transforms.ToTensor(),
        transforms.Resize((opts.H, opts.W), antialias=True) if opts.resize else transforms.Lambda(lambda x: x), # type: ignore
        transforms.Normalize(mean = [0.485, 0.456, 0.406], std = [0.229, 0.224, 0.225])
    ])

    [im1, im2] = [path_to_ycbcr(im) for im in [im1,im2]]
    assert(im1.size == im2.size)
    [im1, im2] = [torch.unsqueeze(trans(im), 0)for im in [im1,im2]] # type: ignore
    [im1, im2] = [im.to(opts.device) for im in [im1,im2]]

    # Fusion
    model.eval()
    with torch.no_grad():
        f_y = model.forward(im1[:,0:1,:,:], im2[:,0:1,:,:])  # Inference
        [f_cb, f_cr] = weightedFusion(im1[:, 1:2], im2[:, 1:2], im1[:, 2:3], im2[:, 2:3])
        [f_cb, f_cr] = weightedFusion(im1[:, 1:2], im2[:, 1:2], im1[:, 2:3], im2[:, 2:3])
        fused = torch.cat((f_y,f_cb,f_cr),dim=1)
    
    # Reconstruct the Fused RGB Image
    inv_trans = transforms.Compose([
        transforms.Normalize(mean=[0., 0., 0.], std=[1/0.229, 1/0.224, 1/0.225]),
        transforms.Normalize(mean=[-0.485, -0.456, -0.406], std=[1., 1., 1.]),
    ])

    fused = inv_trans(fused)
    fused = ycbcr_to_rgb(transforms.ToPILImage()(fused[0,:,:,:]))

    return transforms.ToTensor()(fused)
