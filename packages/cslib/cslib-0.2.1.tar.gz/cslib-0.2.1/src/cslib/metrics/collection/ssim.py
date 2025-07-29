from cslib.metrics.utils import fusion_preprocessing
import kornia
import torch

###########################################################################################

__all__ = [
    'ssim',
    'ssim_approach_loss',
    'ssim_metric'
]

"""
Calculate the Structural Similarity Index (SSIM) between two images.

Args:
    img1 (torch.Tensor): The first input image tensor.
    img2 (torch.Tensor): The second input image tensor.
    window_size (int): The size of the sliding window for SSIM calculation.
    max_val (float, optional): The maximum value of the input images. Default is 1.0.
    eps (float, optional): Small constant to avoid division by zero. Default is 1e-12.
    padding (str, optional): Padding mode for the convolution. Default is 'same'.

Returns:
    torch.Tensor: The SSIM index between the two input images.

Reference:
    [1] Z. Wang, A. C. Bovik, H. R. Sheikh, E. P. Simoncelli et al., "Image quality assessment: from error visibility
    to structural similarity," IEEE transactions on image processing, vol. 13, no. 4, pp. 600-612, 2004.
    [2] Document: https://kornia.readthedocs.io/en/latest/metrics.html#kornia.metrics.ssim
"""
ssim = kornia.metrics.ssim

# https://kornia.readthedocs.io/en/latest/losses.html#kornia.losses.ssim_loss
def ssim_approach_loss(A: torch.Tensor, F: torch.Tensor,
    window_size: int = 11, max_val: float = 1.0,
    eps: float = 1e-12, reduction: str = 'mean', padding: str = 'same') -> torch.Tensor:
    return kornia.losses.ssim_loss(A, F, window_size, max_val, eps, reduction, padding)

# 与 VIFB 统一
@fusion_preprocessing
def ssim_metric(A: torch.Tensor, B: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    w0 = w1 = 0.5 # VIFB 忘了除二
    return torch.mean(w0 * ssim(A, F,window_size=11) + w1 * ssim(B ,F,window_size=11)) # 论文的窗大小就是 11

if __name__ == '__main__':
    from cslib.metrics.fusion import vis,ir,fused
    print(ssim_metric(ir,vis,fused).item())
    print(ssim_metric(ir,vis.repeat(1, 3, 1, 1),fused.repeat(1, 3, 1, 1)).item())
    print(ssim_metric(ir,vis.repeat(1, 3, 1, 1),fused).item())
