from typing import List
import torch
from .base import Base

__all__ = [
    'FSD',
]

class FSD(Base):
    """
    FSD (Filter Subtract Decimate) pyramid

    It can be regarded as a fast and improved version of the Laplacian pyramid.

    Reference:
        Hahn, M., & Samadzadegan, F. (2004, July). A study of image fusion techniques in remote sensing. 
        In Proc. 20th ISPRS Congress Geoimagery Bridging Continents (pp. 889-895).
    """
    def __init__(self,**kwargs) -> None:
        super().__init__("FSD",**kwargs)

    def decomposition_ordinary(self) -> List[torch.Tensor]:
        """
        Perform decomposition of the FSD pyramid using ordinary techniques.

        * Laplaian: Li = Gi - expand(subsample(gaussian_blur(Gi)))
        * FSD:      Li = Gi - gaussian_blur(Gi) <- simlified
        """
        fsd_pyramid = []
        for i in range(self.layer):
            fsd = self.gaussian[i] - self.gaussian_blur(self.gaussian[i])
            fsd_pyramid.append(fsd)

        self.pyramid = fsd_pyramid
        return fsd_pyramid

    def reconstruction_ordinary(self) -> torch.Tensor:
        """
        Same as Laplaian ordinary.
        """
        image_reconstructed = self.gaussian[-1]
        for i in reversed(range(self.layer)):
            _,_,m,n = self.pyramid[i].shape
            expanded = self.pyr_up(image_reconstructed)[:,:,:m,:n]
            image_reconstructed = self.pyramid[i] + expanded

        self.recon = image_reconstructed
        return self.recon


def main():
    # layer=5
    pyramid = FSD(image=ir)
    glance(pyramid.pyramid)
    glance([ir,pyramid.recon]) # One Bad point!

    # layer=3
    pyramid = FSD(image=ir,layer=3)
    glance(pyramid.pyramid)
    glance([ir,pyramid.recon]) # Many bad points!!!

    # layer=6
    pyramid = FSD(image=ir,layer=6)
    glance(pyramid.pyramid)
    glance([ir,pyramid.recon]) # No bad points~
    # Comment: bad, sacrifice quality for speed

if __name__ == '__main__':
    from cslib.metrics.fusion import ir,vis
    from cslib.utils import glance
    main()