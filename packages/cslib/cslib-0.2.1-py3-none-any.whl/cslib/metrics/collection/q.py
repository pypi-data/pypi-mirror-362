from cslib.metrics.utils import fusion_preprocessing
import torch
import kornia

__all__ = [
    'q',
    'q_approach_loss',
    'q_metric'
]

def q(X: torch.Tensor, Y: torch.Tensor, block_size: int = 8) -> torch.Tensor:
    """
    Calculate the quality index between two images.
    Q = QI = UIQI = Q0 (they are the same)
    Q is used to model a any distortion as a combination of three 
    different factors: loss of correlation, luminance distortions,
    and contrast distortion. The range of QI is -1 to 1. The value
    1 indicates reference and fused images are similar.

    Args:
        img1 (torch.Tensor): The first input image tensor.
        img2 (torch.Tensor): The second input image tensor.
        block_size (int, optional): The size of the blocks used in the calculation. Default is 8.

    Returns:
        torch.Tensor: The quality index between the two input images.

    Raises:
        ValueError: If the input images have different dimensions.

    Reference:
        [1] http://live.ece.utexas.edu/research/Quality/zhou_research_anch/quality_index/demo.html
        [2] https://github.com/SeyedMuhammadHosseinMousavi/A-New-Edge-and-Pixel-Based-Image-Quality-Assessment-Metric-for-Colour-and-Depth-Images/blob/60be6958fddab4d1e5b42989c94b6494ec34bc64/imageQualityIndex.m
        [3] Wang, Z. and A.C.B., 2002. A universal image quality index. IEEE singal Process. Lett. XX, 2-5.
    """
    N = block_size**2
    mean_filter = torch.ones(1, 1, block_size, block_size).squeeze(0)# / N

    XX = X*X
    YY = Y*Y
    XY = X*Y

    mX = kornia.filters.filter2d(X, mean_filter, padding='valid')
    mY = kornia.filters.filter2d(Y, mean_filter, padding='valid')
    mXX = kornia.filters.filter2d(XX, mean_filter, padding='valid')
    mYY = kornia.filters.filter2d(YY, mean_filter, padding='valid')
    mXY = kornia.filters.filter2d(XY, mean_filter, padding='valid')

    mXmY = mX * mY
    sum_m2X_m2Y = mX**2 + mY**2

    numerator = 4 * (N * mXY - mXmY) * mXmY
    denominator1 = N * (mXX + mYY) - sum_m2X_m2Y
    denominator = denominator1 * sum_m2X_m2Y

    quality_map = torch.ones_like(denominator)
    index = (denominator1 == 0) & (sum_m2X_m2Y != 0)
    quality_map[index] = 2 * mXmY[index] / sum_m2X_m2Y[index]
    index = (denominator != 0)
    quality_map[index] = numerator[index] / denominator[index]

    return torch.mean(quality_map)

def q_approach_loss(A: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    return 1 - q(A,F)

# 和 matlab 结果保持一致
@fusion_preprocessing
def q_metric(A: torch.Tensor, B: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    w0 = w1 = 0.5
    return w0 * q(A, F) + w1 * q(B, F)

if __name__ == '__main__':
    from cslib.metrics.fusion import ir,vis,fused

    print(f'Q(vis,vis):{q(vis,vis)}')
    print(f'Q(vis,fused):{q(vis,fused)}')  # should be 0.4102
    print(f'Q(vis,ir):{q(vis,ir)}') # should be -0.0432
    print(f'Q(vis,ir):{q(vis*255.0,ir*255.0)}') # the same

    # print(f'Q(vis,vis):{q(vis,vis,256)}') out of memory
    # print(f'Q(vis,fused):{q(vis,fused,256)}')
    # print(f'Q(vis,ir):{q(vis,ir,256)}')

    # print(f'Q(vis,vis):{q(vis,vis,16)}') # 结果差不多
    # print(f'Q(vis,fused):{q(vis,fused,16)}')
    # print(f'Q(vis,ir):{q(vis,ir,16)}')

    from torchmetrics.image import UniversalImageQualityIndex
    uqi = UniversalImageQualityIndex()
    print(uqi(vis*255, vis*255))
    print(uqi(vis*255, fused*255)) # 不如我写的准确
    print(uqi(vis*255, ir*255))
