from cslib.metrics.utils import fusion_preprocessing
import torch
import kornia

__all__ = [
    'te',
    'te_approach_loss',
    'te_metric'
]

def te(image1: torch.Tensor, image2: torch.Tensor,
    q: float = 1.85, bandwidth: float = 0.1, eps: float = 1e-12,
    normalize: bool = False) -> torch.Tensor:
    """
    Calculate the Tsallis entropy (TE) between two input images.

    Args:
        image1 (torch.Tensor): The first input image tensor.
        image2 (torch.Tensor): The second input image tensor.
        q (float, optional): The Tsallis entropy parameter. Default is 1.85.
        bandwidth (float, optional): Bandwidth for histogram smoothing. Default is 0.1.
        eps (float, optional): A small value to avoid numerical instability. Default is 1e-10.
        normalize (bool, optional): Whether to normalize input images. Default is False.

    Returns:
        torch.Tensor: The Tsallis entropy between the two input images.

    Reference:
        N. Cvejic, C. Canagarajah, D. Bull, Image fusion metric based on mutual
        information and tsallis entropy, Electron. Lett. 42 (11) (2006) 626-627.
    """
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

    temp = marginal_x.unsqueeze(1) * marginal_y.unsqueeze(2) # 转置并广播
    mask = (temp > 10*eps)
    result = torch.sum(hist[mask] ** q / (temp[mask]) ** (q-1))

    return (1-result)/(1-q)

# 两张图一样，平均梯度会相等
def te_approach_loss(A: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    return torch.abs(te(A,A)-te(A,F))

# 与 MEFB 统一
@fusion_preprocessing
def te_metric(A: torch.Tensor, B: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    w0 = w1 = 1 # MEFB里边没有除 2
    q=1.85;     # Cvejic's constant
    return w0 * te(A, F, q, normalize=False) + w1 * te(B, F, q, normalize=False)

if __name__ == '__main__':
    from cslib.metrics.fusion import vis,ir,fused
    print(te_metric(ir,vis,fused).item())
