from cslib.metrics.utils import fusion_preprocessing
import torch

__all__ = [
    'sd',
    'sd_approach_loss',
    'sd_metric'
]

def sd(tensor: torch.Tensor) -> torch.Tensor:
    """
    Calculate the standard deviation of a tensor.

    Args:
        tensor (torch.Tensor): Input tensor, assumed to be in the range [0, 1].

    Returns:
        torch.Tensor: The standard deviation of the input tensor.

    Reference:
        [1] Y.-J. Rao, "In-fibre bragg grating sensors," Measurement science and technology,
        vol. 8, no. 4, p. 355, 1997.
    """
    return torch.sqrt(torch.mean((tensor - tensor.mean())**2))

# 如果两幅图相等，SD 会一致
def sd_approach_loss(A: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    return torch.abs(sd(A) - sd(F))

# 与 VIFB 统一
@fusion_preprocessing
def sd_metric(A: torch.Tensor, B: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    return sd(F) * 255.0  # 与 VIFB 统一，需要乘 255

if __name__ == '__main__':
    from cslib.metrics.fusion import vis,ir,fused
    print(sd_metric(ir,vis,fused).item())
    print(sd_metric(ir,vis.repeat(1, 3, 1, 1),fused.repeat(1, 3, 1, 1)).item())
    print(sd_metric(ir,vis.repeat(1, 3, 1, 1),fused).item())
