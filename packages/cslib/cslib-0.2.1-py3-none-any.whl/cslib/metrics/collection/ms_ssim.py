from cslib.metrics.utils import fusion_preprocessing
from cslib.algorithms.pytorch_msssim import ms_ssim as _ms_ssim
import torch

__all__ = [
    'ms_ssim',
    'ms_ssim_approach_loss',
    'ms_ssim_metric'
]

def ms_ssim(X: torch.Tensor, Y: torch.Tensor,
    data_range: int = 1, size_average: bool = False) -> torch.Tensor:
    """
    Calculate the Multi-Scale Structural Similarity Index (MS-SSIM) between two tensors.
    https://github.com/VainF/pytorch-msssim

    Args:
        X (torch.Tensor): The first input tensor.
        Y (torch.Tensor): The second input tensor.
        data_range (int, optional): The dynamic range of the input images (usually 1 or 255). Default is 1.
        size_average (bool, optional): If True, take the average of the SSIM index. Default is False.

    Returns:
        torch.Tensor: The MS-SSIM value between the two input tensors.

    Reference:
        Z. Wang, E. P. Simoncelli and A. C. Bovik, "Multiscale structural similarity for image quality assessment," 
        The Thrity-Seventh Asilomar Conference on Signals, Systems & Computers, 2003, Pacific Grove, CA, USA, 2003, 
        pp. 1398-1402 Vol.2, doi: 10.1109/ACSSC.2003.1292216.
    """
    return _ms_ssim(X, Y, data_range, size_average)

# https://github.com/VainF/pytorch-msssim
def ms_ssim_approach_loss(X: torch.Tensor, Y: torch.Tensor,
    data_range: int = 1, size_average: bool = False) -> torch.Tensor:
    return 1 - ms_ssim(X,Y,data_range,size_average)

@fusion_preprocessing
def ms_ssim_metric(A: torch.Tensor, B: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    w0 = w1 = 0.5
    return torch.mean(w0 * ms_ssim(A, F) + w1 * ms_ssim(B ,F))

if __name__ == '__main__':
    from cslib.metrics.fusion import ir,vis,fused

    print(f'MSSIM(ir,ir):{torch.mean(ms_ssim(ir,ir))}')
    print(f'MSSIM(ir,fused):{torch.mean(ms_ssim(ir,fused))}')
    print(f'MSSIM(vis,fused):{torch.mean(ms_ssim(vis,fused))}')
    print(ms_ssim_metric(ir,vis,fused).item()) 
