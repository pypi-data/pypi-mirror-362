from typing import List
import torch
from .base import Base

__all__ = [
    'Contrust',
]

class Contrust(Base):
    """
    Contrast pyramid

    This class provides methods for decomposition and reconstruction of the Contrast pyramid
    using ordinary techniques.

    Reference:
        Toet, Alexander et al. “Merging thermal and visual images by a contrast pyramid.” 
        Optical Engineering 28 (1989): 789-792.
    """
    def __init__(self,**kwargs) -> None:
        super().__init__("Contrust",**kwargs)

    def decomposition_ordinary(self) -> List[torch.Tensor]:
        """
        Perform decomposition of the Contrast pyramid using ordinary techniques.

        This method computes the Contrast pyramid by dividing each layer of the Gaussian pyramid
        by the corresponding upsampled layer of the Gaussian pyramid, subtracting 1, and replacing
        zeros in the denominator with zeros.
        """
        laplacian_pyramid = []
        for i in range(self.layer):
            _,_,m,n = self.gaussian[i].shape
            expanded = self.pyr_up(self.gaussian[i+1])[:,:,:m,:n]
            laplacian = torch.where(expanded == 0, torch.zeros_like(self.gaussian[i]),\
                self.gaussian[i] / expanded - 1)
            laplacian_pyramid.append(laplacian)

        self.pyramid = laplacian_pyramid
        return self.pyramid

    def reconstruction_ordinary(self) -> torch.Tensor:
        """
        Perform reconstruction of the Contrast pyramid using ordinary techniques.

        This method reconstructs the image from the Contrast pyramid using ordinary reconstruction
        techniques, which involves multiplying each layer of the Contrast pyramid by the corresponding
        upsampled version of the reconstructed image, and then adding 1.
        """
        image_reconstructed = self.gaussian[-1]
        for i in reversed(range(self.layer)):
            _,_,m,n = self.pyramid[i].shape
            expanded = self.pyr_up(image_reconstructed)[:,:,:m,:n]
            image_reconstructed = (self.pyramid[i] + 1) * expanded

        self.recon = image_reconstructed
        return self.recon
