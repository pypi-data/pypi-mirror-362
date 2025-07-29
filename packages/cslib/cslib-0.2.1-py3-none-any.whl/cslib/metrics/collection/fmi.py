from cslib.metrics.utils import fusion_preprocessing
import torch
import kornia
import scipy
from pathlib import Path

__all__ = [
    'fmi',
    'fmi_approach_loss',
    'fmi_metric','fmi_p_metric','fmi_w_metric','fmi_e_metric','fmi_d_metric','fmi_g_metric',
]

def _wavelet(I, dwtEXTM='sym'):
    # Matlab:
    # [cA,cH,cV,cD] = dwt2(I,'dmey');
    # aFeature = rerange([cA,cH;cV,cD]);
    # M. Misiti, Y. Misiti, G. Oppenheim, J.M. Poggi 12-Mar-96.
    #
    # dwtEXTM: 'sym', 'per'(per是周期延拓的意思) 目前只写了sym方式
    path = Path(__file__).resolve().parent.parent / 'fusion' / 'resources' / 'dmey.mat'
    try:
        W = torch.tensor(scipy.io.loadmat(path)['dmey'])
    except:
        W = torch.tensor(scipy.io.loadmat(path)['dmey'])
    Lo_R = W * torch.sqrt(torch.tensor(2))
    Hi_D = Lo_R.clone()
    Hi_D[:,0::2] *= -1
    Hi_R = torch.flip(Hi_D, [-2])
    Lo_D = torch.flip(Lo_R, [-2])

    L = Lo_R.shape[1]
    _ ,_, M, N = I.shape
    first = [2,2]  # 默认偏移量为 [0 0]，所以 first = [2 2]
    if dwtEXTM == 'sym':
        sizeEXT = L - 1
        last = [sizeEXT + M,sizeEXT + N]
    elif dwtEXTM == 'per': # 周期延拓模式
        sizeEXT = L // 2  #扩展大小为滤波器长度的一半
        last = [2 * ((M + 1) // 2), 2 * ((N + 1) // 2)]  # 周期延拓模式，最终大小为 2x2 的整数倍
    else:
        raise ValueError("dwtEXTM should be 'sym' or 'per'")

    def wextend_addcol(tensor, n):
        left_cols = torch.flip(tensor[:,:,:,:n], dims=[-1])
        right_cols = torch.flip(tensor[:,:,:,-n:], dims=[-1])
        return torch.cat([left_cols, tensor, right_cols], dim=-1)

    def wextend_addrow(tensor, n):
        up_raws = torch.flip(tensor[:,:,:n,:], dims=[-2])
        down_raws = torch.flip(tensor[:,:,-n:,:], dims=[-2])
        return torch.cat([up_raws, tensor, down_raws], dim=-2)

    def convdown(tensor, kernel, lenEXT):
        y = tensor[..., first[1]:last[1]:2]             # 提取需要进行卷积的子集
        y = wextend_addrow(y, lenEXT)   # 使用 'addrow' 模式对 y 进行扩展
        y = kornia.filters.filter2d(y.permute(0, 1, 3, 2),kernel.unsqueeze(0),padding="valid")
        y = y.permute(0, 1, 3, 2)[:,:,first[0]:last[0]:2,:]   # 提取结果的子集
        return y

    Y = wextend_addcol(I,sizeEXT)
    Z = kornia.filters.filter2d(Y,Lo_D.unsqueeze(0),padding="valid")
    A = convdown(Z,Lo_D,sizeEXT)
    H = convdown(Z,Hi_D,sizeEXT)
    Z = kornia.filters.filter2d(Y,Hi_D.unsqueeze(0),padding="valid")
    V = convdown(Z,Lo_D,sizeEXT)
    D = convdown(Z,Hi_D,sizeEXT)

    R = torch.cat([torch.cat([A, H], dim=-1),torch.cat([V, D], dim=-1)], dim=-2)
    return (R-torch.min(R)) / (torch.max(R)-torch.min(R))

def _gradient(I,eps=1e-10):
    # 使用Sobel算子计算水平和垂直梯度
    _grad_x = kornia.filters.filter2d(I,torch.tensor([[-1,  1]], dtype=torch.float64).unsqueeze(0))
    _grad_y = kornia.filters.filter2d(I,torch.tensor([[-1],[1]], dtype=torch.float64).unsqueeze(0))

    # 对梯度进行平均以避免过度敏感性(与 Matlab 统一)
    grad_x = (torch.cat((_grad_x[:,:,:,0:1],_grad_x[:,:,:,:-1]),dim=-1)+torch.cat((_grad_x[:,:,:,:-1],_grad_x[:,:,:,-2:-1]),dim=-1))/2
    grad_y = (torch.cat((_grad_y[:,:,0:1,:],_grad_y[:,:,:-1,:]),dim=-2)+torch.cat((_grad_y[:,:,:-1,:],_grad_y[:,:,-2:-1,:]),dim=-2))/2

    # 计算梯度的平均幅度
    s = torch.sqrt((grad_x ** 2 + grad_y ** 2 + eps)/2)

    #return grad_x # 在 matlab 代码中，没有求 y 方向的梯度，我进行了改进
    return s

def _edge(I, method='sobel',border_type='replicate', eps=1e-10): # matlab 版本默认是 sobel
    # 与 Matlab 的 [bx, by, b] = images.internal.builtins.edgesobelprewitt(a, isSobel, kx, ky); 完全一致
    grad_x = 1/8 * kornia.filters.filter2d(I,torch.tensor([[ 1,  0, -1],[ 2,  0, -2],[ 1,  0, -1]], dtype=torch.float64).unsqueeze(0),border_type=border_type)
    grad_y = 1/8 * kornia.filters.filter2d(I,torch.tensor([[ 1,  2,  1],[ 0,  0,  0],[-1, -2, -1]], dtype=torch.float64).unsqueeze(0),border_type=border_type)
    grad = (grad_x ** 2 + grad_y ** 2)
    # cutoff = scale * sum(b(:),'double') / numel(b); matlab中 scale 是 4
    # thresh = sqrt(cutoff);
    cutoff = 4 * torch.sum(grad) / (I.shape[-1] * I.shape[-2])
    thresh = torch.sqrt(cutoff)
    # 无法模拟
    # e = images.internal.builtins.computeEdges(b,bx,by,kx,ky,int8(offset),100*eps,cutoff);
    # 退而求其次: e = b > cutoff;
    e = (grad > cutoff).float()
    return e

def _dct(I):
    def dct(a):
        _, _, m, n = a.shape
        if n==1 or m==1:
            if n>1:
                do_trans = True
            else:
                do_trans = False
            a = torch.reshape(a,(1,1,m+n-1,1))
        else:
            do_trans = False
        _, _, n, m = a.shape

        aa = a

        if n % 2 == 1:
            y = torch.cat((aa, torch.flip(aa,[-2])),dim=-2)
            yy = torch.fft.fft(y, dim=-2)
            ww = (torch.exp(-1j * torch.arange(n) * torch.tensor(float(torch.pi) / (2 * n))) / torch.sqrt(torch.tensor(2 * n, dtype=torch.double))).unsqueeze(1)
            ww[0] = ww[0] / torch.sqrt(torch.tensor(2, dtype=torch.double))
            b = ww.expand(n, m)*(yy[:,:,:n,:])
        else:
            y = torch.cat((aa[:,:,::2, :], torch.flip(aa[:,:,1::2, :],[-2])), dim=-2)
            yy = torch.fft.fft(y, dim=-2)
            ww = 2 * torch.exp(-1j * torch.arange(n).unsqueeze(1) * torch.tensor(float(torch.pi) / (2 * n), dtype=torch.double)) / torch.sqrt(torch.tensor(2 * n, dtype=torch.double))
            ww[0] = ww[0] / torch.sqrt(torch.tensor(2, dtype=torch.double))
            b = ww.expand(n, m) * yy

        return b.real

    return torch.transpose(dct(torch.transpose(dct(I), dim0=-1, dim1=-2)), dim0=-1, dim1=-2)


def fmi(A: torch.Tensor, B: torch.Tensor, F: torch.Tensor, feature: str = 'pixel', window_size: int = 3) -> torch.Tensor:
    """
    Calculate the Feature Mutual Information (FMI) between two images A and B with respect to a reference image F.

    Args:
        A (torch.Tensor): Image A.
        B (torch.Tensor): Image B.
        F (torch.Tensor): Reference image F.
        feature (str): Type of feature to use. Options are 'pixel', 'wavelet', 'edge', 'dct', 'gradient'. Default is 'pixel'.
        window_size (int): Size of the sliding window. Default is 3.

    Returns:
        torch.Tensor: FMI value.

    Reference:
        [1] M.B.A. Haghighat, A. Aghagolzadeh, H. Seyedarabi, A non-reference image 
            fusion metric based on mutual information of image features, Comput. 
            Electr. Eng. 37 (5) (2011) 744-756.
        [2] G. Qu, D. Zhang, P. Yan, Information measure for performance of image 
            fusion, Electron. Lett. 38 (7) (2002) 313-315.
    """
    if feature == 'pixel':
        [A,B,F] = [A.float()*255,B.float()*255,F.float()*255]
    elif feature == 'wavelet':
        [A,B,F] = [_wavelet(I.float()*255) for I in [A, B, F]]
    elif feature == 'dct':
        [A,B,F] = [_dct(I.float()*255) for I in [A, B, F]]
    elif feature == 'edge': # 未完全复现，没有按照 thin 的方案
        [A,B,F] = [_edge(I.float()*255) for I in [A, B, F]]
    elif feature == 'gradient':
        [A,B,F] = [_gradient(I.float()*255) for I in [A, B, F]]
    else:
        raise ValueError("feature should be: 'gradient', 'edge', 'dct', 'wavelet', 'pixel'")
    
    _, _, m, n = A.shape
    w = int((window_size+1)/2-1)
    fmi_map = torch.ones((m - 2 * w, n - 2 * w))

    # 展开
    def unfolded_image(I):
        unfolded = torch.nn.functional.unfold(I, (m-2*w,n-2*w), stride=1)
        return unfolded.view(unfolded.size(0), unfolded.size(1), -1).squeeze(0)  # 将展平的张量重新变形为窗口数据
    [uA, uB, uF] = [unfolded_image(I) for I in [A, B, F]]

    def reorder_for_matlab(uI):
        return torch.cat([uI[:,i::window_size] for i in range(window_size)], dim=1)
    [uA, uB, uF] = [reorder_for_matlab(uI) for uI in [uA, uB, uF]]
    # print('uA',uA[640:641,:])
    # print('uB',uB[640:641,:])
    # print('uF',uF[640:641,:])

    # 计算pdf
    def cal_pdf(uI):
        # 计算最大最小值
        (max_uI,_) = torch.max(uI,dim=1)
        (min_uI,_) = torch.min(uI,dim=1)
        max_uI = max_uI.unsqueeze(-1)
        min_uI = min_uI.unsqueeze(-1)
        # 调整分母
        denominator = max_uI - min_uI
        denominator[max_uI == min_uI] = 1
        # 调整分子
        classify = denominator.clone()
        classify[max_uI != min_uI] = 0
        classify = torch.matmul(classify,torch.ones(1,uI.shape[-1],device=classify.device))
        numerator = uI - min_uI
        numerator = (1-classify) * numerator + classify
        # 规范化
        uI = numerator / denominator
        # pdf
        return uI / torch.sum(uI,dim=1).unsqueeze(-1)
    [pdfA, pdfB, pdfF] = [cal_pdf(uI) for uI in [uA, uB, uF]]
    # print('pdfA',pdfA[640:641,:])
    # print('pdfF',pdfF[640:641,:])

    # 计算相等的区域
    def cal_same(uI, uF):
        return ((uI == uF).all(dim=-1)).float().unsqueeze(-1)
    [sameAF, sameBF] = [cal_same(pdfI, pdfF) for pdfI in [pdfA, pdfB]]
    # print('sameAF',sameAF[640:641,:])

    # 累积求和得到 CDF
    [cdfA, cdfB, cdfF] = [torch.cumsum(pdfI, dim=1) for pdfI in [pdfA, pdfB, pdfF]]

    # 计算判别常数 C(与 0 的大小比较)
    def cal_c(pdfI, pdfF):
        tempI = pdfI - torch.mean(pdfI,dim=1).unsqueeze(-1)
        tempF = pdfF - torch.mean(pdfF,dim=1).unsqueeze(-1)
        sumIF = torch.sum(tempI * tempF, dim=1)
        sumII = torch.sum(tempI * tempI, dim=1)
        sumFF = torch.sum(tempF * tempF, dim=1)
        denominator = sumII * sumFF # In case denominator==0
        denominator[denominator==0] = 1.0 # tempI * tempI >= 0, so set denominator > 0
        cIF = (sumIF / torch.sqrt(denominator)).unsqueeze(-1)
        return cIF
    [cAF, cBF] = [cal_c(pdfI,pdfF) for pdfI in [pdfA, pdfB]]

    # 标准差
    def cal_sd(pdfI):
        weight = torch.arange(1,window_size**2+1,1,device=pdfI.device)
        pdfEI = torch.sum(weight * pdfI,dim=1).unsqueeze(-1)
        pdfE2I = torch.sum(weight**2 * pdfI,dim=1).unsqueeze(-1)
        return torch.sqrt(torch.abs(pdfE2I - pdfEI**2))
    [sdA, sdB, sdF] = [cal_sd(pdfI) for pdfI in [pdfA, pdfB, pdfF]]

    # 计算熵
    def cal_entropy(jpdf):
        zero_mask = (jpdf==0).float()
        zero_en = jpdf*0.0
        pos_mask = (jpdf>0).float()
        pos_jpdf = pos_mask * jpdf
        pos_jpdf[pos_jpdf==0] = 1.0
        pos_en = pos_mask*(-pos_jpdf * torch.log2(pos_jpdf))
        neg_mask = (jpdf<0).float()
        neg_jpdf = neg_mask * jpdf
        neg_jpdf[neg_jpdf==0] = -1.0
        neg_en = neg_mask*(-neg_jpdf * torch.log2(-neg_jpdf))
        return zero_en + pos_en + neg_en
    [eA, eB, eF] = [torch.sum(cal_entropy(pdfI),dim=1).unsqueeze(-1) for pdfI in [pdfA, pdfB, pdfF]]

    # angle
    def cal_jpdf(cIF,cdfI,cdfF,pdfI,pdfF,sdI,sdF):
        # Mask
        zero_mask = (cIF * sdI * sdF == 0).float() # Is Zero
        positive_mask = (cIF>=0).float()            # c > 0

        # Angle
        numerator = sdF*sdI
        numerator[numerator==0] = 1.0 # In case sdF*sdI==0
        cdfIs = [torch.cat((cdfI[:,i:], cdfI[:,:i]), dim=1) for i in range(window_size**2)]
        phis = [torch.sum(0.5*(cdfIi+cdfF-torch.abs(cdfIi-cdfF))-cdfIi*cdfF,dim=1).unsqueeze(-1) for cdfIi in cdfIs]
        phi_denominator = torch.sum(torch.stack(phis), dim=0)
        phi_denominator[phi_denominator==0] = 1.0 # In case sdF*sdI==0
        phi = (1-zero_mask)*(cIF*numerator/phi_denominator)
        thetas = [torch.sum(0.5*(cdfIi+cdfF-1+torch.abs(cdfIi+cdfF-1))-cdfIi*cdfF,dim=1).unsqueeze(-1) for cdfIi in cdfIs]
        theta_denominator = torch.sum(torch.stack(thetas), dim=0)
        theta_denominator[theta_denominator==0] = 1.0 # In case sdF*sdI==0
        theta = (1-zero_mask)*(cIF*numerator/theta_denominator)
        angle = positive_mask*phi + (1-positive_mask)*theta

        # Joint Entropy - jpdf
        jpdfupI = 0.5*(cdfF[:,0:1]+cdfI[:,0:1]-torch.abs(cdfF[:,0:1]-cdfI[:,0:1]))
        jpdfpI = angle*jpdfupI + (1-angle)*cdfF[:,0:1]*cdfI[:,0:1]
        jpdfloI = 0.5*(cdfF[:,0:1]+cdfI[:,0:1]-1+torch.abs(cdfF[:,0:1]+cdfI[:,0:1]-1))
        jpdfnI = angle*jpdfloI + (1-angle)*cdfF[:,0:1]*cdfI[:,0:1]
        jpdfI = positive_mask*jpdfpI + (1-positive_mask)*jpdfnI
        joint_entropy1 = cal_entropy(jpdfI)

        # Joint Entropy - 1D - F
        jpdfupI = 0.5*(cdfF+cdfI[:,0:1]-torch.abs(cdfF-cdfI[:,0:1]))
        jpdfupI = jpdfupI[:,1:] - jpdfupI[:,:-1]
        jpdfpIs = [angle*jpdfupI[:,i:i+1] + (1-angle)*pdfF[:,i+1:i+2]*pdfI[:,0:1] for i in range(window_size**2-1)]
        joint_entropy2s_pos = [cal_entropy(jpdfI) for jpdfI in jpdfpIs]
        joint_entropy2_pos = torch.sum(torch.stack(joint_entropy2s_pos), dim=0)
        jpdfloI = 0.5*(cdfF+cdfI[:,0:1]-1+torch.abs(cdfF+cdfI[:,0:1]-1))
        jpdfloI = jpdfloI[:,1:] - jpdfloI[:,:-1]
        jpdfpIs = [angle*jpdfloI[:,i:i+1] + (1-angle)*pdfF[:,i+1:i+2]*pdfI[:,0:1] for i in range(window_size**2-1)]
        joint_entropy2s_neg = [cal_entropy(jpdfI) for jpdfI in jpdfpIs]
        joint_entropy2_neg = torch.sum(torch.stack(joint_entropy2s_neg), dim=0)
        joint_entropy2 = positive_mask*joint_entropy2_pos + (1-positive_mask)*joint_entropy2_neg

        # Joint Entropy - 1D - I
        jpdfupI = 0.5*(cdfF[:,0:1]+cdfI-torch.abs(cdfF[:,0:1]-cdfI))
        jpdfupI = jpdfupI[:,1:] - jpdfupI[:,:-1]
        jpdfpIs = [angle*jpdfupI[:,i:i+1] + (1-angle)*pdfF[:,0:1]*pdfI[:,i+1:i+2] for i in range(window_size**2-1)]
        joint_entropy3s_pos = [cal_entropy(jpdfI) for jpdfI in jpdfpIs]
        joint_entropy3_pos = torch.sum(torch.stack(joint_entropy3s_pos), dim=0)

        jpdfloI = 0.5*(cdfF[:,0:1]+cdfI-1+torch.abs(cdfF[:,0:1]+cdfI-1))
        jpdfloI = jpdfloI[:,1:] - jpdfloI[:,:-1]
        jpdfpIs = [angle*jpdfloI[:,i:i+1] + (1-angle)*pdfF[:,0:1]*pdfI[:,i+1:i+2] for i in range(window_size**2-1)]
        joint_entropy3s_neg = [cal_entropy(jpdfI) for jpdfI in jpdfpIs]
        joint_entropy3_neg = torch.sum(torch.stack(joint_entropy3s_neg), dim=0)
        joint_entropy3 = positive_mask*joint_entropy3_pos + (1-positive_mask)*joint_entropy3_neg

        # Joint Entropy - 2D - I,F
        joint_entropy4 = torch.zeros_like(joint_entropy1)
        for i in range(1,window_size**2):
            for j in range(1,window_size**2):
                jpdf_up = 0.5 * (cdfF[:,i:i+1] + cdfI[:,j:j+1] - torch.abs(cdfF[:,i:i+1] - cdfI[:,j:j+1])) - \
                          0.5 * (cdfF[:,i-1:i] + cdfI[:,j:j+1] - torch.abs(cdfF[:,i-1:i] - cdfI[:,j:j+1])) - \
                          0.5 * (cdfF[:,i:i+1] + cdfI[:,j-1:j] - torch.abs(cdfF[:,i:i+1] - cdfI[:,j-1:j])) + \
                          0.5 * (cdfF[:,i-1:i] + cdfI[:,j-1:j] - torch.abs(cdfF[:,i-1:i] - cdfI[:,j-1:j]))
                jpdf_pos = angle * jpdf_up + (1 - angle) * pdfF[:,i:i+1] * pdfI[:,j:j+1]
                jpdf_lo = 0.5 * (cdfF[:,i:i+1] + cdfI[:,j:j+1] - 1 + torch.abs(cdfF[:,i:i+1] + cdfI[:,j:j+1] - 1)) - \
                          0.5 * (cdfF[:,i-1:i] + cdfI[:,j:j+1] - 1 + torch.abs(cdfF[:,i-1:i] + cdfI[:,j:j+1] - 1)) - \
                          0.5 * (cdfF[:,i:i+1] + cdfI[:,j-1:j] - 1 + torch.abs(cdfF[:,i:i+1] + cdfI[:,j-1:j] - 1)) + \
                          0.5 * (cdfF[:,i-1:i] + cdfI[:,j-1:j] - 1 + torch.abs(cdfF[:,i-1:i] + cdfI[:,j-1:j] - 1))
                jpdf_neg = angle * jpdf_lo + (1 - angle) * pdfF[:,i:i+1] * pdfI[:,j:j+1]
                jpdf = positive_mask * jpdf_pos + (1-positive_mask) * jpdf_neg
                joint_entropy4 += cal_entropy(jpdf)

        joint_entropy = joint_entropy1 + joint_entropy2 + joint_entropy3 + joint_entropy4
        # print('0',cIF[20:21,:])
        # print('1',(joint_entropy1)[20:21,:])
        # print('2',(joint_entropy1+joint_entropy2)[20:21,:])
        # print('3',(joint_entropy1+joint_entropy2+joint_entropy3)[20:21,:])
        # print('4',(joint_entropy1+joint_entropy2+joint_entropy3+joint_entropy4)[20:21,:])
        # print('je',joint_entropy[20:21,:])
        return joint_entropy
    
    jeAF = cal_jpdf(cAF,cdfA,cdfF,pdfA,pdfF,sdA,sdF)
    jeBF = cal_jpdf(cBF,cdfB,cdfF,pdfB,pdfF,sdB,sdF)

    # 特征互信息
    def cal_mi(eI,eF,jeIF,same):
        sumIF = eI+eF
        mi = sumIF - jeIF
        mi[sumIF==0] = 0.5
        sumIF[sumIF==0] = 1.0
        return 2*mi/sumIF

    #print(torch.cat((cal_mi(eA,eF,jeAF,sameAF),cal_mi(eB,eF,jeBF,sameBF),eA,eB,eF,jeAF,jeBF,eA+eF-jeAF,eB+eF-jeBF),dim=1)[:20,:])
    # print(torch.cat((cal_mi(eA,eF,jeAF,sameAF),cal_mi(eB,eF,jeBF,sameBF)),dim=1)[20:40,:])
    return torch.mean((cal_mi(eA,eF,jeAF,sameAF)+cal_mi(eB,eF,jeBF,sameBF))/2)

def fmi_approach_loss(A: torch.Tensor, F: torch.Tensor,
    feature: str = 'pixel', window_size: int = 3) -> torch.Tensor:
    return 1-fmi(A, A, F, feature, window_size)

@fusion_preprocessing
def fmi_metric(A: torch.Tensor, B: torch.Tensor, F: torch.Tensor,
    feature: str = 'pixel', window_size: int = 3) -> torch.Tensor:
    return fmi(A, B, F, feature, window_size)

@fusion_preprocessing
def fmi_p_metric(A: torch.Tensor, B: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    return fmi(A, B, F, feature='pixel', window_size=3)

@fusion_preprocessing
def fmi_w_metric(A: torch.Tensor, B: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    return fmi(A, B, F, feature='wavelet', window_size=3)

@fusion_preprocessing
def fmi_e_metric(A: torch.Tensor, B: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    return fmi(A, B, F, feature='edge', window_size=3)

@fusion_preprocessing
def fmi_d_metric(A: torch.Tensor, B: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    return fmi(A, B, F, feature='dct', window_size=3)

@fusion_preprocessing
def fmi_g_metric(A: torch.Tensor, B: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    return fmi(A, B, F, feature='gradient', window_size=3)

if __name__ == '__main__':
    from cslib.metrics.fusion import ir,vis,fused

    toy1 = torch.tensor([[[[1,1,1,1,1,1],
                           [1,0,0,0,0,0],
                           [2,1,0,0,0,0],
                           [2,1,0,0,0,0],
                           [2,1,0,0,0,0]]]])*0.5
    toy2 = torch.tensor([[[[1,1,1,1,1,1],
                           [1,0,0,0,1,1],
                           [2,1,0,0,0,0],
                           [2,1,0,0,0,2],
                           [2,1,0,0,0,0]]]])*0.5
    toy3 = torch.tensor([[[[1,2,1,2],
                           [0,2,0,2],
                           [1,0,1,0],
                           [0,0,1,1]]]])*0.5
    toy4 = torch.tensor([[[[0,0,1,2],
                           [2,2,0,1],
                           [2,0,1,1],
                           [1,1,2,2]]]])*0.5
    # print(f'FMI(pixel):{fmi(vis,vis,vis,feature="pixel")}')
    # print(f'FMI(pixel):{fmi(vis,vis,fused,feature="pixel")}')
    # print(f'FMI(pixel):{fmi(vis,vis,ir,feature="pixel")}')
    # print(f'FMI(wavelet):{fmi(vis,vis,vis,feature="wavelet")}')
    # print(f'FMI(wavelet):{fmi(vis,vis,fused,feature="wavelet")}')
    # print(f'FMI(wavelet):{fmi(vis,vis,ir,feature="wavelet")}')
    # print(f'FMI(gradient):{fmi(vis,vis,vis,feature="gradient")}')
    # print(f'FMI(gradient):{fmi(vis,vis,fused,feature="gradient")}')
    # print(f'FMI(gradient):{fmi(vis,vis,ir,feature="gradient")}')
    # print(f'FMI(pixel):{fmi(ir,vis,fused,feature="pixel")}')
    # print(f'FMI(wavelet):{fmi(vis,ir,fused,feature="wavelet")}')
    # print(f'FMI(dct):{fmi(vis,ir,fused,feature="dct")}')
    # print(f'FMI(edge):{fmi(vis,ir,fused,feature="edge")}')
    # print(f'FMI(gradient):{fmi(vis,ir,fused,feature="gradient")}')
    # fmi(toy1,toy1,toy2,feature="pixel")
    # print(toy3)
    # print(toy4)
    # # fmi(toy3,toy3,toy4,feature="pixel")
    # # fmi(toy1,toy1,toy2)
    # print(fmi(vis,ir,fused,feature="pixel"))
    print(fmi_metric(vis,ir,fused))
    # print(fmi_metric(ir,vis,fused))
