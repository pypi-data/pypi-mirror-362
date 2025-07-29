from cslib.metrics.utils import fusion_preprocessing
import torch
import torch.nn.functional as F
from torchvision.transforms import GaussianBlur

__all__ = [
    'vif',
    'vif_approach_loss',
    'vif_metric'
]

def ComVidVindG(ref, dist, sq):
    """
    Compute visual information with and without distortion.
    
    Parameters:
    ref (torch.Tensor): Reference image tensor (C x H x W).
    dist (torch.Tensor): Distorted image tensor (C x H x W).
    sq (float): Visual noise.
    
    Returns:
    Tg1 (list of torch.Tensor): Matrix of visual information with distortion information (VID).
    Tg2 (list of torch.Tensor): Matrix of visual information without distortion information (VIND).
    Tg3 (list of torch.Tensor): Matrix of scalar value gi.
    """
    ref = ref.unsqueeze(0)
    dist = dist.unsqueeze(0)

    sigma_nsq = sq
    scales = 4
    Tg1 = []
    Tg2 = []
    Tg3 = []

    for scale in range(1, scales + 1):
        N = 2 ** (4 - scale + 1) + 1
        H = int(N/2)
        win = GaussianBlur(N,(N/5,N/5))
        
        if scale > 1:
            ref = win(ref)[:,H:-H,H:-H] # matlab 'valid'
            dist = win(dist)[:,H:-H,H:-H]# matlab 'valid'
            ref = ref[:, ::2, ::2]
            dist = dist[:, ::2, ::2]

        mu1 = win(ref)[:,H:-H,H:-H]# matlab 'valid'
        mu2 = win(dist)[:,H:-H,H:-H]# matlab 'valid'
        mu1_sq = mu1 ** 2
        mu2_sq = mu2 ** 2
        mu1_mu2 = mu1 * mu2
        sigma1_sq = win(ref**2)[:,H:-H,H:-H] - mu1_sq
        sigma2_sq = win(dist**2)[:,H:-H,H:-H] - mu2_sq
        sigma12 = win(dist*ref)[:,H:-H,H:-H] - mu1_mu2

        sigma1_sq = torch.clamp(sigma1_sq, min=0)
        sigma2_sq = torch.clamp(sigma2_sq, min=0)

        g = sigma12 / (sigma1_sq + 1e-10)
        sv_sq = sigma2_sq - g * sigma12

        g = torch.clamp(g, min=0)
        sv_sq = torch.clamp(sv_sq, min=1e-10)

        # g = torch.clamp(g, max=1)
        # sv_sq = torch.clamp(sv_sq, max=1)

        g[sigma1_sq < 1e-10] = 0
        sv_sq[sigma1_sq < 1e-10] = sigma2_sq[sigma1_sq < 1e-10]
        sigma1_sq[sigma1_sq < 1e-10] = 0

        g[sigma2_sq < 1e-10] = 0
        sv_sq[sigma2_sq < 1e-10] = 0

        sv_sq[g < 0] = sigma2_sq[g < 0]
        g[g < 0] = 0
        sv_sq[sv_sq <= 1e-10] = 1e-10

        Tg3.append(g)
        VID = torch.log10(1 + g ** 2 * sigma1_sq / (sv_sq + sigma_nsq))
        VIND = torch.log10(1 + sigma1_sq / sigma_nsq)
        Tg1.append(VID)
        Tg2.append(VIND)

    return Tg1, Tg2, Tg3

def vif(Im1, Im2, ImF):
    """
    Compute the Visual Information Fidelity (VIF) metric.

    Parameters
    ----------
    Im1 : torch.Tensor
        Source image 1 tensor.
    Im2 : torch.Tensor
        Source image 2 tensor.
    ImF : torch.Tensor
        Fused image tensor.

    Returns
    -------
    output : torch.Tensor
        Fusion assessment value.
    """
    # Visual noise
    sq = 0.005 * 255 * 255
    # Error comparison parameter
    C = 1e-7

    # r, s, l = Im1.shape

    # Color space transformation
    # if l == 3:
    #     # Convert to Lab color space
    #     cform = transforms.ColorJitter.get_params("srgb", "lab")
    #     T1 = cform(Im1)
    #     T2 = cform(Im2)
    #     TF = cform(ImF)
    #     Ix1 = T1[:, 0, :, :]
    #     Ix2 = T2[:, 0, :, :]
    #     IxF = TF[:, 0, :, :]
    # else:
    #     Ix1 = Im1
    #     Ix2 = Im2
    #     IxF = ImF
    Ix1 = Im1[0,0,:,:]
    Ix2 = Im2[0,0,:,:]
    IxF = ImF[0,0,:,:]

    T1p = Ix1.float()
    T2p = Ix2.float()
    Trp = IxF.float()

    p = torch.tensor([1, 0, 0.15, 1]) / 2.15
    T1N, T1D, T1G = ComVidVindG(T1p, Trp, sq)
    T2N, T2D, T2G = ComVidVindG(T2p, Trp, sq)

    VID = []
    VIND = []

    # Multiscale image level
    for i in range(1, 5):
        M_Z1 = T1N[i-1]
        M_Z2 = T2N[i-1]
        M_M1 = T1D[i-1]
        M_M2 = T2D[i-1]
        M_G1 = T1G[i-1]
        M_G2 = T2G[i-1]
        L = M_G1 < M_G2
        M_G = M_G2
        M_G[L] = M_G1[L]
        M_Z12 = M_Z2
        M_Z12[L] = M_Z1[L]
        M_M12 = M_M2
        M_M12[L] = M_M1[L]

        VID.append((M_Z12 + C).sum())
        VIND.append((M_M12 + C).sum())
        F = torch.tensor(VID) / torch.tensor(VIND)
    output = torch.sum(F * p)

    return output

def vif_approach_loss(A, B, F):
    return 1-vif_metric(A, B, F)

# 和 matlab 保持一致
@fusion_preprocessing
def vif_metric(A, B, F):
    return vif(A*255,B*255,F*255)

if __name__ == '__main__':
    from cslib.metrics.fusion import ir,vis,fused
    print(f'vif(vis,ir,fused):{vif_metric(ir,vis,fused)}') # should be 0.3755
