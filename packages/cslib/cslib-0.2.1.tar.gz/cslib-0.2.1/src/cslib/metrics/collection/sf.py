from cslib.metrics.utils import fusion_preprocessing
import torch
import kornia

__all__ = [
    'sf',
    'sf_approach_loss',
    'sf_metric'
]

def sf(tensor: torch.Tensor, eps: float = 1e-10) -> torch.Tensor:
    """
    Calculate the standard frequency of a tensor.

    Args:
        tensor (torch.Tensor): Input tensor, assumed to be in the range [0, 1].
        eps (float, optional): A small value to avoid numerical instability. Default is 1e-10.

    Returns:
        torch.Tensor: The standard frequency of the input tensor.

    Reference:
        [1] A. M. Eskicioglu and P. S. Fisher, "Image quality measures and their performance,"
        IEEE Transactions on communications, vol. 43, no. 12, pp. 2959-2965, 1995.
    """
    # 使用 Sobel 算子计算水平和垂直梯度 - Old
    grad_x = kornia.filters.filter2d(tensor,torch.tensor([[1,  -1]]).unsqueeze(0),padding='valid')
    grad_y = kornia.filters.filter2d(tensor,torch.tensor([[1],[-1]]).unsqueeze(0),padding='valid')

    # 计算梯度的幅度
    return torch.sqrt(torch.mean(grad_x**2) + torch.mean(grad_y**2) + eps)

# 如果两幅图相等，SF 会一致
def sf_approach_loss(A: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    return torch.abs(sf(A) - sf(F))

# 与 VIFB 统一
@fusion_preprocessing
def sf_metric(A: torch.Tensor, B: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    return sf(F) * 255.0  # 与 VIFB 统一，需要乘 255

if __name__ == '__main__':
    from cslib.metrics.fusion import vis,ir,fused
    print(sf_metric(ir,vis,fused).item())
    print(sf_metric(ir,vis.repeat(1, 3, 1, 1),fused.repeat(1, 3, 1, 1)).item())
    print(sf_metric(ir,vis.repeat(1, 3, 1, 1),fused).item())
