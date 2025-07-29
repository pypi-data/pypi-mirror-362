from cslib.metrics.utils import fusion_preprocessing
import torch
import kornia

__all__ = [
    'q_y',
    'q_y_approach_loss',
    'q_y_metric'
]

def q_y(A: torch.Tensor, B: torch.Tensor, F: torch.Tensor,
        window_size: int = 7, eps: float = 1e-10) -> torch.Tensor:
    """
    Calculate the Q_Y quality index for image fusion.

    Args:
        A (torch.Tensor): The first input image tensor.
        B (torch.Tensor): The second input image tensor.
        F (torch.Tensor): The fused image tensor.
        window_size (int, optional): The size of the Gaussian kernel for filtering. Default is 7.
        eps (float, optional): A small value to avoid numerical instability. Default is 1e-10.

    Returns:
        torch.Tensor: The Q_Y quality index between the two input images and their fusion.

    Reference:
        C. Yang, J.-Q. Zhang, X.-R. Wang, X. Liu, A novel similarity based quality metric for 
        image fusion, Inf. Fusion 9 (2) (2008) 156-160.
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
        return (ssim_map,sAA,sBB)

    (ssimAB, SAA, SBB) = ssim_yang(A*255, B*255)
    (ssimAF, _, _) = ssim_yang(A*255, F*255)
    (ssimBF, _, _) = ssim_yang(B*255, F*255)

    ramda=SAA/(SAA+SBB+eps)

    Q1 = (ramda*ssimAF + (1-ramda)*ssimBF)[(ssimAB>=0.75) * ((SAA+SBB)>eps)]
    Q2 = torch.max(ssimAF,ssimBF)[(ssimAB<0.75) * ((SAA+SBB)>eps)]

    return (torch.sum(Q1)+torch.sum(Q2)) / (Q1.shape[0]+Q2.shape[0]) # 为了和 MEFB 统一，改变了平均的方式

def q_y_approach_loss(A: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    return 1-q_y(A, A, F, window_size=7, eps=1e-10)

@fusion_preprocessing
def q_y_metric(A: torch.Tensor, B: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    return q_y(A, B, F, window_size=7, eps=1e-10)

if __name__ == '__main__':
    from cslib.metrics.fusion import vis,ir,fused
    print(q_y_metric(ir,vis,fused).item())
