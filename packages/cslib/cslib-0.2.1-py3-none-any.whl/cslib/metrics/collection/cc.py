from cslib.metrics.utils import fusion_preprocessing
import torch
import numpy as np

__all__ = [
    'cc','cc_tang',
    'cc_approach_loss',
    'cc_metric'
]

def cc(A: torch.Tensor, B: torch.Tensor, eps: float = 1e-10) -> torch.Tensor:
    """
    Calculate the Correlation Coefficient (CC) between two input images.

    Args:
        A (torch.Tensor): The first input image tensor.
        B (torch.Tensor): The second input image tensor.
        eps (float, optional): A small value to avoid numerical instability. Default is 1e-10.

    Returns:
        torch.Tensor: The correlation coefficient value.
    
    Reference:
        [1] X. X. Zhu and R. Bamler, "A Sparse Image Fusion Algorithm With Application to 
            Pan-Sharpening," in IEEE Transactions on Geoscience and Remote Sensing, 
            vol. 51, no. 5, pp. 2827-2836, May 2013, doi: 10.1109/TGRS.2012.2213604.
    """
    [mA, mB] = [torch.mean(I) for I in [A, B]]
    rAB = torch.sum((A - mA) * (B - mB)) / torch.sqrt(eps + torch.sum((A - mA) ** 2) * torch.sum((B - mB) ** 2))
    return torch.mean(rAB)

def cc_tang(A: np.ndarray, B: np.ndarray, F: np.ndarray) -> float:
    """
    Compute the correlation coefficient between two variables A and B with respect to a third variable F.

    Parameters:
    - A (numpy.ndarray): Array representing variable A.
    - B (numpy.ndarray): Array representing variable B.
    - F (numpy.ndarray): Array representing variable F.

    Returns:
    - float: Correlation coefficient between A and F (rAF) and between B and F (rBF), averaged to get the final correlation coefficient (CC).

    Author: Linfeng Tang
    Reference: https://zhuanlan.zhihu.com/p/611295921

    This function calculates the correlation coefficients rAF and rBF between variables A and F, and B and F, respectively.
    It then computes the average of these coefficients to obtain the overall correlation coefficient (CC).

    The formula used for correlation coefficient calculation is based on the Pearson correlation coefficient formula.
    """
    # Calculate mean values for A, B, and F
    mean_A = np.mean(A)
    mean_B = np.mean(B)
    mean_F = np.mean(F)

    # Calculate correlation coefficients rAF and rBF
    rAF = np.sum((A - mean_A) * (F - mean_F)) / np.sqrt(np.sum((A - mean_A) ** 2) * np.sum((F - mean_F) ** 2))
    rBF = np.sum((B - mean_B) * (F - mean_F)) / np.sqrt(np.sum((B - mean_B) ** 2) * np.sum((F - mean_F) ** 2))

    # Calculate the average correlation coefficient CC
    return float(np.mean([rAF, rBF]))

def cc_approach_loss(A: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    return cc_metric(A,A,A) - cc_metric(A,A,F)

# 与 Tang 统一
@fusion_preprocessing
def cc_metric(A: torch.Tensor, B: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    '''
    Reference:
        [1] Luo, Y.; Luo, Z. Infrared and Visible Image Fusion: Methods, Datasets, Applications, 
            and Prospects. Appl. Sci. 2023, 13, 10891. https://doi.org/10.3390/app131910891
    '''
    w0 = w1 = 0.5
    return w0 * cc(A,F) + w1 * cc(B,F)

if __name__ == '__main__':
    from cslib.metrics.fusion import ir,vis,fused
    from cslib.utils import to_numpy
    [ir_arr, vis_arr, fused_arr] = [to_numpy(i) for i in [ir, vis, fused]]

    print(f'CC(ir,fused):{cc(ir,fused)}')
    print(f'CC(vis,fused):{cc(vis,fused)}')
    print(f'CC(ir,vis,fused) by Charles:{cc_metric(ir,vis,fused)}')
    print(f'CC(ir,vis,fused) by Tang   :{cc_tang(ir_arr,vis_arr,fused_arr)}')
