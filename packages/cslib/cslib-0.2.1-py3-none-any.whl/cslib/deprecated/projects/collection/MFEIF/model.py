from typing import List
import torch
import torch.nn as nn
from kornia.filters import SpatialGradient

def load_model(opts):
    model = MEFIF()
    params = torch.load(opts.pre_trained, map_location='cpu') # model parameters
    model.net_ext.load_state_dict(params['ext']) # load extractor
    model.net_con.load_state_dict(params['con']) # load constructor
    model.net_att.load_state_dict(params['att']) # load attention layer
    model.to(opts.device)

    return model


class MEFIF(nn.Module):
    def __init__(self):
        super(MEFIF, self).__init__()
        self.net_ext = Extractor()
        self.net_con = Constructor()
        self.net_att = Attention()
        self.softmax = torch.nn.Softmax(dim=1)
        self.feather_fuse = FeatherFuse()
    
    def forward(self, ir: torch.Tensor, vi: torch.Tensor) -> torch.Tensor:
        ir_1, ir_b_1, ir_b_2 = self.net_ext(ir)
        vi_1, vi_b_1, vi_b_2 = self.net_ext(vi)

        ir_att = self.net_att(ir)
        vi_att = self.net_att(vi)

        fus_1 = ir_1 * ir_att + vi_1 * vi_att
        fus_1 = self.softmax(fus_1)
        fus_b_1, fus_b_2 = self.feather_fuse((ir_b_1, ir_b_2), (vi_b_1, vi_b_2))

        fus_2 = self.net_con(fus_1, fus_b_1, fus_b_2)
        return fus_2


class ConvBlock(nn.Module):
    def __init__(self, in_channels: int, out_channels: int, k: int = 3, s: int = 1, p: int = 0, d: int = 1):
        super(ConvBlock, self).__init__()

        self.conv = nn.Conv2d(in_channels, out_channels, (k, k), (s, s), (p, p), (d, d))
        self.bn = nn.BatchNorm2d(out_channels)
        self.relu = nn.ReLU()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.conv(x)
        x = self.bn(x)
        x = self.relu(x)
        return x
    
    
class Constructor(nn.Module):
    def __init__(self):
        super(Constructor, self).__init__()

        self.conv_1 = ConvBlock(64, 16, p=1)
        self.conv_2 = ConvBlock(64, 32, p=1)
        self.conv_3 = ConvBlock(64, 16, p=1)
        self.conv_4 = ConvBlock(16, 1, p=1)

    def forward(self, x, b_1, b_2) -> torch.Tensor:
        x = self.conv_1(x)
        x = torch.cat([x, b_1], dim=1)
        x = self.conv_2(x)
        x = torch.cat([x, b_2], dim=1)
        x = self.conv_3(x)
        x = self.conv_4(x)

        return x
    

class Extractor(nn.Module):
    def __init__(self):
        super(Extractor, self).__init__()

        # group S
        self.conv_1 = ConvBlock(1, 16, p=1)

        # group A
        self.conv_a1 = ConvBlock(16, 32, p=1)
        self.conv_a2 = ConvBlock(32, 48, p=1)
        self.conv_a3 = ConvBlock(48, 64, p=1)

        # group B
        self.conv_b1 = ConvBlock(16, 32, p=2, d=2)
        self.conv_b2 = ConvBlock(32, 48, p=1)
        self.conv_b3 = ConvBlock(48, 64, p=1)

        # group C
        self.conv_c1 = ConvBlock(16, 32, p=3, d=3)
        self.conv_c2 = ConvBlock(32, 48, p=1)
        self.conv_c3 = ConvBlock(48, 64, p=1)

    def forward(self, x):
        # group S
        x = self.conv_1(x)

        # group A
        a1 = self.conv_a1(x)
        a2 = self.conv_a2(a1)
        a3 = self.conv_a3(a2)

        # group B
        b1 = self.conv_b1(x)
        b2 = self.conv_b2(b1)
        b3 = self.conv_b3(b2)

        # group C
        c1 = self.conv_c1(x)
        c2 = self.conv_c2(c1)
        c3 = self.conv_c3(c2)

        # final feathers
        w_tp = [0.1, 0.1, 1]
        f = w_tp[0] * a3 + w_tp[1] * b3 + w_tp[2] * c3

        # transform block
        b_2 = a1 + b1 + c1
        b_1 = a2 + b2 + c2

        # pass
        return f, b_1, b_2
    

class ConvConv(nn.Module):
    def __init__(self, a_channels, b_channels, c_channels):
        super(ConvConv, self).__init__()

        self.conv_1 = nn.Conv2d(a_channels, b_channels, (3, 3), padding=(1, 1))
        self.relu = nn.ReLU()
        self.conv_2 = nn.Conv2d(b_channels, c_channels, (3, 3), padding=(2, 2), dilation=(2, 2))

    def forward(self, x):
        x = self.conv_1(x)
        x = self.relu(x)
        x = self.conv_2(x)
        return x


class EdgeDetect(nn.Module):
    def __init__(self):
        super(EdgeDetect, self).__init__()
        self.spatial = SpatialGradient('diff')
        self.max_pool = nn.MaxPool2d(3, 1, 1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        s = self.spatial(x)
        dx, dy = s[:, :, 0, :, :], s[:, :, 1, :, :]
        u = torch.sqrt(torch.pow(dx, 2) + torch.pow(dy, 2))
        y = self.max_pool(u)
        return y
    

class Attention(nn.Module):
    def __init__(self):
        super(Attention, self).__init__()

        self.conv_1 = ConvConv(1, 32, 32)
        self.conv_2 = ConvConv(32, 64, 128)
        self.conv_3 = ConvConv(128, 64, 32)
        self.conv_4 = nn.Conv2d(32, 1, (1, 1))

        self.ed = EdgeDetect()

    def forward(self, x):
        # edge detect
        e = self.ed(x)
        x = x + e

        # attention
        x = self.conv_1(x)
        x = self.conv_2(x)
        x = self.conv_3(x)
        x = self.conv_4(x)

        return x
    

class FeatherFuse(nn.Module):
    def __init__(self):
        super(FeatherFuse, self).__init__()

    @staticmethod
    def forward(ir_b: List[torch.Tensor], vi_b: List[torch.Tensor], mode='min-mean') -> List[torch.Tensor]:
        if len(ir_b) != 2 or len(vi_b) != 2:
            raise ValueError("ir_b and vi_b should contain exactly two tensors each.")
        b_1 = torch.min(ir_b[0], vi_b[0])
        b_2 = torch.min(ir_b[1], vi_b[1])
        b_3 = (ir_b[0] + vi_b[0] + b_1) / 3
        b_4 = (ir_b[1] + vi_b[1] + b_2) / 3
        if mode == 'min':
            return [b_1, b_2]
        elif mode == 'min-mean':
            return [b_3, b_4]
        else:
            raise ValueError(f"Unsupported mode: {mode}. Supported modes are 'min' and 'min-mean'.")