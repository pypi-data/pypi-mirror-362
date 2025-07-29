from cslib.metrics.utils import fusion_preprocessing
import torch
import kornia

__all__ = [
    'pww',
    'pww_approach_loss',
    'pww_metric'
]

def pww(A: torch.Tensor, B: torch.Tensor, F: torch.Tensor, N: int = 2, alpha1: float = 2.0/3, alpha2: float = 1.0/3) -> torch.Tensor:
    """
    This function implements Pei-Wei Wang's algorithms for fusion metric.

    Args:
        A: First input image.
        B: Second input image.
        F: Fused image.
        N: Decomposition level (default = 2).
        alpha1: Weight for the first decomposition level (default = 2/3).
        alpha2: Weight for the second decomposition level (default = 1/3).

    Returns:
        res: Metric value.

    Reference:
        A novel image fusion metric based on multi-scale analysis, 
        pp.965-968, ICSP 2008.
    """
    def corrDn(I,filt,step,start): # 因为 Haar 的形状确定了，所以 stag 也确定了 为 2
        # matlab的 reflect 是在最前边的反转，pyhton 的是在最后边的反转，只能采取手动 padding
        temp = kornia.filters.filter2d(torch.cat((I[1:2,:],I),dim=0).unsqueeze(0).unsqueeze(0),filt,padding='valid')
        return (temp.squeeze(0).squeeze(0))[start[0]::step[0],start[1]::step[1]]

    def build_wpyr(I,ht):
        # matlab 参数 filter : haar
        # matlab 参数 edges : reflect1
        m,n = I.shape
        if ht <= 0:
            pyr = I.T.reshape((m*n,1))
            pind = torch.tensor(I.shape).unsqueeze(0)
            return pyr, pind

        filt = torch.sqrt(torch.tensor([[[1],[1]]]) / 2.0)  # Haar filter
        # kernel = [1 1]' / sqrt(2); % matlab code
        hfilt = torch.tensor([[[-1],[1]]]) * filt # Simplified for Haar
        # hfilt = modulateFlip(filt); % matlab code, modulate by (-1)^n
        # % Reverse order of taps in filt, to do correlation instead of convolution
        # filt = filt(size(filt,1):-1:1,size(filt,2):-1:1);

        if n==1:
            lolo = corrDn(I,filt,step=(2,1),start=(1,0))
            # lolo = corrDn(im, filt, edges, [2 1], [stag 1]);
            hihi = corrDn(I,hfilt,step=(2,1),start=(1,0))
            # hihi = corrDn(im, hfilt, edges, [2 1], [2 1]);
        elif m==1:
            lolo = corrDn(I.T,filt,step=(2,1),start=(1,0)).T
            # lolo = corrDn(im, filt', edges, [1 2], [1 stag]);
            hihi = corrDn(I.T,hfilt,step=(2,1),start=(1,0)).T
            # hihi = corrDn(im, hfilt', edges, [1 2], [1 2]);
        else:
            lo = corrDn(I,filt,step=(2,1),start=(1,0))
            # lo = corrDn(im, filt, edges, [2 1], [stag 1]);
            hi = corrDn(I,hfilt,step=(2,1),start=(1,0))
            # hi = corrDn(im, hfilt, edges, [2 1], [2 1]);
            lolo = corrDn(lo.T,filt,step=(2,1),start=(1,0)).T
            # lolo = corrDn(lo, filt', edges, [1 2], [1 stag]);
            lohi = corrDn(hi.T,filt,step=(2,1),start=(1,0)).T
            # lohi = corrDn(hi, filt', edges, [1 2], [1 stag]); % horizontal
            hilo = corrDn(lo.T,hfilt,step=(2,1),start=(1,0)).T
            # hilo = corrDn(lo, hfilt', edges, [1 2], [1 2]); % vertical
            hihi = corrDn(hi.T,hfilt,step=(2,1),start=(1,0)).T # 这步和 matlab 有不一样了
            # hihi = corrDn(hi, hfilt', edges, [1 2], [1 2]); % diagonal

        (npyr, nind) = build_wpyr(lolo,ht-1)

        if m==1 or n==1:
            pyr = torch.cat((hihi.T.reshape((-1,1)),npyr),dim=0)
            # pyr = [hihi(:); npyr];
            pind = torch.tensor(hihi.shape).unsqueeze(0)
            pind = torch.cat((pind,nind),dim=0)
            # pind = [size(hihi); nind];
        else:
            pyr = torch.cat((lohi.T.reshape((-1,1)),hilo.T.reshape((-1,1)),hihi.T.reshape((-1,1)),npyr),dim=0)
            # pyr = [lohi(:); hilo(:); hihi(:); npyr];
            pind1 = torch.tensor(lohi.shape).unsqueeze(0)
            pind2 = torch.tensor(hilo.shape).unsqueeze(0)
            pind3 = torch.tensor(hihi.shape).unsqueeze(0)
            pind = torch.cat((pind1,pind2,pind3,nind),dim=0)
            # pind = [size(lohi); size(hilo); size(hihi); nind];

        return pyr, pind

    def pyrBand(pyr, pind, band):
        if band > pind.size(0) or band < 1:
            raise ValueError(f"BAND_NUM must be between 1 and number of pyramid bands ({pind.size(0)}).")

        if pind.size(1) != 2:
            raise ValueError("INDICES must be an Nx2 matrix indicating the size of the pyramid subbands.")

        ind = 0
        for l in range(band - 1):
            ind += torch.prod(pind[l])

        start_idx = ind
        end_idx = ind + torch.prod(pind[band - 1]) - 1
        indices = torch.arange(start_idx, end_idx + 1) # type: ignore

        # print(torch.mean(pyr[indices].reshape(pind[band-1, 0], pind[band-1, 1]).T))
        return pyr[indices].reshape(pind[band-1, 0], pind[band-1, 1]).T

    # 1. wavelet decomposition
    (CA, SA) = build_wpyr(A.squeeze(0).squeeze(0),N)
    (CB, SB) = build_wpyr(B.squeeze(0).squeeze(0),N)
    (CF, SF) = build_wpyr(F.squeeze(0).squeeze(0),N)
    # print(torch.mean(CA),torch.sum(SA))
    # print(torch.mean(CB),torch.sum(SB))
    # print(torch.mean(CF),torch.sum(SF))

    # 2. caculate the metric
    Qep = []
    for i in range(N):
        bandNum = i*3
        HA = pyrBand(CA, SA, bandNum+1)
        VA = pyrBand(CA, SA, bandNum+2)
        DA = pyrBand(CA, SA, bandNum+3)

        HB = pyrBand(CB, SB, bandNum+1)
        VB = pyrBand(CB, SB, bandNum+2)
        DB = pyrBand(CB, SB, bandNum+3)

        HF = pyrBand(CF, SF, bandNum+1)
        VF = pyrBand(CF, SF, bandNum+2)
        DF = pyrBand(CF, SF, bandNum+3)

        WA = HA**2 + VA**2 + DA**2
        WB = HB**2 + VB**2 + DB**2
        # print('WA',torch.mean(WA))
        # print('WB',torch.mean(WB))

        EPA = torch.exp(-torch.abs(HA-HF)) + torch.exp(-torch.abs(VA-VF)) + torch.exp(-torch.abs(DA-DF))
        EPB = torch.exp(-torch.abs(HB-HF)) + torch.exp(-torch.abs(VB-VF)) + torch.exp(-torch.abs(DB-DF))
        # print('EPA',torch.mean(EPA))
        # print('EPB',torch.mean(EPB))

        Qep.append(torch.sum(EPA*WA+EPB*WB) / torch.sum(WA+WB))

    return Qep[0]**alpha1 * Qep[1]**alpha2


def pww_approach_loss(A: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    return 3.0 - pww(A,A,F)

@fusion_preprocessing
def pww_metric(A: torch.Tensor, B: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    return pww(A*255.0,B*255.0,F*255.0)

if __name__ == '__main__':
    from cslib.metrics.fusion import ir,vis,fused

    # toy = torch.tensor([[[[1,2],[3,4],[5,6]]]])
    # toy = torch.tensor([[[[1],[2],[3],[4]]]])*1.0
    # toy = torch.tensor([[[[1,2,3,4]]]])*1.0
    toy = torch.tensor([[[[1,2,3,4],[5,6,7,8],[2,4,6,8],[1,3,5,7]]]])*1.0

    print(f'PWW:{pww_metric(vis, ir, fused)}')
    print(f'PWW:{pww_metric(vis, vis, vis)}')
    print(f'PWW:{pww_metric(vis, vis, fused)}')
    print(f'PWW:{pww_metric(vis, vis, ir)}')
    print(f'PWW:{pww(toy,toy,toy)}')
