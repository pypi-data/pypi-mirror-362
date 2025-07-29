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

    [Encoder_Base_Test, Encoder_Detail_Test, Decoder_Test] = model

    Encoder_Base_Test.eval()
    Encoder_Detail_Test.eval()
    Decoder_Test.eval()
    
    with torch.no_grad():
        B_K_IR,_,_=Encoder_Base_Test(im1)
        B_K_VIS,_,_=Encoder_Base_Test(im2)
        D_K_IR,_,_=Encoder_Detail_Test(im1)
        D_K_VIS,_,_=Encoder_Detail_Test(im2)
        
    if opts.addition_mode=='Sum':      
        F_b=(B_K_IR+B_K_VIS)
        F_d=(D_K_IR+D_K_VIS)

    elif opts.addition_mode=='Average':
        F_b=(B_K_IR+B_K_VIS)/2         
        F_d=(D_K_IR+D_K_VIS)/2

    elif opts.addition_mode=='l1_norm':
        F_b=l1_addition(B_K_IR,B_K_VIS,device=opts.device)
        F_d=l1_addition(D_K_IR,D_K_VIS,device=opts.device)
        
    with torch.no_grad():
        Out = Decoder_Test(F_b,F_d)
     
    return Out[0,:,:,:]