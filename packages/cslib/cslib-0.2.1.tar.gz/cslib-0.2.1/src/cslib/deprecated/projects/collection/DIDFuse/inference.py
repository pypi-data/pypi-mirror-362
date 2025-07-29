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

    [AE_Encoder1, AE_Decoder1] = model

    AE_Encoder1.eval()
    AE_Decoder1.eval()
    
    with torch.no_grad():
        F_i1,F_i2,F_ib,F_id=AE_Encoder1(im1)
        F_v1,F_v2,F_vb,F_vd=AE_Encoder1(im2)
        
    if opts.addition_mode=='Sum':      
        F_b=(F_ib+F_vb)
        F_d=(F_id+F_vd)
        F_1=(F_i1+F_v1)
        F_2=(F_i2+F_v2)
    elif opts.addition_mode=='Average':
        F_b=(F_ib+F_vb)/2         
        F_d=(F_id+F_vd)/2
        F_1=(F_i1+F_v1)/2
        F_2=(F_i2+F_v2)/2
    elif opts.addition_mode=='l1_norm':
        F_b=l1_addition(F_ib,F_vb)
        F_d=l1_addition(F_id,F_vd)
        F_1=l1_addition(F_i1,F_v1)
        F_2=l1_addition(F_i2,F_v2)
    else:
        raise ValueError(f"wrong opts.addition_mode: {opts.addition_mode}")
        
    with torch.no_grad():
        Out = AE_Decoder1(F_1,F_2,F_b,F_d)
     
    return Out[0,:,:,:]