from cslib.metrics.utils import fusion_preprocessing
import torch
import kornia
from skimage.feature import graycomatrix
from typing import List

__all__ = [
    'asm',
    'asm_metric'
]

def asm(tensor: torch.Tensor, distances: List[int] = [1, 2], angles: List[int] = [0, 90]) -> torch.Tensor:
    """
    Calculate the Angular Second Moment (ASM) of a gray-scale image tensor.

    Args:
        tensor (torch.Tensor): The input gray-scale image tensor.
        distances (List[int], optional): List of pixel pair distances. Default is [1, 2].
        angles (List[int], optional): List of angles in degrees. Default is [0, 90].

    Returns:
        torch.Tensor: The ASM value.

    Reference:
        https://blog.csdn.net/qq_49729636/article/details/134502721
    """
    # 转换为灰度图像
    if tensor.shape[1] == 3:
        tensor = kornia.color.rgb_to_grayscale(tensor)

    # 转换为 uint8 类型
    tensor = (tensor * 255).to(torch.uint8)

    asm_sum = torch.tensor(0.0)
    # 计算每个角度和距离的 ASM，并将其加总
    for d in distances:
        for a in angles:
            m = graycomatrix(tensor.cpu().numpy().squeeze(), distances=distances, angles=angles, symmetric=True, normed=True)
            m = torch.tensor(m)
            asm_sum += torch.sum(m**2)

    # 计算 ASM 的平均值
    asm_mean: torch.Tensor = asm_sum / (len(distances)*len(angles))

    return asm_mean

@fusion_preprocessing
def asm_metric(A: torch.Tensor, B: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    return asm(F)

if __name__ == '__main__':
    from cslib.metrics.fusion import ir,vis,fused
    print(f'ergas metric: {asm_metric(ir,vis,fused)}')