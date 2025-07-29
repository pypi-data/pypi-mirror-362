'''
Origin code: https://github.com/ZjjConan/SimAM/blob/master/networks/attentions/simam_module.py
Modified from: https://blog.csdn.net/weixin_43694096/article/details/138308819
'''
import torch
import torch.nn as nn

__all__ = ['SimAMBlock']

class SimAMBlock(torch.nn.Module):
    def __init__(self, channels=None, e_lambda=1e-4):
        super(SimAMBlock, self).__init__()

        self.activaton = nn.Sigmoid()
        self.e_lambda = e_lambda

    def forward(self, x):

        b, c, h, w = x.size()
        n = w * h - 1
        x_minus_mu_square = (x - x.mean(dim=[2, 3], keepdim=True)).pow(2)
        y = (
            x_minus_mu_square
            / (
                4
                * (x_minus_mu_square.sum(dim=[2, 3], keepdim=True) / n + self.e_lambda)
            )
            + 0.5
        )
        return x * self.activaton(y)


if __name__ == "__main__":
    input = torch.randn(64, 256, 8, 8)
    model = SimAMBlock(64)
    output = model(input)
    print(output.shape)

