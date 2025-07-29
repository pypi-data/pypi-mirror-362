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

    [Encoder, Decoder, BaseFuseLayer, DetailFuseLayer] = model
    feature_V_B, feature_V_D, feature_V = Encoder(im2) # VIS
    feature_I_B, feature_I_D, feature_I = Encoder(im1) # IR
    feature_F_B = BaseFuseLayer(feature_V_B + feature_I_B)
    feature_F_D = DetailFuseLayer(feature_V_D + feature_I_D)
    data_Fuse, _ = Decoder(im2, feature_F_B, feature_F_D)
    data_Fuse=(data_Fuse-torch.min(data_Fuse))/(torch.max(data_Fuse)-torch.min(data_Fuse))

    return data_Fuse[0,:,:,:]