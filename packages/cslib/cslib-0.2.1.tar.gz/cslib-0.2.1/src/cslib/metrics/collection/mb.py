from cslib.metrics.utils import fusion_preprocessing
import torch

__all__ = [
    'mb',
    'mb_approach_loss',
    'mb_metric'
]

def mb(R: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    """
    Calculate the mean bias (MB).

    Args:
        R (torch.Tensor): Input tensor Reference Image.
        F (torch.Tensor): Input tensor Fused.

    Returns:
        torch.Tensor: The mean bias of the input tensors.

    Reference:
        P. Jagalingam, Arkal Vittal Hegde, A Review of Quality 
        Metrics for Fused Image, Aquatic Procedia, Volume 4,
        2015, Pages 133-142, ISSN 2214-241X, 
        https://doi.org/10.1016/j.aqpro.2015.02.019.
    """

    [mR, mF] = [torch.mean(I) for I in [R, F]]

    return torch.abs(1-mF/mR) # 我加的绝对值

# 如果两幅图相等，MB 会一致
def mb_approach_loss(A: torch.Tensor, B: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    return mb(A, F) + mb(B, F)

@fusion_preprocessing
def mb_metric(A: torch.Tensor, B: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    '''
        Remote sensing fusion: only use MS image !!!!
        Infared visiable fusion: weighted (self defined)
    '''
    w1 = w2 = 0.5
    return w1*mb(A,F) + w2*mb(B,F) # 不乘 255 也一样

if __name__ == '__main__':
    from cslib.metrics.fusion import vis,ir,fused
    print(mb_metric(ir,vis,fused).item())
