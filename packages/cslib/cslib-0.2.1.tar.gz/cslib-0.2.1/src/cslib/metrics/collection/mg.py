from cslib.metrics.utils import fusion_preprocessing
import torch
import kornia

__all__ = [
    'mg',
    'mg_approach_loss',
    'mg_metric'
]

def mg(I: torch.Tensor, eps: float = 1e-10) -> torch.Tensor:
    """
    Calculate the mean graident (MA).

    Args:
        I (torch.Tensor): Input tensor.
        eps (float, optional): A small value to avoid numerical instability.

    Reference:
        J. Ma, Y. Ma, C. Li, Infrared and visible image fusion methods 
        and applications: A survey, Inf. Fusion 45 (2019) 153-178.
    """

    # 使用Sobel算子计算水平和垂直梯度
    # AG 是所有点的梯度平均，分母是 MN
    # 然而 MG 是非下边和右边点的梯度平均，分母是 (M-1)(N-1)
    gx = kornia.filters.filter2d(I,torch.tensor([[[-1,  1]]]))[:,:,:-1,:-1]
    gy = kornia.filters.filter2d(I,torch.tensor([[[-1],[1]]]))[:,:,:-1,:-1]

    # 对梯度进行平均以避免过度敏感性(AG为了梯度会做这个步骤)
    # gx = (torch.cat((_gx[...,0:1],_gx[...,:-1]),dim=-1)+torch.cat((_gx[...,:-1],_gx[...,-2:-1]),dim=-1))/2
    # gy = (torch.cat((_gy[:,:,0:1,:],_gy[:,:,:-1,:]),dim=-2)+torch.cat((_gy[:,:,:-1,:],_gy[:,:,-2:-1,:]),dim=-2))/2

    # 计算梯度的平均幅度
    s = torch.sqrt((gx ** 2 + gy ** 2 + eps)/2)

    # 返回 MG 值
    return torch.sum(s) / ((I.shape[2] - 1) * (I.shape[3] - 1))

# 如果两幅图相等，MG 会一致
def mg_approach_loss(A: torch.Tensor, B: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    return mg(A)+mg(B)-2*mg(F)

@fusion_preprocessing
def mg_metric(A: torch.Tensor, B: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    return mg(F)

if __name__ == '__main__':
    from cslib.metrics.fusion import vis,ir,fused
    print(mg_metric(ir,vis,fused).item())
