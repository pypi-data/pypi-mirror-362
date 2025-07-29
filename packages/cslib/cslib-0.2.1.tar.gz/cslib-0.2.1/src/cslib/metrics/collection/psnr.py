from cslib.metrics.utils import fusion_preprocessing
import torch

__all__ = [
    'psnr',
    'psnr_approach_loss',
    'psnr_metric'
]

def psnr(A: torch.Tensor, B: torch.Tensor, F: torch.Tensor,
    MAX: float = 255.0, eps: float = 1e-10) -> torch.Tensor: # 改造成 VIFB 提出的用于融合的 PSNR
    """
    Calculate the Peak Signal-to-Noise Ratio (PSNR) for image fusion.

    Args:
        A (torch.Tensor): The first input image tensor.
        B (torch.Tensor): The second input image tensor.
        F (torch.Tensor): The fused image tensor.
        MAX (float, optional): The maximum possible pixel value. Default is 1.
        eps (float, optional): A small value to avoid numerical instability. Default is 1e-10.

    Returns:
        torch.Tensor: The PSNR value for the fused image.

    Reference:
        [1] P. Jagalingam and A. V. Hegde, "A review of quality metrics for fused image,"
        Aquatic Procedia, vol. 4, no. Icwrcoe, pp. 133-142, 2015.
        [2] Peak Signal-to-Noise Ratio (PSNR), Available online:
        https://jason-chen-1992.weebly.com/home/-peak-single-to-noise-ratio
        [3] https://github.com/liuuuuu777/ImageFusion-Evaluation/blob/main/metrics/metricsPsnr.m
    """
    # 计算两个输入图像与融合图像的均方误差（MSE）
    MSE1 = torch.mean((A - F)**2)
    MSE2 = torch.mean((B - F)**2)
    MSE = (MSE1+MSE2)/2.0

    # 计算PSNR值，防止MSE为零
    return 10 * torch.log10(MAX ** 2 / (MSE + eps))

# 两张图完全一样，PSNR 是无穷大
def psnr_approach_loss(A: torch.Tensor, B: torch.Tensor,
    F: torch.Tensor, MAX: float = 1) -> torch.Tensor:
    return -psnr(A, B, F, MAX=MAX)

# 与 VIFB 统一
@fusion_preprocessing
def psnr_metric(A: torch.Tensor, B: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    # w0 = w1 = 0.5
    # return w0 * psnr_kornia(imgF,imgA,max_val=1) + w1 * psnr_kornia(imgF,imgB,max_val=1)
    # return w0 * psnr_kornia(imgF*255,imgA*255,max_val=255) + w1 * psnr_kornia(imgF*255,imgB*255,max_val=255) # 为了与VIFB 统一
    # 发现原来 VIFB 里边的两个 MAE 竟然在一个 log 里边！所以不能分开算两个 PSNR 再求平均。
    return psnr(A, B, F, 1) # 0-1与 0-255 的输入进去只要 MAX 设置对，结果一样

if __name__ == '__main__':
    from cslib.metrics.fusion import vis,ir,adf,cddfuse,densefuse
    print(psnr_metric(ir,vis,adf).item())
    print(psnr_metric(ir,vis,cddfuse).item())
    print(psnr_metric(ir,vis,densefuse).item())