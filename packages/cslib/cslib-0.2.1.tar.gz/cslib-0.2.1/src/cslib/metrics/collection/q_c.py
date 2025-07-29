from cslib.metrics.utils import fusion_preprocessing
import torch
import kornia

__all__ = [
    'q_c',
    'q_c_approach_loss',
    'q_c_metric'
]

def q_c(A: torch.Tensor, B: torch.Tensor, F: torch.Tensor,
        window_size: int = 7, eps: float = 1e-10) -> torch.Tensor:
    """
    Calculate the Q_C quality index for image fusion.

    Args:
        A (torch.Tensor): The first input image tensor.
        B (torch.Tensor): The second input image tensor.
        F (torch.Tensor): The fused image tensor.
        window_size (int, optional): The size of the Gaussian kernel for filtering. Default is 7.
        eps (float, optional): A small value to avoid numerical instability. Default is 1e-10.

    Returns:
        torch.Tensor: The Q_C quality index between the two input images and their fusion.

    Reference:
        [1] Metric for multimodal image sensor fusion, Electronics Letters, 43 (2) 2007 
        [2] N. Cvejic, A. Loza, D. Bull, N. Canagarajah, A similarity metric for assessment of image fusion 
        algorithms, Int. J. Signal Process. 2 (3) (2005) 178-182.
    """
    def ssim_yang(A,B): # SSIM_Yang
        C1 = 2e-16
        C2 = 2e-16
        kernel = kornia.filters.get_gaussian_kernel1d(window_size, 1.5, device=A.device, dtype=A.dtype)
        muA = kornia.filters.filter2d_separable(A, kernel, kernel, padding="valid")
        muB = kornia.filters.filter2d_separable(B, kernel, kernel, padding="valid")
        sAA = kornia.filters.filter2d_separable(A**2, kernel, kernel, padding="valid") - muA**2
        sBB = kornia.filters.filter2d_separable(B**2, kernel, kernel, padding="valid") - muB**2
        sAB = kornia.filters.filter2d_separable(A*B, kernel, kernel, padding="valid") - muA*muB
        ssim_map = ((2*muA*muB + C1)*(2*sAB + C2)) / ((muA**2 + muB**2 + C1)*(sAA + sBB + C2)+eps)
        return (ssim_map,sAB)

    (ssimAF, SAF) = ssim_yang(A*255, F*255)
    (ssimBF, SBF) = ssim_yang(B*255, F*255)
    ssimABF = SAF / (SAF+SBF+eps)
    Q_C = ssimABF*ssimAF + (1-ssimABF)*ssimBF
    Q_C[ssimABF>1] = 1
    Q_C[ssimABF<0] = 0
    return torch.mean(Q_C)

def q_c_approach_loss(A: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    return 1-q_c(A, A, F, window_size=7)

# 与 OE 保持一致
@fusion_preprocessing
def q_c_metric(A: torch.Tensor, B: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    return q_c(A, B, F, window_size=7)

if __name__ == '__main__':
    from cslib.metrics.fusion import vis,ir,fused
    print(q_c_metric(ir,vis,fused).item()) # should be 0.7187
