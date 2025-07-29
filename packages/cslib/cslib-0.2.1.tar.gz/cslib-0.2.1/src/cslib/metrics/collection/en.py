from cslib.metrics.utils import fusion_preprocessing
import torch
import kornia

__all__ = [
    'en',
    'en_approach_loss',
    'en_metric'
]

def en(grey_tensor: torch.Tensor, bandwidth: float = 0.1, eps: float = 1e-10, is_pdf: bool = False) -> torch.Tensor:
    """
    Calculate the entropy of a grayscale image.

    Args:
        grey_tensor (torch.Tensor): The grayscale image tensor.
        bandwidth (float, optional): Bandwidth for histogram smoothing. Default is 0.1.
        eps (float, optional): A small value to avoid numerical instability. Default is 1e-10.
        is_pdf (bool, optional): Whether the input tensor represents a probability density function (PDF).
                    If True, the input tensor is considered as a PDF; otherwise, it is treated as pixel values.
                    Default is False.

    Returns:
        torch.Tensor: The entropy of the grayscale image.

    Reference:
        [1] V. Aardt and Jan, "Assessment of image fusion procedures using entropy,
        image quality, and multispectral classification," Journal of Applied Remote
        Sensing, vol. 2, no. 1, p. 023522, 2008.
    """
    if is_pdf == False:
        # 将灰度图像值缩放到范围[0, 255]
        grey_tensor = grey_tensor.view(1, -1) * 255

        # 创建用于直方图计算的区间
        bins = torch.linspace(0, 255, 256).to(grey_tensor.device)

        # 计算灰度图像的直方图
        histogram = kornia.enhance.histogram(grey_tensor, bins=bins, bandwidth=torch.tensor(bandwidth))
    else:
        histogram = grey_tensor

    # 计算图像的熵
    image_entropy = -torch.sum(histogram * torch.log2(histogram + eps))

    return image_entropy

# 两张图一样，含有的信息会相等
def en_approach_loss(A: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    return torch.abs(en(A) - en(F))

# 与 VIFB 统一
@fusion_preprocessing
def en_metric(A: torch.Tensor, B: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    return en(F)
