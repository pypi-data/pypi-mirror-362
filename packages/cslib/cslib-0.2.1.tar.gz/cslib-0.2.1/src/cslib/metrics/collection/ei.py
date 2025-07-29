from cslib.metrics.utils import fusion_preprocessing
import torch
import kornia

__all__ = [
    'ei',
    'ei_approach_loss',
    'ei_metric'
]

def ei(tensor: torch.Tensor, border_type: str = 'replicate', eps: float = 1e-10) -> torch.Tensor:
    """
    Calculate the edge intensity (EI) of a tensor using Sobel operators.

    Args:
        tensor (torch.Tensor): Input tensor, assumed to be in the range [0, 1].
        border_type (str, optional): Type of border extension. Default is 'replicate'.
        eps (float, optional): A small value to avoid numerical instability. Default is 1e-10.

    Returns:
        torch.Tensor: The edge intensity of the input tensor.

    Reference:
        [1] B. Rajalingam and R. Priya, "Hybrid multimodality medical image fusion
        technique for feature enhancement in medical diagnosis," International Journal
        of Engineering Science Invention, 2018.
    """
    # 使用Sobel算子计算水平和垂直梯度
    grad_x = kornia.filters.filter2d(tensor,torch.tensor([[[ 1,  2,  1],[ 0,  0,  0],[-1, -2, -1]]]),border_type=border_type)
    grad_y = kornia.filters.filter2d(tensor,torch.tensor([[[ 1,  0, -1],[ 2,  0, -2],[ 1,  0, -1]]]),border_type=border_type)

    # 计算梯度的幅度
    s = torch.sqrt(grad_x ** 2 + grad_y ** 2 + eps)

    # 返回 EI 值
    return torch.mean(s)

# 如果两幅图相等，EI 会一致
def ei_approach_loss(A: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    return torch.abs(ei(A) - ei(F))

# 与 VIFB 统一
@fusion_preprocessing
def ei_metric(A: torch.Tensor, B: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    return ei(F) * 255  # 与 VIFB 统一，需要乘 255

if __name__ == '__main__':
    from cslib.metrics.fusion import ir,vis,fused

    print(ei_metric(ir,vis,fused).item()) 