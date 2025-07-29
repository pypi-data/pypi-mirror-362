from cslib.metrics.utils import fusion_preprocessing
from typing import Tuple
import torch
import kornia

__all__ = [
    'nmi',
    'nmi_approach_loss',
    'nmi_metric'
]

def _mi(image1: torch.Tensor, image2: torch.Tensor,
    bandwidth: float = 0.1, eps: float = 1e-10,
    normalize: bool = False) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
    # 将图片拉平成一维向量,将一维张量转换为二维张量
    if normalize == True:
        x1 = ((image1-torch.min(image1))/(torch.max(image1) - torch.min(image1))).view(1,-1) * 255
        x2 = ((image2-torch.min(image2))/(torch.max(image2) - torch.min(image2))).view(1,-1) * 255
    else:
        x1 = image1.view(1,-1) * 255
        x2 = image2.view(1,-1) * 255

    # 定义直方图的 bins
    bins = torch.linspace(0, 255, 256).to(image1.device)

    # 计算二维直方图
    hist = kornia.enhance.histogram2d(x1, x2, bins, bandwidth=torch.tensor(bandwidth))

    # 计算边缘分布
    marginal_x = torch.sum(hist, dim=2)
    marginal_y = torch.sum(hist, dim=1)

    # 计算互信息
    mask = (hist > eps)
    en_xy = -torch.sum(hist[mask] * torch.log2(hist[mask])) # MEFB里边用的 log2，不是 log(和 VIFB 相反! 服了)
    mask = (marginal_x != 0)
    en_x = -torch.sum(marginal_x[mask] * torch.log2(marginal_x[mask]))
    mask = (marginal_y != 0)
    en_y = -torch.sum(marginal_y[mask] * torch.log2(marginal_y[mask]))
    mi = en_x + en_y - en_xy

    return mi, en_xy, en_x, en_y

@fusion_preprocessing
def nmi(A: torch.Tensor, B: torch.Tensor, F: torch.Tensor,
    bandwidth: float = 0.1, eps: float = 1e-10, normalize: bool = False) -> torch.Tensor:
    """
    Calculate the Normalized Mutual Information (NMI) between two input images and their fusion.

    Args:
        A (torch.Tensor): The first input image tensor.
        B (torch.Tensor): The second input image tensor.
        F (torch.Tensor): The fused image tensor.
        bandwidth (float, optional): Bandwidth for histogram smoothing. Default is 0.1.
        eps (float, optional): A small value to avoid numerical instability. Default is 1e-10.
        normalize (bool, optional): Whether to normalize input images. Default is False.

    Returns:
        torch.Tensor: The NMI value between the two input images and their fusion.

    Reference:
        M. Hossny, S. Nahavandi, D. Creighton, Comments on `information measure for 
        performance of image fusion`, Electron. Lett. 44 (18) (2008) 1066-1067.
    """
    mi_AF, en_AF, en_A, en_F1 = _mi(A,F,bandwidth,eps,normalize)
    mi_BF, en_BF, en_B, en_F2 = _mi(B,F,bandwidth,eps,normalize)
    return 2*(mi_AF/(en_A+en_F1)+mi_BF/(en_B+en_F2))


def nmi_approach_loss(A: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    return -nmi(A,A,F)

# 与 MEFB 统一
nmi_metric = nmi

if __name__ == '__main__':
    from cslib.metrics.fusion import vis,ir,fused
    print(nmi_metric(ir,vis,fused).item())
