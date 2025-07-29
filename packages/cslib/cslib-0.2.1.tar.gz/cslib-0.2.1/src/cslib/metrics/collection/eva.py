from cslib.metrics.utils import fusion_preprocessing
import torch
import kornia

__all__ = [
    'eva',
    'eva_approach_loss',
    'eva_metric'
]

def eva(A: torch.Tensor) -> torch.Tensor:
    """
    Evaluate the image by calculating the sum of the absolute mean values of specific kernels.

    Args:
        A (torch.Tensor): The input image tensor.

    Returns:
        torch.Tensor: The evaluation value.

    Reference:
        [1] https://zhuanlan.zhihu.com/p/136013000
        [2] 王鸿南,钟文,汪静,等.图像清晰度评价方法研究[J].中国图象图形学报: A辑,2004(7):828-831.
    """
    corner = 1 / 2 ** 0.5
    border = 1.0
    center = -4*(corner+border)

    k1 = torch.tensor([[[corner,0,0],[0,-corner,0],[0,0,0]]])
    k2 = torch.tensor([[[0,0,corner],[0,-corner,0],[0,0,0]]])
    k3 = torch.tensor([[[0,0,0],[0,-corner,0],[corner,0,0]]])
    k4 = torch.tensor([[[0,0,0],[0,-corner,0],[0,0,corner]]])
    k5 = torch.tensor([[[0,border,0],[0,-border,0],[0,0,0]]])
    k6 = torch.tensor([[[0,0,0],[0,-border,0],[0,border,0]]])
    k7 = torch.tensor([[[0,0,0],[border,-border,0],[0,0,0]]])
    k8 = torch.tensor([[[0,0,0],[0,-border,border],[0,0,0]]])

    res = [torch.mean(torch.abs(kornia.filters.filter2d(A,kernel))) for kernel in [k1,k2,k3,k4,k5,k6,k7,k8]]

    return torch.sum(torch.stack(res))

def eva_approach_loss(A: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    return torch.abs(eva(A)-eva(F))

@fusion_preprocessing
def eva_metric(A: torch.Tensor, B: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    return eva(F) * 255.0

if __name__ == '__main__':
    from cslib.metrics.fusion import ir,vis,fused
    print(f'EVA:{eva_metric(vis, ir, fused)}')
