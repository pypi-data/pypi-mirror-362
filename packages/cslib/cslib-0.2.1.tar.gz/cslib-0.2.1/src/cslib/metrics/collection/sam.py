from cslib.metrics.utils import fusion_preprocessing
import torch

__all__ = [
    'sam',
    'sam_approach_loss',
    'sam_metric'
]

def sam(src: torch.Tensor, dst: torch.Tensor) -> torch.Tensor:
    """
    Calculate the Spectral Angle Mapper (SAM) between two spectral vectors.

    Args:
        src (torch.Tensor): The source spectral vector tensor.
        dst (torch.Tensor): The destination spectral vector tensor.

    Returns:
        torch.Tensor: The SAM value between the two input spectral vectors.
    """
    # 计算张量的转置
    src_T = src.transpose(0, 1)
    dst_T = dst.transpose(0, 1)

    # 计算点积
    val = torch.dot(src_T.flatten(), dst_T.flatten()) / (torch.norm(src) * torch.norm(dst))

    # 计算 SAM
    sam = torch.acos(val)

    return sam

def sam_approach_loss(A: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    return torch.abs(sam(A,A)-sam(A,F))

@fusion_preprocessing
def sam_metric(A: torch.Tensor, B: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    return sam(A,F)+sam(B,F)

if __name__ == '__main__':
    from cslib.metrics.fusion import ir,vis,fused

    print(f'SAM:{sam_metric(vis, ir, fused)}')
    print(f'SAM:{sam_metric(vis, vis, vis)}')
    print(f'SAM:{sam_metric(vis, vis, fused)}')
    print(f'SAM:{sam_metric(vis, vis, ir)}')
