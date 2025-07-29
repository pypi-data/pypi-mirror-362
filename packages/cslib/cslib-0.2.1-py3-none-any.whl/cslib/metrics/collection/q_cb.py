from cslib.metrics.utils import fusion_preprocessing
import torch
import kornia

__all__ = [
    'q_cb','q_cbm','q_cbb','q_cbd',
    'q_cb_approach_loss','q_cbm_approach_loss','q_cbb_approach_loss','q_cbd_approach_loss',
    'q_cb_metric','q_cbm_metric','q_cbb_metric','q_cbd_metric'
]

def _normalize(data):
    max_value = torch.max(data)
    min_value = torch.min(data)
    if max_value == 0 and min_value == 0: return data
    else: newdata = (data - min_value) / (max_value - min_value)
    return newdata * 255
    # return torch.round(newdata * 255) # <- 最终确定就是这一步导致的梯度消失

def _freq_meshgrid(size, d=1.0):
    """生成频率坐标"""
    def _line(n, d=1.0):
        val = 1.0 / (n * d)
        results = torch.arange(0, n).to(torch.float)
        p2 = (n + 1) // 2
        results[p2:] -= n
        results *= val
        shift = p2 if n % 2 == 0 else p2 - 1
        return torch.roll(results, shift, dims=0)  # 将零频率移到中心
    _, _, m, n = size
    return torch.meshgrid(_line(m,d)*2, _line(n,d)*2, indexing='ij')

def gaussian2d(sigma,size=31):
      meshgrid = kornia.create_meshgrid(size, size, normalized_coordinates=False) # type: ignore
      x = meshgrid[0, :, :, 0] - (size - 1) / 2
      y = meshgrid[0, :, :, 1] - (size - 1) / 2
      gaussian_filter = torch.exp(-(x**2 + y**2) / (2 * sigma**2)) / (2 * torch.tensor([torch.pi], dtype=torch.float64) * sigma**2)
      return gaussian_filter

G1 = gaussian2d(sigma=2,size=31) #  VIFB 这么设置的参数
G2 = gaussian2d(sigma=4,size=31)

def contrast_sensitivity_filtering_Sd(size=None,mode='frequency',filter='DoG'):
    # kernel size
    if mode == 'frequency':
        if size == None:
            raise ValueError("Should input the size of image")
        _, _, M, N = size # VIFB 希望频率的 dog 和原图一样大
        m = M/30;n = N/30 # VIFB里边这么实现的
        # m = M/2; n = N/2  # DoG1
        # m = M/4; n = N/4  # DoG2
        # m = M/8; n = N/8  # DoG3
    elif mode == 'spatial': # 最后证明
        M=N=7 # 我想转换到时域所以 size 需要很小（我加的）
        m = M/2; n = N/2  # DoG1
    else:
        raise ValueError("`mode` should only be 'frequency' or 'spatial'")

    # meshgrid
    (u, v) = _freq_meshgrid(size)
    u = u * n
    v = v * m

    # Dog in Frequency
    r = torch.sqrt(u**2 + v**2)
    if filter == 'DoG':
        f0 = 15.3870;f1 = 1.3456;a = 0.7622 # A.B. Watson, A.J. Ahumada Jr., A standard model for foveal detection of spatial contrast, Journal of Vision 5 (9) (2005) 717–740.
        Sd_freq_domain = torch.exp(-(r / f0)**2) - a * torch.exp(-(r / f1)**2)
    elif filter == 'Barton':
        Sd_freq_domain = r * torch.exp(-0.25*r)
    elif filter == 'Mannos':
        Sd_freq_domain = 2.6*(0.0192+0.114*r)*torch.exp(-(0.114*r)**1.1)
    else:
        raise ValueError("`mode` should only be 'DoG' or 'Barton' or 'Mannos'")

    if mode == 'frequency':
        return Sd_freq_domain
    elif mode == 'spatial':
        Sd_time_domain = torch.fft.ifft2(Sd_freq_domain)
        Sd_time_domain /= torch.max(torch.abs(Sd_time_domain))
        return Sd_time_domain.real

