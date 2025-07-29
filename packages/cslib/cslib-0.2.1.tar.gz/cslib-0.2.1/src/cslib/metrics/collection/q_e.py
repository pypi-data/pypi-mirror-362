from cslib.metrics.utils import fusion_preprocessing
import torch
import kornia

__all__ = [
    'q_e',
    'q_e_approach_loss',
    'q_e_metric'
]

def q_e(A: torch.Tensor, B: torch.Tensor, F: torch.Tensor,
        window_size: int = 11, eps: float = 1e-10) -> torch.Tensor:
    """
    Calculate the Peilla's quality index (q_e) for image fusion.
    It's also called EFQI metric.

    Args:
        A (torch.Tensor): The first input image tensor.
        B (torch.Tensor): The second input image tensor.
        F (torch.Tensor): The fused image tensor.
        window_size (int, optional): The size of the Gaussian kernel for filtering. Default is 11.
        eps (float, optional): A small value to avoid numerical instability. Default is 1e-10.

    Returns:
        torch.Tensor: The q_w quality index between the two input images and their fusion.

    Reference:
        G. Piella and H. Heijmans, "A new quality metric for image fusion," Proceedings 
        2003 International Conference on Image Processing (Cat. No.03CH37429), 
        Barcelona, Spain, 2003, pp. III-173, doi: 10.1109/ICIP.2003.1247209.
    """
    def modify(A):
        X = kornia.filters.filter2d(A*255,torch.tensor([[[1,0,-1],[1,0,-1],[ 1, 0,-1]]]),border_type='constant')
        Y = kornia.filters.filter2d(A*255,torch.tensor([[[1,1, 1],[0,0, 0],[-1,-1,-1]]]),border_type='constant')
        return torch.sqrt(X**2 + Y**2 + eps)
    [A, B, F] = [modify(i) for i in [A, B, F]]

    def sigma2(A):
        kernel = kornia.filters.get_gaussian_kernel1d(window_size, 1.5, device=A.device, dtype=A.dtype)
        mu = kornia.filters.filter2d_separable(A, kernel, kernel, padding="valid")
        mu2 = kornia.filters.filter2d_separable(A**2, kernel, kernel, padding="valid")
        return mu2 - mu**2

    def _ssim(A,B):
        C1 = (0.01*255)**2
        C2 = (0.03*255)**2
        kernel = kornia.filters.get_gaussian_kernel1d(window_size, 1.5, device=A.device, dtype=A.dtype)
        muA = kornia.filters.filter2d_separable(A, kernel, kernel, padding="valid")
        muB = kornia.filters.filter2d_separable(B, kernel, kernel, padding="valid")
        sAA = kornia.filters.filter2d_separable(A**2, kernel, kernel, padding="valid") - muA**2
        sBB = kornia.filters.filter2d_separable(B**2, kernel, kernel, padding="valid") - muB**2
        sAB = kornia.filters.filter2d_separable(A*B, kernel, kernel, padding="valid") - muA*muB

        return  ((2*muA*muB + C1)*(2*sAB + C2)) / ((muA**2 + muB**2 + C1)*(sAA + sBB + C2));

    sigma2A_sq = sigma2(A)
    sigma2B_sq = sigma2(B)

    rectify = ((sigma2A_sq + sigma2B_sq) < eps).float() * 0.5
    sigma2A_sq = sigma2A_sq + rectify
    sigma2B_sq = sigma2B_sq + rectify
    ramda = sigma2A_sq / (sigma2A_sq + sigma2B_sq)

    ssimAF = _ssim(A, F)
    ssimBF = _ssim(B, F)

    sigmaMax = torch.max(sigma2A_sq, sigma2B_sq)
    sigmaMax = sigmaMax / torch.sum(sigmaMax)

    return torch.sum(sigmaMax * (ramda*ssimAF + (1-ramda)*ssimBF))

def q_e_approach_loss(A: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    return 1-q_e(A, A, F, window_size=11, eps=1e-10)

# 与 OE 保持一致
@fusion_preprocessing
def q_e_metric(A: torch.Tensor, B: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    return q_e(A, B, F, window_size=11, eps=1e-10)

if __name__ == '__main__':
    from cslib.metrics.fusion import vis,ir,fused
    print(q_e_metric(ir,vis,fused).item()) # should be 0.7662
