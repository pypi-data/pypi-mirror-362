from cslib.metrics.utils import fusion_preprocessing
from typing import Tuple
import torch
import kornia

__all__ = [
    'n_abf',
    'n_abf_approach_loss',
    'n_abf_metric'
]

def _sobel_fn(I: torch.Tensor, border_type: str = 'reflect') -> Tuple[torch.Tensor, torch.Tensor]:
    grad_y = kornia.filters.filter2d(I,torch.tensor([[[-1, -2, -1],[ 0,  0,  0],[ 1,  2,  1]]]),border_type=border_type)
    grad_x = kornia.filters.filter2d(I,torch.tensor([[[-1,  0,  1],[-2,  0,  2],[-1,  0,  1]]]),border_type=border_type)
    return (grad_x/8.0, grad_y/8.0)

def n_abf(A: torch.Tensor, B: torch.Tensor, F: torch.Tensor,
    Td: float = 2.0, wt_min: float = 0.001, P: int = 1, Lg: float = 1.5,
           Nrg: float = 0.9999, kg: int = 19, sigmag: float = 0.5,
           Nra: float = 0.9995, ka: int = 22, sigmaa: float = 0.5,
           eps: float = 1e-10) -> torch.Tensor:
    """
    Calculate the NABF (No-reference assessment based on blur and noise factors) metric between images A, B, and F.

    Args:
        A (torch.Tensor): Input image A.
        B (torch.Tensor): Input image B.
        F (torch.Tensor): Fused image F.
        Td (float): Threshold for edge strength. Defaults to 2.0.
        wt_min (float): Minimum weight. Defaults to 0.001.
        P (int): Not used. Defaults to 1.
        Lg (float): Edge preservation exponent. Defaults to 1.5.
        Nrg (float): Edge preservation coefficient for gradient. Defaults to 0.9999.
        kg (int): Edge preservation coefficient for gradient. Defaults to 19.
        sigmag (float): Edge preservation parameter for gradient. Defaults to 0.5.
        Nra (float): Edge preservation coefficient for orientation. Defaults to 0.9995.
        ka (int): Edge preservation coefficient for orientation. Defaults to 22.
        sigmaa (float): Edge preservation parameter for orientation. Defaults to 0.5.
        eps (float): Small value for numerical stability. Defaults to 1e-10.

    Returns:
        torch.Tensor: NABF metric value.
    
    Reference:
        Modified Fusion Artifacts measure proposed by B. K. Shreyamsha Kumar
        https://github.com/Linfeng-Tang/Image-Fusion/blob/main/General%20Evaluation%20Metric/Evaluation/analysis_nabf.m
    """
    # Edge Strength & Orientation
    gvA, ghA = _sobel_fn(A)
    gA = torch.sqrt(ghA.pow(2) + gvA.pow(2) + eps)

    gvB, ghB = _sobel_fn(B)
    gB = torch.sqrt(ghB.pow(2) + gvB.pow(2) + eps)

    gvF, ghF = _sobel_fn(F)
    gF = torch.sqrt(ghF.pow(2) + gvF.pow(2) + eps)

    # Relative Edge Strength & Orientation
    gAF = torch.where(gA*gF < eps, torch.zeros_like(gA), torch.min(gF / gA, gA / gF))
    gBF = torch.where(gB*gF < eps, torch.zeros_like(gB), torch.min(gF / gB, gB / gF))
    aA = torch.atan(gvA/(ghA+eps)) # 不能用 tan2，因为 matlab 里边的 atan 值域在-2/pi 到 2/pi。。
    aB = torch.atan(gvB/(ghB+eps))
    aF = torch.atan(gvF/(ghF+eps))
    aAF = torch.abs(torch.abs(aA - aF) - torch.tensor([0.5 * torch.pi],device=aA.device)).mul(2.0 / torch.pi)
    aBF = torch.abs(torch.abs(aB - aF) - torch.tensor([0.5 * torch.pi],device=aA.device)).mul(2.0 / torch.pi)

    # Edge Preservation Coefficient
    QgAF = Nrg / (1 + torch.exp(-kg * (gAF - sigmag)))
    QaAF = Nra / (1 + torch.exp(-ka * (aAF - sigmaa)))
    QAF = torch.sqrt(QgAF * QaAF + eps)
    QgBF = Nrg / (1 + torch.exp(-kg * (gBF - sigmag)))
    QaBF = Nra / (1 + torch.exp(-ka * (aBF - sigmaa)))
    QBF = torch.sqrt(QgBF * QaBF + eps)

    # Total Fusion Performance (QABF)
    wtA = torch.where(gA >= Td, gA**Lg, wt_min * torch.ones_like(gA))
    wtB = torch.where(gB >= Td, gB**Lg, wt_min * torch.ones_like(gB))
    wt_sum = torch.sum(wtA + wtB)
    QAF_wtsum = torch.sum(QAF * wtA) / wt_sum
    QBF_wtsum = torch.sum(QBF * wtB) / wt_sum
    QABF = QAF_wtsum + QBF_wtsum

    # Fusion Loss (LABF)
    rr = torch.where((gF <= gA) | (gF <= gB), torch.ones_like(gF), torch.zeros_like(gF))
    LABF = torch.sum(rr * ((1 - QAF) * wtA + (1 - QBF) * wtB)) / wt_sum

    # Fusion Artifacts (NABF) changed by B. K. Shreyamsha Kumar
    na = torch.where((gF > gA) & (gF > gB), torch.ones_like(gF), torch.zeros_like(gF))
    NABF = torch.sum(na * ((1 - QAF) * wtA + (1 - QBF) * wtB)) / wt_sum

    return NABF

def n_abf_approach_loss(A: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    return n_abf(A, A, F)

# 和 matlab 保持一致
@fusion_preprocessing
def n_abf_metric(A: torch.Tensor, B: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    return n_abf(A*255.0, B*255.0, F*255.0)

if __name__ == '__main__':
    from cslib.metrics.fusion import ir,vis,fused,densefuse

    print(f'N_ABF(vis,vis,vis):{n_abf_metric(vis,vis,vis)}')
    print(f'N_ABF(vis,vis,fused):{n_abf_metric(vis,vis,fused)}')
    print(f'N_ABF(vis,vis,ir):{n_abf_metric(vis,vis,ir)}')
    print(f'N_ABF(vis,ir,fused):{n_abf_metric(vis,ir,fused)}') # should be 0.0159
    print(f'N_ABF(vis,ir,fused2):{n_abf_metric(vis,ir,densefuse)}')
