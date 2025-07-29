from cslib.metrics.utils import fusion_preprocessing
import torch
from torchmetrics.functional.image import spatial_correlation_coefficient as scc
# https://lightning.ai/docs/torchmetrics/stable/image/spatial_correlation_coefficient.html

__all__ = [
    'scc',
    'scc_approach_loss',
    'scc_metric'
]

def scc_approach_loss(A: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    return 1-scc(A,F)

@fusion_preprocessing
def scc_metric(A: torch.Tensor, B: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    return 0.5 * scc(A, F) + 0.5 * scc(B, F)

if __name__ == '__main__':
    from cslib.metrics.fusion import ir,vis,fused
    print(f'SCC(vis,ir):{scc(vis,ir)}')
    print(f'SCC(vis,vis):{scc(vis,vis)}')
    print(f'SCC(vis,fused):{scc(vis,fused)}')
    print(f'SCC(ir,fused):{scc(ir,fused)}')
    print(f'SCC_metric(vis,ir,fused):{scc_metric(vis,ir,fused)}')
