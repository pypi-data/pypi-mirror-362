import torch
import torch.nn.functional as F

###########################################################################################

__all__ = [
    'eme',
    'eme_approach_loss',
    'eme_metric'
]

def eme(x: torch.Tensor, block_size: int = 16) -> torch.Tensor:
    """
    Calculate the Energy of Maxima to Minima Ratio (EME) for an input tensor.

    Parameters:
    - x (torch.Tensor): Input tensor.
    - block_size (int): Size of the blocks for max pooling.

    Returns:
    - torch.Tensor: EME value or tensor of EME values.
    """
    _max = torch.nn.functional.max_pool2d(x, block_size)
    _min = -torch.nn.functional.max_pool2d(-x, block_size)
    eme = torch.log10(_max[(_max*_min)!=0] / _min[(_max*_min)!=0])
    return torch.mean(20.0 * eme)

eme_approach_loss = eme

def eme_metric(A: torch.Tensor, B: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    return eme(F)

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

    print(f'EME(ir):{eme(ir)}')
    print(f'EME(vis):{eme(vis)}')
    print(f'EME(fused):{eme(fused)}')

if __name__ == '__main__':
    main()
