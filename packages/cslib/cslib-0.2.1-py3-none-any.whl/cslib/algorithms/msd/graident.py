from typing import List, Union
import torch
import torch.nn.functional as F
from .base import Base
from .laplacian import Laplacian

__all__ = [
    'Graident',
]

class Graident(Base):
    """
    Gradient pyramid
    """
    def __init__(self,**kwargs) -> None:
        super().__init__("Graident",**kwargs)

    @staticmethod
    def get_graident(image: Union[torch.Tensor, List[torch.Tensor]]) -> List[torch.Tensor]:
        """
        Compute gradients of the input image.

        Args:
            image (torch.Tensor or list): Input image tensor or list of tensors.

        Returns:
            list: List of gradient tensors.
        """
        if not isinstance(image, list):
            image = [image]*4
        h1 = torch.tensor([[0,0,0],[0, 1,-1],[0,0,0]], dtype=torch.float32)
        h2 = torch.tensor([[0,0,0],[0, 0,-1],[0,1,0]], dtype=torch.float32) / torch.sqrt(torch.tensor(2))
        h3 = torch.tensor([[0,0,0],[0,-1, 0],[0,1,0]], dtype=torch.float32)
        h4 = torch.tensor([[0,0,0],[0,-1, 0],[0,0,1]], dtype=torch.float32) / torch.sqrt(torch.tensor(2))
        h = [k.unsqueeze(0).unsqueeze(0).repeat(image[0].shape[1], 1, 1, 1).to(image[0].dtype) for k in [h1,h2,h3,h4]]
        return [F.conv2d(_i, _h, stride=1, padding=1, groups=_i.shape[1]) for _i,_h in zip(image,h)]

    def decomposition_ordinary(self) -> None:
        """
        Perform decomposition of the Gradient pyramid using ordinary techniques.

        This method computes the Gradient pyramid by applying Gaussian blur to each layer
        of the Gaussian pyramid, adding it back to the original layer, and then computing
        gradients.

        Returns:
            None
        """
        graident_pyramid = []
        for i in range(self.layer):
            temp = self.gaussian_blur(self.gaussian[i], kernel_size=3) + self.gaussian[i]
            graident_pyramid.append(self.get_graident(temp))
        self.pyramid = graident_pyramid

    def reconstruction_ordinary(self) -> None:
        """
        Perform reconstruction of the Gradient pyramid using ordinary techniques.

        This method reconstructs the image from the Gradient pyramid using ordinary
        reconstruction techniques, which involves computing the negative sum of gradients
        and adding it to an upsampled version of the reconstructed image.

        Returns:
            None
        """
        lp = Laplacian(image=self.image,auto=False,layer=self.layer)
        for i in range(self.layer):
            temp = torch.stack(self.get_graident(self.pyramid[i]))
            temp = -torch.sum(temp, dim=0) / 8
            pyramid = self.gaussian_blur(temp,kernel_size=3,bias=1) # change FSD to Laplacian
            lp.append(pyramid)
        lp.reconstruction()
        self.recon = lp.recon
