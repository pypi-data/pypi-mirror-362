import torch

###########################################################################################

__all__ = [
    'ncc',
    'ncc_approach_loss',
    'ncc_metric'
]

def ncc(A: torch.Tensor, B: torch.Tensor) -> torch.Tensor:
    """
    Compute the Normalized Cross Correlation (NCC) between two tensors A and B.

    Args:
        A (torch.Tensor): The first tensor.
        B (torch.Tensor): The second tensor.

    Returns:
        float: The NCC value between A and B.
    """
    return torch.sum(A*B)/torch.sum(A*A)

def ncc_approach_loss(A: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    return 1-ncc(A,F)

def ncc_metric(A: torch.Tensor, B: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    return 0.5 * ncc(A, F) + 0.5 * ncc(B, F)

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

    print(f'NCC(vis,ir):{ncc(vis,ir)}')
    print(f'NCC(vis,fused):{ncc(vis,fused)}')
    print(f'NCC(vis,vis):{ncc(vis,vis)}')
    print(f'NCC(fused,ir):{ncc(fused,ir)}')
    print(f'NCC(fused,vis):{ncc(fused,vis)}')
    print(f'NCC_metric(vis,ir,fused):{ncc_metric(vis,ir,fused)}')

if __name__ == '__main__':
    main()
