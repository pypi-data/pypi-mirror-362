from cslib.metrics.utils import fusion_preprocessing
import torch
import kornia

__all__ = [
    'ag',
    'ag_approach_loss',
    'ag_metric'
]


def ag(tensor: torch.Tensor, eps: float = 1e-10) -> torch.Tensor:
    """
    Calculate the average gradient (AG) of a grayscale image.

    Args:
        tensor (torch.Tensor): Input tensor, assumed to be in the range [0, 1].
        eps (float, optional): A small value to avoid numerical instability. Default is 1e-10.

    Returns:
        torch.Tensor: The average gradient of the input tensor.

    Reference:
        [1] G. Cui, H. Feng, Z. Xu, Q. Li, and Y. Chen, "Detail preserved fusion of visible
        and infrared images using regional saliency extraction and multi-scale image
        decomposition," Optics Communications, vol. 341, pp. 199-209, 2015.
    """
    # 使用Sobel算子计算水平和垂直梯度
    _gx = kornia.filters.filter2d(tensor,torch.tensor([[[-1,  1]]]))
    _gy = kornia.filters.filter2d(tensor,torch.tensor([[[-1],[1]]]))

    # 对梯度进行平均以避免过度敏感性(与 Matlab 统一)
    gx = (torch.cat((_gx[...,0:1],_gx[...,:-1]),dim=-1)+torch.cat((_gx[...,:-1],_gx[...,-2:-1]),dim=-1))/2
    gy = (torch.cat((_gy[:,:,0:1,:],_gy[:,:,:-1,:]),dim=-2)+torch.cat((_gy[:,:,:-1,:],_gy[:,:,-2:-1,:]),dim=-2))/2

    # 计算梯度的平均幅度
    s = torch.sqrt((gx ** 2 + gy ** 2 + eps)/2)

    # 返回 AG 值
    return torch.sum(s) / ((tensor.shape[2] - 1) * (tensor.shape[3] - 1))

# 两张图一样，平均梯度会相等
def ag_approach_loss(A: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    return torch.abs(ag(A) - ag(F))

# 与 VIFB 统一
@fusion_preprocessing
def ag_metric(A: torch.Tensor, B: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    return ag(F) * 255.0  # 与 VIFB 统一，需要乘 255

if __name__ == '__main__':
    from cslib.metrics.fusion import vis,ir,fused
    print(ag_metric(ir,vis,fused).item())
    print(ag_metric(ir,vis.repeat(1, 3, 1, 1),fused.repeat(1, 3, 1, 1)).item())
    print(ag_metric(ir,vis.repeat(1, 3, 1, 1),fused).item())