from cslib.metrics.utils import fusion_preprocessing
import torch
import numpy as np

__all__ = [
    'scd','scd_tang',
    'scd_approach_loss',
    'scd_metric'
]

@fusion_preprocessing
def scd(A: torch.Tensor, B: torch.Tensor, F: torch.Tensor, eps: float = 1e-10) -> torch.Tensor:
    """
    Calculate the THE SUM OF THE CORRELATIONS OF DIFFERENCES (SCD) between three variables A, B, and F using PyTorch.

    Parameters:
    - A (torch.Tensor): Tensor representing variable A.
    - B (torch.Tensor): Tensor representing variable B.
    - F (torch.Tensor): Tensor representing variable F.
    - eps (float, optional): A small value to avoid numerical instability. Default is 1e-10.

    Returns:
    - torch.Tensor: THE SUM OF THE CORRELATIONS OF DIFFERENCES (SCD) value.

    This function computes the SCD between variables A, B, and F. SCD is calculated as the sum of two correlation coefficients:
    1. The correlation between (F - B) and A.
    2. The correlation between (F - A) and B.

    Reference: [1] ASLANTAS V, BENDES E. A new image quality metric for image fusion:
        The sum of the correlations of differences[J/OL]. AEU - International Journal
        of Electronics and Communications, 2015: 1890-1896. http://dx.doi.org/10.1016/j.aeue.2015.09.004.
        DOI:10.1016/j.aeue.2015.09.004.
    """
    def corr2(a, b):
        """
        Calculate the Pearson correlation coefficient between two tensors a and b.
        """
        a = a - torch.mean(a)
        b = b - torch.mean(b)
        r = torch.sum(a * b) / torch.sqrt(torch.sum(a * a) * torch.sum(b * b) + eps)
        return r

    # Calculate the SCD as the sum of two correlation coefficients
    return corr2(F - B, A) + corr2(F - A, B)

def scd_tang(A: np.ndarray, B: np.ndarray, F: np.ndarray) -> float:
    """
    Calculate the Symmetric Conditional Dependence (SCD) between three variables A, B, and F.

    Parameters:
    - A (numpy.ndarray): Array representing variable A.
    - B (numpy.ndarray): Array representing variable B.
    - F (numpy.ndarray): Array representing variable F.

    Returns:
    - float: Symmetric Conditional Dependence (SCD) value.

    This function computes the SCD between variables A, B, and F. SCD is calculated as the sum of two correlation coefficients:
    1. The correlation between (F - B) and A.
    2. The correlation between (F - A) and B.

    Author: Linfeng Tang
    Reference: https://zhuanlan.zhihu.com/p/611295921
    """
    def corr2(a, b):
        """
        Calculate the Pearson correlation coefficient between two arrays a and b.
        """
        a = a - np.mean(a)
        b = b - np.mean(b)
        r = np.sum(a * b) / np.sqrt(np.sum(a * a) * np.sum(b * b))
        return r

    # Calculate the SCD as the sum of two correlation coefficients
    return corr2(F - B, A) + corr2(F - A, B)

def scd_approach_loss(A: torch.Tensor, B: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    return -scd(A, B, F)

# 与 Tang 统一
scd_metric = scd

###########################################################################################

def main():
    from torchvision import transforms
    from torchvision.transforms.functional import to_tensor
    from PIL import Image

    torch.manual_seed(42)

    transform = transforms.Compose([transforms.ToTensor()])

    vis_image = Image.open('../imgs/TNO/vis/9.bmp')
    vis_array = np.array(vis_image).astype(np.int32)
    vis_tensor = to_tensor(vis_image).unsqueeze(0)
    ir_image = np.array(Image.open('../imgs/TNO/ir/9.bmp'))
    ir_array = np.array(ir_image).astype(np.int32)
    ir_tensor = to_tensor(ir_image).unsqueeze(0)
    fused_image = np.array(Image.open('../imgs/TNO/fuse/U2Fusion/9.bmp'))
    fused_array = np.array(fused_image).astype(np.int32)
    fused_tensor = to_tensor(fused_image).unsqueeze(0)

    print(f'SCD(ir,vis,fused) by Tang:{scd_tang(ir_array,vis_array,fused_array)}')      # 输入的是 0-255 的整数
    print(f'SCD(ir,vis,fused) by self:{scd(ir_tensor,vis_tensor,fused_tensor)}')        # 输入的是 0-1 的小数
    print(f'SCD(ir,ir,ir) by Tang:{scd_tang(ir_array,ir_array,ir_array)}')              # 输入的是 0-255 的整数
    print(f'SCD(ir,ir,ir) by self:{scd(ir_tensor,ir_tensor,ir_tensor)}')                # 输入的是 0-1 的小数
    print(f'SCD(vis,vis,vis) by Tang:{scd_tang(vis_array,vis_array,vis_array)}')        # 输入的是 0-255 的整数
    print(f'SCD(vis,vis,vis) by self:{scd(vis_tensor,vis_tensor,vis_tensor)}')          # 输入的是 0-1 的小数
    print(f'SCD(vis,vis,ir) by Tang:{scd_tang(vis_array,vis_array,ir_array)}')          # 输入的是 0-255 的小数
    print(f'SCD(vis,vis,ir) by self:{scd(vis_tensor,vis_tensor,ir_tensor)}')            # 输入的是 0-1 的小数
    print(f'SCD(vis,vis,fused) by Tang:{scd_tang(vis_array,vis_array,fused_array)}')    # 输入的是 0-255 的整数
    print(f'SCD(vis,vis,fused) by self:{scd(vis_tensor,vis_tensor,fused_tensor)}')      # 输入的是 0-1 的小数

if __name__ == '__main__':
    main()
