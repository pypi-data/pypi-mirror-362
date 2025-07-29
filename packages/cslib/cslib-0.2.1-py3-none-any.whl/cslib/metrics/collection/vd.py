import torch

###########################################################################################

__all__ = [
    'vd',
    'vd_approach_loss',
    'vd_metric'
]

def vd(A: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    """
    Compute the variance difference between two tensors A and F.

    Args:
        A (torch.Tensor): The Original Image.
        F (torch.Tensor): The Fused Image.

    Returns:
        torch.Tensor: The difference between the variances of A and F.

    """
    mA = torch.mean(A)
    mF = torch.mean(F)
    return (torch.mean(A**2) - mA**2) - (torch.mean(F**2) - mF**2)

def vd_approach_loss(A: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    return vd(A,F)

def vd_metric(A: torch.Tensor, B: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    return 0.5 * vd(A, F) + 0.5 * vd(B, F)

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

    print(f'VD(vis,ir):{vd(vis,ir)}')
    print(f'VD(vis,fused):{vd(vis,fused)}')
    print(f'VD(vis,vis):{vd(vis,vis)}')
    print(f'VD(fused,ir):{vd(fused,ir)}')
    print(f'VD(fused,vis):{vd(fused,vis)}')
    print(f'vd_metric(vis,ir,fused):{vd_metric(vis,ir,fused)}')

if __name__ == '__main__':
    main()
