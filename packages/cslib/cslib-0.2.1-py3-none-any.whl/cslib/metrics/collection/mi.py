from cslib.metrics.utils import fusion_preprocessing
import torch
import kornia
from sklearn.metrics.cluster import mutual_info_score as mi_sklearn

__all__ = [
    'mi','mi_sklearn',
    'mi_approach_loss',
    'mi_metric'
]

def mi(image1: torch.Tensor, image2: torch.Tensor, bandwidth: float = 0.1, eps: float = 1e-10, normalize: bool = False) -> torch.Tensor:
    """
    Calculate the differentiable mutual information between two images.

    Args:
        image1 (torch.Tensor): The first input image tensor.
        image2 (torch.Tensor): The second input image tensor.
        bandwidth (float, optional): Bandwidth for histogram smoothing. Default is 0.25.
        eps (float, optional): A small value to avoid numerical instability. Default is 1e-10.
        normalize (bool, optional): Whether to normalize the pixel values of the images. Default is False.

    Returns:
        torch.Tensor: The differentiable mutual information between the two images.

    Reference:
        [1] G. Qu, D. Zhang, and P. Yan, "Information measure for performance of image fusion,"
        Electronics letters, vol. 38, no. 7, pp. 313-315, 2002.
    """
    # 将图片拉平成一维向量,将一维张量转换为二维张量
    if normalize == True:
        x1 = ((image1-torch.min(image1))/(torch.max(image1) - torch.min(image1))).view(1,-1) * 255.0
        x2 = ((image2-torch.min(image2))/(torch.max(image2) - torch.min(image2))).view(1,-1) * 255.0
    else:
        x1 = image1.view(1,-1) * 255.0
        x2 = image2.view(1,-1) * 255.0

    # 定义直方图的 bins
    bins = torch.linspace(0, 255, 256).to(image1.device)

    # 计算二维直方图
    hist = kornia.enhance.histogram2d(x1, x2, bins, bandwidth=torch.tensor(bandwidth))

    # 计算边缘分布
    marginal_x = torch.sum(hist, dim=2)
    marginal_y = torch.sum(hist, dim=1)

    # 计算互信息
    mask = (hist > eps)
    en_xy = -torch.sum(hist[mask] * torch.log(hist[mask])) # VIFB里边用的 log，不是 log2
    mask = (marginal_x != 0)
    en_x = -torch.sum(marginal_x[mask] * torch.log(marginal_x[mask]))
    mask = (marginal_y != 0)
    en_y = -torch.sum(marginal_y[mask] * torch.log(marginal_y[mask]))

    return en_x + en_y - en_xy

# 内容相同时互信息最大，采用 1减比值的方法把损失做到 0-1 之间
def mi_approach_loss(A: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    return torch.abs(1 - mi(A,F) / mi(A,A))

# 与调整过的 VIFB 统一（传入的图片未进行normalize）
@fusion_preprocessing
def mi_metric(A: torch.Tensor, B: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    w0 = w1 = 1 # MEFB里边没有除 2
    res = w0 * mi(A,F) + w1 * mi(B,F)
    return res

if __name__ == '__main__':
    from cslib.metrics.fusion import vis,ir,fused
    print(mi_metric(ir,vis,fused).item())
    print(mi_metric(ir,vis.repeat(1, 3, 1, 1),fused.repeat(1, 3, 1, 1)).item())
    print(mi_metric(ir,vis.repeat(1, 3, 1, 1),fused).item())