def contrast_sensitivity_filtering_freq(im, mode='frequency',filter='DoG'):
    # 计算 Sd 用于滤波
    Sd = contrast_sensitivity_filtering_Sd(im.size(),mode,filter)
    assert Sd is not None
    Sd=Sd.to(im.device)
    #print(Sd.shape)
    if mode == 'frequency': # VIFB 的方法, 但是会导致梯度消失
        # 进行二维傅里叶变换
        im_fft = torch.fft.fft2(im)
        # fftshift 操作
        im_fft_shifted = torch.roll(im_fft, shifts=(im.shape[2]//2, im.shape[3]//2), dims=(2, 3))
        # 点乘 Sd
        im_filtered_shifted = im_fft_shifted * Sd
        # ifftshift 操作
        im_filtered = torch.roll(im_filtered_shifted, shifts=(-im.shape[2]//2, -im.shape[3]//2), dims=(2, 3))
        # 逆二维傅里叶变换
        return torch.fft.ifft2(im_filtered)

    elif mode == 'spatial':
        # 使用时域卷积操作进行滤波
        return torch.nn.functional.conv2d(im, Sd.unsqueeze(0).unsqueeze(0), padding=Sd.size(0)//2)

    else:
        raise Exception("mode should only be `spatial` or `frequency`")

def q_cb(imgA: torch.Tensor, imgB: torch.Tensor, imgF: torch.Tensor,
          border_type: str = 'constant', mode: str = 'frequency',
          filter: str = 'DoG', normalize: bool = False) -> torch.Tensor:
    """
    Calculate the Q_CB (Quality Assessment for image Combined with Blurred and Fused) metric.

    Args:
        imgA (torch.Tensor): The first input image tensor.
        imgB (torch.Tensor): The second input image tensor.
        imgF (torch.Tensor): The fused image tensor.
        border_type (str, optional): Type of border extension. Default is 'constant'.
        mode (str, optional): Mode for filtering ('frequency' or 'spatial'). Default is 'frequency'.
        filter (str, optional): Type of filter to use for saliency calculation. Default is 'DoG'.
        normalize (bool, optional): Whether to normalize input images. Default is True.

    Returns:
        torch.Tensor: The Q_CB metric value.

    Reference:
        [1] Yin Chen et al., "A new automated quality assessment algorithm for image fusion,"
        Image and Vision Computing, 27 (2009) 1421-1432.
        [2] MATLAB code for the metric by Chen and Blum: https://github.com/zhengliu6699/imageFusionMetrics/blob/master/metricChenBlum.m
    """
    # mode = 'spatial', mode = 'frequency'
    # Normalize
    if normalize:
        imgA = _normalize(imgA)
        imgB = _normalize(imgB)
        imgF = _normalize(imgF)
    # return torch.mean(imgA-imgF)

    # Contrast sensitivity filtering with DoG --- Get Sd
    # Sd 被用于计算图像的局部对比度，以评估融合图像的质量。
    # Sd = contrast_sensitivity_filtering_Sd(imgA.size())
    #print('1. Sd:',torch.mean(Sd))

    # Contrast sensitivity filtering with DoG --- Frequency Domain
    fused1 = contrast_sensitivity_filtering_freq(imgA,mode,filter)
    fused2 = contrast_sensitivity_filtering_freq(imgB,mode,filter)
    ffused = contrast_sensitivity_filtering_freq(imgF,mode,filter)
    # if ffused.is_leaf == False:
    #     ffused.retain_grad()
    #     ffused.real.mean().backward()
    #     print (ffused.grad)
    #     raise
    # return torch.mean(ffused.real)
    # fused1 = contrast_sensitivity_filtering_freq(F.leaky_relu(imgA), Sd)
    # fused2 = contrast_sensitivity_filtering_freq(F.leaky_relu(imgB), Sd)
    # ffused = contrast_sensitivity_filtering_freq(F.leaky_relu(imgF), Sd)

    #print(torch.mean(fused1))
    #print(torch.mean(fused2))
    #print(torch.mean(ffused))

    # local contrast computation
    # G1, G2
    #print(torch.mean(G1),G1.shape)
    #print(torch.mean(G2),G2.shape)

    # filtering in frequency domain
    def filtering_in_frequency_domain(im):
        k = 1;h = 1;p = 3;q = 2;Z = 0.0001
        buff1 = kornia.filters.filter2d(im,G1.unsqueeze(0), border_type=border_type)
        buff2 = kornia.filters.filter2d(im,G2.unsqueeze(0), border_type=border_type)
        C = torch.abs(buff1.squeeze() / buff2.squeeze() - 1)
        #print(torch.mean(buff1),torch.mean(buff2),torch.mean(C))
        return (k * (C**p)) / (h * (C**q) + Z)
    C1P = filtering_in_frequency_domain(fused1)
    C2P = filtering_in_frequency_domain(fused2)
    CfP = filtering_in_frequency_domain(ffused)

    # if CfP.is_leaf == False:
    #     CfP.retain_grad()
    #     CfP.real.mean().backward()
    #     print (CfP.grad)
    #     raise

    #print(C1P.shape)
    #print(torch.mean(C1P))
    #print(torch.mean(C2P))
    #print(torch.mean(CfP))

    # contrast preservation calculation
    mask = (C1P < CfP).float()
    Q1F = (C1P / CfP) * mask + (CfP / C1P) * (1 - mask)

    mask = (C2P < CfP).float()
    Q2F = (C2P / CfP) * mask + (CfP / C2P) * (1 - mask)

    # Saliency map generation
    ramda1 = (C1P**2) / (C1P**2 + C2P**2)
    ramda2 = (C2P**2) / (C1P**2 + C2P**2)

    # global quality map
    Q = ramda1 * Q1F + ramda2 * Q2F

    return torch.mean(Q)

def q_cbm(imgA: torch.Tensor, imgB: torch.Tensor, imgF: torch.Tensor,
          border_type: str = 'constant', mode: str = 'frequency',
          normalize: bool = False) -> torch.Tensor:
    return q_cb(imgA,imgB,imgF,border_type,mode,'Mannos',normalize)

def q_cbb(imgA: torch.Tensor, imgB: torch.Tensor, imgF: torch.Tensor,
          border_type: str = 'constant', mode: str = 'frequency',
          normalize: bool = False) -> torch.Tensor:
    return q_cb(imgA,imgB,imgF,border_type,mode,'Barton',normalize)

def q_cbd(imgA: torch.Tensor, imgB: torch.Tensor, imgF: torch.Tensor,
          border_type: str = 'constant', mode: str = 'frequency',
          normalize: bool = False) -> torch.Tensor:
    return q_cb(imgA,imgB,imgF,border_type,mode,'DoG',normalize)

# 采用相同图片的 q_cb 减去不同图片的 q_cb
def q_cb_approach_loss(A: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    return 1-q_cbd(A, A, F)
def q_cbm_approach_loss(A: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    return 1-q_cbm(A, A, F)
def q_cbb_approach_loss(A: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    return 1-q_cbb(A, A, F)
def q_cbd_approach_loss(A: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    return 1-q_cbd(A, A, F)

# 与 VIFB 统一
@fusion_preprocessing
def q_cb_metric(A: torch.Tensor, B: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    # 论文方案mode是frequency，结果复现较为准确, 改成spatial会明显单提速，但是误差提高
    # 论文方案normalize=True
    return q_cb(A, B, F, border_type='constant', mode='frequency', normalize=True)
@fusion_preprocessing
def q_cbm_metric(A: torch.Tensor, B: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    return q_cbm(A, B, F, border_type='constant', mode='frequency', normalize=True)
@fusion_preprocessing
def q_cbb_metric(A: torch.Tensor, B: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    return q_cbb(A, B, F, border_type='constant', mode='frequency', normalize=True)
@fusion_preprocessing
def q_cbd_metric(A: torch.Tensor, B: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    return q_cbd(A, B, F, border_type='constant', mode='frequency', normalize=True)

if __name__ == '__main__':
    from cslib.metrics.fusion import vis,ir,fused
    print(q_cb_metric(ir,vis,fused).item())
    print(q_cb_metric(ir,vis.repeat(1, 3, 1, 1),fused.repeat(1, 3, 1, 1)).item())
    print(q_cb_metric(ir,vis.repeat(1, 3, 1, 1),fused).item())