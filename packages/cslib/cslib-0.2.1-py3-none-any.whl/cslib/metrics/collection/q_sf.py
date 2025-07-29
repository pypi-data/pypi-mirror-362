from cslib.metrics.utils import fusion_preprocessing
import torch
import kornia

__all__ = [
    'q_sf',
    'q_sf_approach_loss',
    'q_sf_metric'
]

def q_sf(A: torch.Tensor, B: torch.Tensor, F: torch.Tensor,
    border_type: str = 'replicate', eps: float = 1e-10) -> torch.Tensor:
    """
    Calculates the Q_SF metric between two images A and B
    with respect to a fused image F.

    Args:
        A (torch.Tensor): The first input image tensor.
        B (torch.Tensor): The second input image tensor.
        F (torch.Tensor): The fused image tensor.
        border_type (str, optional): The padding mode for convolution. Default is 'replicate'.
        eps (float, optional): Small value to prevent division by zero. Default is 1e-10.

    Returns:
        torch.Tensor: The SF quality metric value.

    Reference:
        M. Hossny, S. Nahavandi, D. Creighton, Comments on`information measure for performance of 
        image fusion`, Electron. Lett. 44 (18) (2008) 1066-1067.
    """

    def calculate_grad(I):
        RF = kornia.filters.filter2d(I,torch.tensor([[[1],[-1]]]),border_type=border_type)
        CF = kornia.filters.filter2d(I,torch.tensor([[[ 1, -1]]]),border_type=border_type)
        MDF= kornia.filters.filter2d(I,torch.tensor([[[-1,0],[0,1]]]),border_type=border_type)
        SDF= kornia.filters.filter2d(I,torch.tensor([[[0,-1],[1,0]]]),border_type=border_type)
        [MDF,SDF] = [G/torch.sqrt(torch.tensor(2.0)) for G in [MDF,SDF]]
        [RF,CF,MDF,SDF] = [torch.abs(G) for G in [RF,CF,MDF,SDF]]
        return (RF,CF,MDF,SDF)

    def calculate_sf(RF,CF,MDF,SDF):
        [RF,CF,MDF,SDF] = [torch.mean(G**2) for G in [RF,CF,MDF,SDF]]
        return torch.sqrt(RF+CF+MDF+SDF+eps)

    [RFF,CFF,MDFF,SDFF] = calculate_grad(F)
    [RFR,CFR,MDFR,SDFR] = [torch.max(GA,GB) for (GA,GB) in zip(calculate_grad(A),calculate_grad(B))]
    # import matplotlib.pyplot as plt
    # plt.subplot(2,2,1)
    # plt.imshow(RFR.squeeze().detach().numpy())
    # plt.subplot(2,2,2)
    # plt.imshow(CFR.squeeze().detach().numpy())
    # plt.subplot(2,2,3)
    # plt.imshow(MDFR.squeeze().detach().numpy())
    # plt.subplot(2,2,4)
    # plt.imshow(SDFR.squeeze().detach().numpy())
    # plt.show()
    SFF = calculate_sf(RFF,CFF,MDFF,SDFF)
    SFR = calculate_sf(RFR,CFR,MDFR,SDFR)
    return (SFF-SFR)/SFR

def q_sf_approach_loss(A: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    return 1 - q_sf(A,A,F)

# 和 OE 保持一致
@fusion_preprocessing
def q_sf_metric(A: torch.Tensor, B: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    return q_sf(A*255, B*255, F*255)

if __name__ == '__main__':
    from cslib.metrics.fusion import vis,ir,fused,densefuse,adf
    print(q_sf_metric(ir,vis,fused).item())
    print(q_sf_metric(ir,vis,densefuse).item())
    print(q_sf_metric(ir,vis,adf).item())
    # print(q_sf_metric(ir,vis.repeat(1, 3, 1, 1),fused.repeat(1, 3, 1, 1)).item())
    # print(q_sf_metric(ir,vis.repeat(1, 3, 1, 1),fused).item())
    # print(q_sf_metric(vis,vis,vis).item())
    # print(q_sf_metric(vis,vis,fused).item())
    # print(q_sf_metric(vis,vis,ir).item())
    # print(q_sf_metric(vis,ir,fused).item())
