import torch
import torchvision.transforms as transforms
from torch.autograd import Variable

from .utils import *

def inference(model,im1,im2,opts):
    if hasattr(opts, "height") and hasattr(opts, "width"):
        trans = transforms.Compose([
            transforms.ToTensor(),
            transforms.Resize([opts.height, opts.width], interpolation=transforms.InterpolationMode.NEAREST),
        ])
    else:
        trans = transforms.Compose([transforms.ToTensor(),])

    [im1, im2] = [path_to_gray(im) for im in [im1,im2]]
    [im1, im2] = [torch.unsqueeze(trans(im), 0) for im in [im1,im2]] # type: ignore
    assert(im1.shape == im2.shape)
    [im1, im2] = [im.to(opts.device) for im in [im1,im2]]
    
    model.eval()
    with torch.no_grad():
        img_ir, h, w, c = get_test_images(im1)
        img_vi, h, w, c = get_test_images(im2)

        img_fusion_blocks = []
        for i in range(c):
            img_vi_temp = img_vi[i]
            img_ir_temp = img_ir[i]
            img_vi_temp = Variable(img_vi_temp, requires_grad=False)
            img_ir_temp = Variable(img_ir_temp, requires_grad=False)
            # encoder
            tir3 = model.encoder(img_ir_temp)
            tvi3 = model.encoder(img_vi_temp)
            # fusion
            f = model.fusion(tir3, tvi3, opts.fusion_type)
            # decoder
            img_fusion = model.up_x4(f)
            img_fusion = ((img_fusion / 2) + 0.5) * 255
            img_fusion_blocks.append(img_fusion)

        if 224 < h < 448 and 224 < w < 448:
            img_fusion_list = recons_fusion_images1(img_fusion_blocks, h, w, opts.device)
        if 448 < h < 672 and 448 < w < 672:
            img_fusion_list = recons_fusion_images2(img_fusion_blocks, h, w, opts.device)
        if 448 < h < 672 and 672 < w < 896:
            img_fusion_list = recons_fusion_images3(img_fusion_blocks, h, w, opts.device)
        if 224 < h < 448 and 448 < w < 672:
            img_fusion_list = recons_fusion_images4(img_fusion_blocks, h, w, opts.device)
        if 672 < h < 896 and 896 < w < 1120:
            img_fusion_list = recons_fusion_images5(img_fusion_blocks, h, w, opts.device)
        if 0 < h < 224 and 224 < w < 448:
            img_fusion_list = recons_fusion_images6(img_fusion_blocks, h, w, opts.device)
        if 0 < h < 224 and 448 < w < 672:
            img_fusion_list = recons_fusion_images7(img_fusion_blocks, h, w, opts.device)
        if h == 224 and 448 < w < 672:
            img_fusion_list = recons_fusion_images8(img_fusion_blocks, h, w, opts.device)
        assert len(img_fusion_list) == 1

        img_fusion = img_fusion_list[0]
        min_val = torch.min(img_fusion)
        max_val = torch.max(img_fusion)
        img_fusion = (img_fusion - min_val) / (max_val - min_val)

        return img_fusion