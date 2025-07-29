import torch
import kornia

__all__ = [
    'q_h',
    'q_h_approach_loss',
    'q_h_metric'
]

def q_h(A: torch.Tensor, B: torch.Tensor, F: torch.Tensor, window_size: int = 7) -> torch.Tensor:
    """
    Calculates the Hossny's fusion metric between two input images A and B
    with respect to a fused image F.

    Args:
        A (torch.Tensor): The first input image tensor.
        B (torch.Tensor): The second input image tensor.
        F (torch.Tensor): The fused image tensor.
        window_size (int, optional): The size of the local window. Default is 7.

    Returns:
        torch.Tensor: The Hossny's fusion metric value.
    
    Reference:
        Hossny, M., Nahavandi, S., Crieghton, D. (2008). Feature-Based Image Fusion Quality Metrics. 
        In: Xiong, C., Huang, Y., Xiong, Y., Liu, H. (eds) Intelligent Robotics and Applications. 
        ICIRA 2008. Lecture Notes in Computer Science(), vol 5314. Springer, Berlin, Heidelberg. 
        https://doi.org/10.1007/978-3-540-88513-9_51
    """
    # 展开
    _, _, m, n = A.shape
    w = int((window_size+1)/2-1)
    def unfolded_image(I):
        unfolded = torch.nn.functional.unfold(I, (m-2*w,n-2*w), stride=1)
        return unfolded.view(unfolded.size(0), unfolded.size(1), -1).squeeze(0)  # 将展平的张量重新变形为窗口数据
    [uA, uB, uF] = [unfolded_image(I*255.0) for I in [A, B, F]]

    # 计算直方图
    def calculate_hist(I):
        # Old
        # cdf = torch.ones(8,I.shape[0])
        # for i in range(8):
        #     cdf[i,:] = ((I > -0.5+i) & (I <= 0.5+i)).sum(dim=1)
        # cdf = cdf.T
        # New
        bin = torch.arange(-0.5, 255.5).unsqueeze(-1).unsqueeze(-1)
        cdf = ((I > bin[:-1,...]) & (I <= bin[1:,...])).sum(dim=2).T
        return cdf / window_size**2
    [PDFA, PDFB, PDFF] = [calculate_hist(I) for I in [uA, uB, uF]]

    # 计算熵
    def calculate_entropy(pdf):
        entropy = torch.ones_like(pdf) * 0.0
        index = (pdf!=0)
        entropy[index] = pdf[index] * torch.log2(pdf[index])
        return -entropy.sum(dim=1).unsqueeze(-1)
    [ENA, ENB, ENF] = [calculate_entropy(PDF) for PDF in [PDFA, PDFB, PDFF]]

    # 重新折叠成原来的形状
    def folded_image(I):
        return I.view(1,1,m-2*w,n-2*w)
    [ENA, ENB, ENF] = [folded_image(ENI) for ENI in [ENA, ENB, ENF]]

    # importance map
    PA = ENA / torch.max(ENA)
    PB = ENB / torch.max(ENB)
    PA = PA[..., w:-w, w:-w]
    PB = PB[..., w:-w, w:-w]

    # SSIM
    def calculate_ssim(X,Y):
        C1 = (0.01*255)**2
        C2 = (0.03*255)**2
        kernel = kornia.filters.get_gaussian_kernel1d(window_size, 1.5, device=X.device, dtype=X.dtype)
        muX = kornia.filters.filter2d_separable(X, kernel, kernel, padding="valid")
        muY = kornia.filters.filter2d_separable(Y, kernel, kernel, padding="valid")
        sXX = kornia.filters.filter2d_separable(X**2, kernel, kernel, padding="valid") - muX**2
        sYY = kornia.filters.filter2d_separable(Y**2, kernel, kernel, padding="valid") - muY**2
        sXY = kornia.filters.filter2d_separable(X*Y, kernel, kernel, padding="valid") - muX*muY
        return  ((2*muX*muY + C1)*(2*sXY + C2)) / ((muX**2 + muY**2 + C1)*(sXX + sYY + C2))
    mapAF = calculate_ssim(ENA, ENF)
    mapBF = calculate_ssim(ENB, ENF)

    EAF = mapAF * PA
    EBF = mapBF * PB

    ENA = ENA[..., w:-w, w:-w]
    ENB = ENB[..., w:-w, w:-w]
    sum_s = ENA + ENB
    r = torch.ones_like(ENA) * 0.5
    index = (sum_s != 0)
    r[index] = ENA[index] / sum_s[index]
    return torch.mean(1 - r*mapAF - (1-r)*mapBF)
    # 这里好像不用乘 c
    # 结果不用惊讶，就是 0.0 几
    # 运算慢的惊人，我已经尽力了
    # 滑动窗口每一个窗口都算信息熵。。。


def q_h_approach_loss(A: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    return q_h(A,A,F)

def q_h_metric(A: torch.Tensor, B: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    return q_h(A, B, F)

def main():
    from cslib.metrics.fusion import vis,ir,fused

    print(f'Q_H(vis,ir,fused):{q_h(vis,ir,fused)}')
    print(f'Q_H(vis,vis,vis):{q_h(vis,vis,vis)}')
    print(f'Q_H(vis,vis,fused):{q_h(vis,vis,fused)}')
    print(f'Q_H(vis,vis,ir):{q_h(vis,vis,ir)}')

    # toy = torch.tensor([[[[1,1,2,2,3],[2,2,3,3,4],[3,3,4,4,5],[4,4,5,5,6],[5,5,6,6,7]]]])/255.0
    # print(f'Q_H(vis,ir,fused):{q_h(toy,toy,toy,window_size=3)}')

if __name__ == '__main__':
    main()
