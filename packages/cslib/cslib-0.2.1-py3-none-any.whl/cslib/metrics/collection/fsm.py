import torch
import kornia

###########################################################################################

__all__ = [
    'fsm',
    'fsm_approach_loss',
    'fsm_metric'
]

def fsm(A: torch.Tensor, B: torch.Tensor, F: torch.Tensor, window_size: int = 7, eps: float = 1e-10) -> torch.Tensor:
    # SSIM
    C1 = (0.01*255)**2
    C2 = (0.03*255)**2
    kernel = kornia.filters.get_gaussian_kernel1d(window_size, 1.5, device=F.device, dtype=F.dtype)
    muA = kornia.filters.filter2d_separable(A, kernel, kernel, padding="valid")
    muB = kornia.filters.filter2d_separable(B, kernel, kernel, padding="valid")
    muF = kornia.filters.filter2d_separable(F, kernel, kernel, padding="valid")
    sAA = kornia.filters.filter2d_separable(A**2, kernel, kernel, padding="valid") - muA**2
    sBB = kornia.filters.filter2d_separable(B**2, kernel, kernel, padding="valid") - muB**2
    sFF = kornia.filters.filter2d_separable(F**2, kernel, kernel, padding="valid") - muF**2
    sAF = kornia.filters.filter2d_separable(A*F, kernel, kernel, padding="valid") - muA*muF
    sBF = kornia.filters.filter2d_separable(B*F, kernel, kernel, padding="valid") - muB*muF
    ssimAF = ((2*muA*muF + C1)*(2*sAF + C2)) / ((muA**2 + muF**2 + C1)*(sAA + sFF + C2))
    ssimBF = ((2*muB*muF + C1)*(2*sBF + C2)) / ((muB**2 + muF**2 + C1)*(sBB + sFF + C2))
    # IC_SSM
    wA = sAA / torch.mean(sAA)
    wB = sBB / torch.mean(sBB)
    c = (sAF+eps)/(sAF+sBF+eps)
    print(torch.mean(c))
    c[c<0] = 0.0
    c[c>1] = 1.0
    ic_ssim = c*wA*ssimAF + (1-c)*wB*ssimBF
    print(torch.mean(ssimAF),torch.mean(wA),torch.mean(wA*ssimAF))
    print(torch.mean(ssimBF),torch.mean(wB),torch.mean(wB*ssimBF))
    return torch.mean(ic_ssim)

def fsm_approach_loss(A: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    return fsm(A,A,F)

def fsm_metric(A: torch.Tensor, B: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    return fsm(A,B,F)

###########################################################################################

def main():
    from torchvision import transforms
    from torchvision.transforms.functional import to_tensor
    from PIL import Image

    torch.manual_seed(42)

    transform = transforms.Compose([transforms.ToTensor()])

    vis = to_tensor(Image.open('../imgs/TNO/vis/9.bmp')).unsqueeze(0)
    ir = to_tensor(Image.open('../imgs/TNO/ir/9.bmp')).unsqueeze(0)
    fused = to_tensor(Image.open('../imgs/TNO/fuse/U2Fusion/9.bmp')).unsqueeze(0)

    print(f'fsm(vis,ir,fused):{fsm(vis*255,ir*255,fused*255)}')
    print(f'fsm(vis,ir,fused):{fsm(vis*255,ir*255,(vis+ir)/2*255)}')
    print(f'fsm(vis,vis,vis):{fsm(vis*255,vis*255,vis*255)}')
    print(f'fsm(vis,vis,fused):{fsm(vis*255,vis*255,fused*255)}')
    print(f'fsm(vis,vis,ir):{fsm(vis*255,vis*255,ir*255)}')
    # print(f'fsm(vis,vis,vis):{fsm(vis,vis,vis)}')
    # print(f'fsm(vis,vis,fused):{fsm(vis,vis,fused)}')
    # print(f'fsm(vis,vis,ir):{fsm(vis,vis,ir)}')

if __name__ == '__main__':
    main()
