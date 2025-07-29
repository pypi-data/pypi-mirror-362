from cslib.metrics.utils import fusion_preprocessing
import torch

__all__ = [
    'snr',
    'snr_metric'
]

def snr(A: torch.Tensor, B: torch.Tensor, F: torch.Tensor, eps: float = 1e-10) -> torch.Tensor:
    """
    Calculate the Signal-to-Noise Ratio (SNR) for image fusion.

    Args:
        A (torch.Tensor): The first input image tensor.
        B (torch.Tensor): The second input image tensor.
        F (torch.Tensor): The fused image tensor.
        eps (float, optional): A small value to avoid numerical instability. Default is 1e-10.

    Returns:
        torch.Tensor: The SNR value for the fused image.
    
    Reference:
        Yuhendra, et al. “Assessment of Pan-Sharpening Methods Applied to Image Fusion of 
        Remotely Sensed Multi-Band Data.” International Journal of Applied Earth Observation 
        and Geoinformation, Aug. 2012, pp. 165-75, https://doi.org/10.1016/j.jag.2012.01.013.
    """
    # 计算信号部分与噪声部分
    signal = torch.sum(A**2) + torch.sum(B**2)
    noise = torch.sum((A - F)**2) + torch.sum((B - F)**2)

    # 计算SNR值，防止MSE为零
    return 10 * torch.log10( signal / (noise + eps))

# 两张图完全一样，SNR 是无穷大
def snr_approach_loss(A: torch.Tensor, B: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    return -snr(A, B, F)

@fusion_preprocessing
def snr_metric(A: torch.Tensor, B: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    # print(snr(A*255, B*255, F*255),snr(A, B, F)) # 结果一样，所以简化计算可以不乘 255
    return snr(A, B, F)

if __name__ == '__main__':
    from cslib.metrics.fusion import vis,ir,fused
    print(snr_metric(ir,vis,fused).item())
    print(snr_metric(ir,ir,ir).item())
    print(snr_metric(vis,vis,vis).item())
