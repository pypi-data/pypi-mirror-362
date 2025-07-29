from cslib.metrics.utils import fusion_preprocessing
import torch
import kornia

__all__ = [
    'ce',
    'ce_approach_loss',
    'ce_metric'
]

def ce(target: torch.Tensor, predict: torch.Tensor, bandwidth: float = 0.1, eps: float = 1e-10) -> torch.Tensor:
    """
    Calculate the cross-entropy between the target and predicted histograms.

    Args:
        target (torch.Tensor): The target image tensor.
        predict (torch.Tensor): The predicted image tensor.
        bandwidth (float, optional): Bandwidth for histogram smoothing. Default is 0.1.
        eps (float, optional): A small value to avoid numerical instability. Default is 1e-10.

    Returns:
        torch.Tensor: The cross-entropy between the histograms of the target and predicted images.

    Reference:
        [1] D. M. Bulanon, T. Burks, and V. Alchanatis, "Image fusion of visible
        and thermal images for fruit detection," Biosystems Engineering, vol. 103,
        no. 1, pp. 12-22, 2009.
    """
    # 将预测值和目标值缩放到范围[0, 255]
    predict = predict.view(1, -1) * 255
    target = target.view(1, -1) * 255

    # 创建用于直方图计算的区间
    bins = torch.linspace(0, 255, 256).to(predict.device)

    # 计算目标和预测图像的直方图
    h1 = kornia.enhance.histogram(target, bins=bins, bandwidth=torch.tensor(bandwidth))
    h2 = kornia.enhance.histogram(predict, bins=bins, bandwidth=torch.tensor(bandwidth))

    # 创建一个掩码以排除直方图中小于eps的值 - 这里是与 VIFB 统一的重点
    mask = (h1 > eps)&( h2 > eps)

    # 计算交叉熵
    return torch.sum(h1[mask] * torch.log2(h1[mask]/(h2[mask])))

# 如果两幅图片一样 ce 为 0
def ce_approach_loss(A: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    return -ce(A, F)

# 与 VIFB 统一
@fusion_preprocessing
def ce_metric(A: torch.Tensor, B: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    w0 = w1 = 0.5
    return w0 * ce(A,F) + w1 * ce(B,F)

if __name__ == '__main__':
    from cslib.metrics.fusion import vis,ir,fused
    print(ce_metric(ir,vis,fused).item())
    print(ce_metric(vis,vis,vis).item())
