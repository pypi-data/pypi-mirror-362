import torch
import torchvision.transforms as transforms

from .utils import path_to_gray,path_to_rgb

def inference(model,im1,im2,opts):
    trans = transforms.Compose([
        transforms.ToTensor(),
    ])

    if opts.color == 'gray':
        [im1, im2] = [path_to_gray(im) for im in [im1,im2]]
        [im1, im2] = [torch.unsqueeze(trans(im), 0) for im in [im1,im2]] # type: ignore
        assert(im1.shape == im2.shape)
        [im1, im2] = [im.to(opts.device) for im in [im1,im2]]
        im1_list = [im1]
        im2_list = [im2]
    elif opts.color == 'color':
        [im1, im2] = [path_to_rgb(im) for im in [im1,im2]]
        [im1, im2] = [torch.unsqueeze(trans(im), 0) for im in [im1,im2]] # type: ignore
        assert(im1.shape == im2.shape)
        [im1, im2] = [im.to(opts.device) for im in [im1,im2]]
        im1_list = [im1[:, 0+i:1+i, :, :] for i in range(3)]
        im2_list = [im2[:, 0+i:1+i, :, :] for i in range(3)]
    else:
        raise ValueError("Color mode should only be `gray` or `color`")

    model.eval()
    with torch.no_grad():
        imf_list = []
        for _im1,_im2 in zip(im1_list,im2_list):
            en_r = model.encoder(_im1)
            en_v = model.encoder(_im2)
            f = model.fusion(en_r, en_v)
            imf_list.append(model.decoder(f)[0])
        
        if opts.color == 'gray':
            img_fusion = imf_list[0]
        else:
            img_fusion = torch.cat([imf_list[0], imf_list[1], imf_list[2]], dim=1)
    return img_fusion[0,:,:,:]