from cslib.metrics.utils import fusion_preprocessing
import torch
import kornia

__all__ = [
    'viff',
    'viff_approach_loss',
    'viff_metric'
]

def viff(A: torch.Tensor, B: torch.Tensor, F: torch.Tensor, eps: float = 1e-10) -> torch.Tensor:
    """Calculate the Visual Information Fidelity for Fusion (VIFF) metric.

    Args:
        A (torch.Tensor): The source image tensor.
        B (torch.Tensor): The fused image tensor.
        F (torch.Tensor): The reference image tensor.
        eps (float, optional): Small value to avoid division by zero. Defaults to 1e-10.

    Returns:
        torch.Tensor: The VIF metric value.

    Reference:
        [1] Yu Han, Yunze Cai, Yin Cao, Xiaoming Xu, A new image fusion performance metric 
        based on visual information fidelity, information fusion, Volume 14, Issue 2, April 2013, Pages 127-135
        [2] https://github.com/HarrisXia/image-fusion-evaluation/blob/c4173cf45a83754b59c375ebc1ab2036a47245cb/VIFF_Public.m
    """
    def gaussian_kernel(kernel_size, sigma):
        # Create a grid of points centered at the kernel origin
        x = torch.arange(-kernel_size // 2 + 1, kernel_size // 2 + 1, dtype=torch.float32)
        y = torch.arange(-kernel_size // 2 + 1, kernel_size // 2 + 1, dtype=torch.float32)
        grid = torch.meshgrid(x, y, indexing='ij')
        distance = torch.sqrt(grid[0]**2 + grid[1]**2)

        # Calculate the 2D Gaussian kernel
        kernel = torch.exp(-0.5 * (distance / sigma)**2)
        kernel = kernel / kernel.sum()  # Normalize the kernel to ensure sum is 1
        return kernel.unsqueeze(0)

    def ComVidVindG(ref, dist, sq):
        num_scales = 4
        sigma_nsq = sq
        tg1 = []
        tg2 = []
        tg3 = []
        for scale in range(num_scales):
            N = 2**(4-scale)+1
            win = gaussian_kernel(N, N/5.0)

            if scale!=0:
                ref = kornia.filters.filter2d(ref, win, padding="valid")[:,:,::2,::2]
                dist = kornia.filters.filter2d(dist, win, padding="valid")[:,:,::2,::2]

            mu1 = kornia.filters.filter2d(ref, win, padding="valid")
            mu2 = kornia.filters.filter2d(dist, win, padding="valid")
            mu1_sq = mu1**2
            mu2_sq = mu2**2
            mu1_mu2 = mu1 * mu2
            sigma1_sq = kornia.filters.filter2d(ref**2, win, padding="valid") - mu1_sq
            sigma2_sq = kornia.filters.filter2d(dist**2, win, padding="valid") - mu2_sq
            sigma12 = kornia.filters.filter2d(ref * dist, win, padding="valid") - mu1_mu2

            sigma1_sq[sigma1_sq < 0] = 0
            sigma2_sq[sigma2_sq < 0] = 0

            g = sigma12 / (sigma1_sq + 1e-10)
            sv_sq = sigma2_sq - g * sigma12

            g[sigma1_sq < 1e-10] = 0
            sv_sq[sigma1_sq < 1e-10] = sigma2_sq[sigma1_sq < 1e-10]
            sigma1_sq[sigma1_sq < 1e-10] = 0

            g[sigma2_sq < 1e-10] = 0
            sv_sq[sigma2_sq < 1e-10] = 0

            sv_sq[g < 0] = sigma2_sq[g < 0]
            g[g < 0] = 0
            sv_sq[sv_sq <= 1e-10] = 1e-10

            tg1.append(torch.log10(1 + g**2 * sigma1_sq / (sv_sq + sigma_nsq)))
            tg2.append(torch.log10(1 + sigma1_sq / sigma_nsq))
            tg3.append(g)

        return tg1, tg2, tg3

    sq=0.005*255*255 # visual noise
    p = torch.tensor([item/2.15 for item in [1,0,0.15,1]])

    (T1N, T1D, T1G) = ComVidVindG(A,F,sq)
    (T2N, T2D, T2G) = ComVidVindG(B,F,sq)

    vid = []
    vind = []
    for i in range(4):
        M_Z1 = T1N[i]
        M_Z2 = T2N[i]
        M_M1 = T1D[i]
        M_M2 = T2D[i]
        M_G1 = T1G[i]
        M_G2 = T2G[i]
        L = M_G1 < M_G2
        M_G = M_G2.clone()
        M_G[L] = M_G1[L]
        M_Z12 = M_Z2.clone()
        M_Z12[L] = M_Z1[L]
        M_M12 = M_M2.clone()
        M_M12[L] = M_M1[L]

        VID = torch.sum(torch.sum(M_Z12 + eps))
        VIND = torch.sum(torch.sum(M_M12 + eps))
        vid.append(VID)
        vind.append(VIND)

    F = torch.tensor([vid[i] / vind[i] for i in range(4)])
    output = torch.sum(F * p)

    return output


def viff_approach_loss(A: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    return 1-viff(A,A,F)

# 和原 matlab 结果保持一致
@fusion_preprocessing
def viff_metric(A: torch.Tensor, B: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    return viff(A*255.0, B*255.0, F*255.0)

if __name__ == '__main__':
    from cslib.metrics.fusion import ir,vis,fused
    print(f'VIFF:{viff_metric(vis, ir, fused)}') # should be 0.3755
