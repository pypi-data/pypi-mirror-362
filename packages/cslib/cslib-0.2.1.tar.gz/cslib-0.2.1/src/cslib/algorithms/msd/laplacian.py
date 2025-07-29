from typing import List
import torch
from cslib.algorithms.msd.base import Base

__all__ = [
    'Laplacian',
]

class Laplacian(Base):
    """
    Laplacian pyramid

    This class provides methods for decomposition and reconstruction of the Laplacian pyramid
    using ordinary and orthogonal techniques.

    Reference:
        P. Burt and E. Adelson, "The Laplacian Pyramid as a Compact Image Code," 
        in IEEE Transactions on Communications, vol. 31, no. 4, pp. 532-540, 
        April 1983, doi: 10.1109/TCOM.1983.1095851.
    """
    def __init__(self,**kwargs) -> None:
        super().__init__("Laplacian",**kwargs)

    def decomposition_ordinary(self) -> List[torch.Tensor]:
        """
        Perform decomposition of the Laplacian pyramid using ordinary techniques.

        This method computes the Laplacian pyramid by subtracting each layer of the Gaussian pyramid
        from the corresponding upsampled layer of the Gaussian pyramid.
        """
        laplacian_pyramid = []
        for i in range(self.layer):
            _,_,m,n = self.gaussian[i].shape
            expanded = self.pyr_up(self.gaussian[i+1])[:,:,:m,:n]
            laplacian = self.gaussian[i] - expanded
            laplacian_pyramid.append(laplacian)

        self.pyramid = laplacian_pyramid
        return self.pyramid

    def reconstruction_ordinary(self) -> torch.Tensor:
        """
        Perform reconstruction of the Laplacian pyramid using ordinary techniques.

        This method reconstructs the image from the Laplacian pyramid using ordinary reconstruction
        techniques, which involves adding each layer of the Laplacian pyramid to the corresponding
        upsampled version of the reconstructed image.
        """
        image_reconstructed = self.gaussian[-1]
        for i in reversed(range(self.layer)):
            _,_,m,n = self.pyramid[i].shape
            expanded = self.pyr_up(image_reconstructed)[:,:,:m,:n]
            image_reconstructed = self.pyramid[i] + expanded

        self.recon = image_reconstructed
        return self.recon

    def reconstruction_orthogonal(self) -> torch.Tensor:
        """
        Perform reconstruction of the Laplacian pyramid using orthogonal techniques.

        This method reconstructs the image from the Laplacian pyramid using orthogonal reconstruction
        techniques, which involves subtracting each downsampled version of the Laplacian pyramid from
        the reconstructed image, and then adding each layer of the Laplacian pyramid to the corresponding
        upsampled version of the reconstructed image.

        Reference:
        M. N. Do and M. Vetterli, "Framing pyramids," in IEEE Transactions on Signal Processing, 
        vol. 51, no. 9, pp. 2329-2342, Sept. 2003, doi: 10.1109/TSP.2003.815389.
        """
        image_reconstructed = self.gaussian[-1]
        for i in reversed(range(self.layer)):
            _,_,m,n = self.pyramid[i].shape
            image_reconstructed -= self.pyr_down(self.pyramid[i])
            expanded = self.pyr_up(image_reconstructed)[:,:,:m,:n]
            image_reconstructed = self.pyramid[i] + expanded

        self.recon = image_reconstructed
        return self.recon
