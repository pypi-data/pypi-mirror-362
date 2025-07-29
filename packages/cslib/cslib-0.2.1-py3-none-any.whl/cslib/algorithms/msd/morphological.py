from typing_extensions import override
import torch
import torch.nn.functional as F
from .base import Base

__all__ = [
    'Morphological',
]

class Morphological(Base):
    """
    Represents a pyramid constructed using morphological operations on an input image.

    Attributes:
        name (str): Name of the pyramid.
        image (torch.Tensor): Input image tensor.
        pyramid (List[torch.Tensor]): List to store pyramid layers.
        layer (int): Number of layers in the pyramid.
        recon (torch.Tensor): Output image after reconstruction.
        auto (bool): Flag indicating whether to automatically construct and reconstruct the pyramid.
        down_way (str): Method used for downsampling during pyramid construction.
    """
    def __init__(self,**kwargs) -> None:
        super().__init__("Morphological",**kwargs)

    @staticmethod
    def morph_dilation(image: torch.Tensor, kernel_size: int = 5) -> torch.Tensor:
        """
        Applies dilation operation to the input image.

        Args:
            image (torch.Tensor): Input image tensor.
            kernel_size (int): Size of the dilation kernel.

        Returns:
            torch.Tensor: Dilated image tensor.
        """
        # Define the kernel for dilation
        kernel = torch.ones((1, 1, kernel_size, kernel_size), dtype=torch.float32)

        # Perform dilation operation
        dilated_image = F.max_pool2d(image, kernel_size=kernel_size, stride=1, padding=kernel_size//2)

        return dilated_image

    @staticmethod
    def morph_erosion(image: torch.Tensor, kernel_size: int = 5) -> torch.Tensor:
        """
        Applies erosion operation to the input image.

        Args:
            image (torch.Tensor): Input image tensor.
            kernel_size (int): Size of the erosion kernel.

        Returns:
            torch.Tensor: Eroded image tensor.
        """
        # Define the kernel for erosion
        kernel = torch.ones((1, 1, kernel_size, kernel_size), dtype=torch.float32)

        # Perform erosion operation
        eroded_image = F.avg_pool2d(image, kernel_size=kernel_size, stride=1, padding=kernel_size//2)

        return eroded_image

    @staticmethod
    def morph_opening(image: torch.Tensor, kernel_size: int = 5) -> torch.Tensor:
        """
        Performs opening operation on the input image.

        Args:
            image (torch.Tensor): Input image tensor.
            kernel_size (int): Size of the kernel.

        Returns:
            torch.Tensor: Opened image tensor.
        """
        # Perform erosion followed by dilation (opening)
        eroded_image = Morphological.morph_erosion(image, kernel_size=kernel_size)
        opened_image = Morphological.morph_dilation(eroded_image, kernel_size=kernel_size)

        return opened_image

    @staticmethod
    def morph_closing(image: torch.Tensor, kernel_size: int = 5) -> torch.Tensor:
        """
        Performs closing operation on the input image.

        Args:
            image (torch.Tensor): Input image tensor.
            kernel_size (int): Size of the kernel.

        Returns:
            torch.Tensor: Closed image tensor.
        """
        # Perform dilation followed by erosion (closing)
        dilated_image = Morphological.morph_dilation(image, kernel_size=kernel_size)
        closed_image = Morphological.morph_erosion(dilated_image, kernel_size=kernel_size)

        return closed_image

    def _build_morphology_pyramid(self) -> None:
        """
        Constructs a Morphology pyramid from the input image.
        """
        if self.image is not None:
            image = self.image
            self.morphology = [image]
            for _ in range(self.layer):
                image  = self.morph_opening(image)
                image = self.morph_closing(image)
                image = self.down_sample(image)
                self.morphology.append(image)
        else:
            raise ValueError("You should first assign a image.")

    @override
    def _build_base_pyramid(self) -> None:
        self._build_morphology_pyramid()

    def decomposition_ordinary(self) -> None:
        """
        Performs ordinary decomposition of the pyramid.
        """
        morph_pyramid = []
        for i in range(self.layer):
            _,_,m,n = self.morphology[i].shape
            expanded = self.up_sample(self.morphology[i+1])[:,:,:m,:n]
            expanded = self.morph_closing(expanded)
            expanded = self.morph_opening(expanded)
            morph = self.morphology[i] - expanded
            morph_pyramid.append(morph)

        self.pyramid = morph_pyramid

    def reconstruction_ordinary(self) -> None:
        """
        Performs ordinary reconstruction of the pyramid.
        """
        image_reconstructed = self.morphology[-1]
        for i in reversed(range(self.layer)):
            _,_,m,n = self.pyramid[i].shape
            expanded = self.up_sample(image_reconstructed)[:,:,:m,:n]
            expanded = self.morph_closing(expanded)
            expanded = self.morph_opening(expanded)
            image_reconstructed = self.pyramid[i] + expanded

        self.recon = image_reconstructed

def main():
    pyramid = Morphological(image=ir)
    glance(pyramid.pyramid)
    glance([ir,pyramid.recon])
    # Comment: good

if __name__ == '__main__':
    from cslib.metrics.fusion import ir,vis
    from cslib.utils import glance
    main()