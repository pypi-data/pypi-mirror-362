from cslib.metrics.utils import fusion_preprocessing
import torch

__all__ = [
    'pfe',
    'pfe_approach_loss',
    'pfe_metric'
]

def pfe(I: torch.Tensor, F: torch.Tensor, eps: float = 1e-10) -> torch.Tensor:
    """
    Calculate the Percentage Fit Error (PFE) between two images.

    Args:
        I (torch.Tensor): The reference image tensor.
        F (torch.Tensor): The fused image tensor.
        eps (float, optional): A small value to avoid numerical instability. Default is 1e-10.

    Returns:
        torch.Tensor: The PFE between fused and reference values.

    Reference:
        Naidu V P S. Discrete cosine transform-based image fusion[J]. 
        Defence Science Journal, 2010, 60(1): 48.
    """
    # Compute the difference between the two images
    D = I - F

    # Compute the norm of the difference and the reference image
    norm_diff = torch.norm(D.view(D.shape[0], -1), dim=1, p=2)
    norm_ref = torch.norm(I.view(I.shape[0], -1), dim=1, p=2)

    # Avoid division by zero
    norm_ref[norm_ref == 0] = eps

    # Compute the PFE
    pfe = (norm_diff / norm_ref) * 100

    return pfe.mean()  # Return the mean PFE across all images in the batch

pfe_approach_loss = pfe

@fusion_preprocessing
def pfe_metric(A: torch.Tensor, B: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    w0 = w1 = 0.5
    return w0 * pfe(A, F) + w1 * pfe(B, F)

if __name__ == '__main__':
    from cslib.metrics.fusion import ir,vis,fused
    print(f'PFE(ir,ir):{pfe(ir,ir)}')
    print(f'PFE(ir,fused):{pfe(ir,fused)}')
    print(f'PFE(ir,vis):{pfe(ir,vis)}')
    print(f'PFE metrics:{pfe_metric(ir,vis,fused)}')
