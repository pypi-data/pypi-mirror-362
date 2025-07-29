from cslib.metrics.utils import fusion_preprocessing
import torch

__all__ = [
    'd',
    'd_approach_loss',
    'd_metric'
]

def d(I: torch.Tensor, F: torch.Tensor, eps: float = 1e-10) -> torch.Tensor:
    """
    Calculate the degree of distortion (D) between two images.

    Args:
        I (torch.Tensor): The reference image tensor.
        F (torch.Tensor): The fused image tensor.
        eps (float, optional): A small value to avoid numerical instability. Default is 1e-10.

    Returns:
        torch.Tensor: The PFE between fused and reference values.

    Reference:
        X. X. Zhu and R. Bamler, "A Sparse Image Fusion Algorithm With Application 
        to Pan-Sharpening," in IEEE Transactions on Geoscience and Remote Sensing, 
        vol. 51, no. 5, pp. 2827-2836, May 2013, doi: 10.1109/TGRS.2012.2213604.
    """
    D = torch.abs(I - F + eps)
    return torch.sum(D) / (I.shape[-2] * I.shape[-1])

d_approach_loss = d

@fusion_preprocessing
def d_metric(A: torch.Tensor, B: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    w0 = w1 = 0.5
    return w0 * d(A, F) + w1 * d(B, F)

if __name__ == '__main__':
    from cslib.metrics.fusion import ir,vis,fused
    print(f'D(ir,ir):{d(ir,ir)}')
    print(f'D(ir,fused):{d(ir,fused)}')
    print(f'D(ir,vis):{d(ir,vis)}')
    print(f'D metrics:{d_metric(ir,vis,fused)}')
