from typing import List, Union, Optional
import torch
import torch.nn.functional as F
from torchvision import transforms
import torchvision.transforms.functional as TF
from PIL import Image

__all__ = [
    'Base'
]

class Base(object):
    """
    Represents a pyramid constructed from an input image using Gaussian pyramid(Default).

    Attributes:
        name (str): Name of the pyramid.
        image (Union[str, torch.Tensor]): Input image as a filename (str) or tensor (torch.Tensor).
        pyramid (List[torch.Tensor]): List to store pyramid layers.
        layer (int): Number of layers in the pyramid.
        recon (torch.Tensor): Output image after reconstruction.
        auto (bool): Flag indicating whether to automatically construct and reconstruct the pyramid.
        down_way (str): Method used for downsampling during pyramid construction.
        up_way (str): Method used for upsampling during pyramid reconstruction.
        dec_way (str): Method used for decomposition.
        rec_way (str): Method used for reconstruction.
    """
    def __init__(self, name: str, **kwargs) -> None:
        """
        Initializes a Pyramid object.

        Args:
            name (str): Name of the pyramid.
            **kwargs: Additional keyword arguments to customize object attributes.

        Attributes:
            name (str): Name of the pyramid.
            image (Union[str, torch.Tensor]): Input image as a filename (str) or tensor (torch.Tensor).
            pyramid (List[torch.Tensor]): List to store pyramid layers.
            layer (int): Number of layers in the pyramid.
            recon (torch.Tensor): Output image after reconstruction.
            auto (bool): Flag indicating whether to automatically construct and reconstruct the pyramid.
            down_way (str): Method used for downsampling during pyramid construction.
            up_way (str): Method used for upsampling during pyramid reconstruction.
            dec_way (str): Method used for decomposition.
            rec_way (str): Method used for reconstruction.
        """
        self.name = name
        self.image = None # type: ignore
        self.pyramid = []
        self.layer = 5
        self.recon = None
        self.auto = True
        self.down_way = 'zero'        # Downsample method
        self.up_way = 'zero'          # Upsample method
        self.dec_way = 'ordinary'     # Decomposition method
        self.rec_way = 'ordinary'     # Reconstruction method
        self.gau_blur_way = 'Pytorch' # Gaussian kernel method

        # Update attributes based on additional keyword arguments
        for key, value in kwargs.items():
            setattr(self, key, value)

        # Default operations
        if self.image is not None:
           self.set_image(self.image)
        elif self.pyramid != []:
            # Auto Reconstruction for Output Image
            if self.auto:
                self.reconstruction()

    def gaussian_blur(
        self,
        image: torch.Tensor, 
        kernel_size: int = 5,
        gau_blur_way: str = 'Pytorch', 
        sigma: Optional[List[float]] = None, 
        bias: float = 0,
        current_layer: int = 0,
        total_layer: int =0,
    ) -> torch.Tensor:
        """
        Applies Gaussian blur to the input image.

        Args:
            image (torch.Tensor): Input image tensor of shape (batch_size, channels, height, width).
            kernel_size (int, optional): Size of the Gaussian kernel. Default is 5.
            gau_blur_way (str, optional): Method used for Gaussian blur. Options are 'Pytorch' and 'Paper'. Default is 'Paper'.
            sigma (List[float], optional): Standard deviation for the Gaussian kernel. Only used when `gau_blur_way` is 'Pytorch'. Default is None.
            bias (float, optional): Bias value added to the Gaussian kernel. Default is 0.

        Returns:
            torch.Tensor: Blurred image tensor.

        Raises:
            ValueError: If `kernel_size` is not 3 or 5 when `gau_blur_way` is 'Paper', or if `gau_blur_way` is not 'Pytorch' or 'Paper'.
        """
        if gau_blur_way == "Pytorch":
            return TF.gaussian_blur(image, kernel_size=[kernel_size, kernel_size], sigma=sigma)
        elif gau_blur_way == "Paper":
            # Define a Gaussian kernel
            if kernel_size == 3:
                kernel = torch.tensor([[1., 2., 1.],
                                       [2., 4., 2.],
                                       [1., 2., 1.]]) / 16 + bias
            elif kernel_size == 5:
                kernel = torch.tensor([[1., 4., 6., 4., 1.],
                                    [4., 16., 24., 16., 4.],
                                    [6., 24., 36., 24., 6.],
                                    [4., 16., 24., 16., 4.],
                                    [1., 4., 6., 4., 1.]]) / 256 + bias
            else:
                raise ValueError(f"kernel size in paper only be 3 or 5, not {kernel_size}")
            # Expand dimensions of the kernel for convolution
            kernel = kernel.unsqueeze(0).unsqueeze(0).to(image.dtype)

            # Adjust the kernel to match the number of channels in the input image
            kernel = kernel.expand(image.shape[1], -1, -1, -1)

            # Apply 2D convolution with the Gaussian kernel
            return F.conv2d(image, kernel, stride=1, padding=(kernel_size - 1) // 2, groups=image.shape[1])
        elif gau_blur_way == 'Adaptive':
            kernel_size = 2*(total_layer-current_layer+1) + 1
            sigma = [(kernel_size-1) / 6.0]
            # print(kernel_size,total_layer,current_layer,sigma)
            return TF.gaussian_blur(image, kernel_size=[kernel_size, kernel_size], sigma=sigma)
        else:
            raise ValueError(f"`gau_blur_way` should only be 'Pytorch', 'Adaptive' or 'Paper', not {gau_blur_way}.")

    def down_sample(self, image: torch.Tensor, dawn_sample_way: str = "Zero") -> torch.Tensor:
        """
        Downsamples the input image using specified method.

        Args:
            image (torch.Tensor): Input image tensor of shape (batch_size, channels, height, width).
            down_sample_way (str, optional): The method used for downsampling. Options are 'Max' for max pooling
                or 'Zero' for simple element removal. Defaults to 'Zero'.

        Returns:
            torch.Tensor: Downsampled image tensor.

        Raises:
            ValueError: If `down_sample_way` is not 'Max' or 'Zero'.
        """
        if dawn_sample_way == "Max":
            # Method 1. Subsample the image using 2x2 max pooling
            return F.max_pool2d(image, kernel_size=2, stride=2)
        elif dawn_sample_way == "Zero":
            # Method 2. Downsamples the input image by remove elements.
            return image[:, :, ::2, ::2]
        else:
            raise ValueError("`dawn_sample_way` should be 'Max' or 'Zero'")

    def up_sample(self, image: torch.Tensor) -> torch.Tensor:
        """
        Upsamples the input image using zero-padding.

        Args:
            image (torch.Tensor): Input image tensor of shape (batch_size, channels, height, width).

        Returns:
            torch.Tensor: Upsampled image tensor.
        """
        if self.up_way == "zero":
            batch_size, channels, height, width = image.size()
            padded_img = torch.zeros(batch_size, channels, 2 * height, 2 * width, device=image.device)
            padded_img[:, :, ::2, ::2] = image
        elif self.up_way == "bilinear":
            padded_img = F.interpolate(image, scale_factor=2, mode='bilinear', align_corners=False)
        return padded_img

    def pyr_down(self, image: torch.Tensor, **kwargs) -> torch.Tensor:
        """
        Downsamples the input image using Gaussian blur and max pooling.

        Args:
            image (torch.Tensor): Input image tensor of shape (batch_size, channels, height, width).

        Returns:
            torch.Tensor: Downsampled image tensor.
        """
        blurred = self.gaussian_blur(image, **kwargs)
        downsampled = self.down_sample(blurred)
        return downsampled

    def pyr_up(self, image: torch.Tensor) -> torch.Tensor:
        """
        Upsamples the input image using zero-padding and Gaussian blur.

        Args:
            image (torch.Tensor): Input image tensor of shape (batch_size, channels, height, width).

        Returns:
            torch.Tensor: Upsampled image tensor.
        """
        if self.up_way == "zero":
            padded_img = self.up_sample(image)
            blurred_img = self.gaussian_blur(padded_img)
            return blurred_img * 4
        elif self.up_way == "bilinear":
            return self.gaussian_blur(self.up_sample(image))
            return self.up_sample(image)

    def _build_gaussian_pyramid(self) -> None:
        """
        Constructs a Gaussian pyramid from the input image.
        """
        if self.image is None:
            raise ValueError("You should first assign a image.")
        image = self.image
        _, _, width, height = image.shape
        if self.layer > int(torch.floor(torch.log2(torch.tensor(min(width, height)))) - 2):
            raise RuntimeError('Cannot build {} levels, image too small.'.format(self.layer))
        self.gaussian = [image]
        for i in range(self.layer):
            image = self.pyr_down(
                image, gau_blur_way = self.gau_blur_way,
                current_layer = i+1, 
                total_layer = self.layer)
            self.gaussian.append(image)

    def _build_base_pyramid(self) -> None:
        """
        Builds the base (default Gaussian) pyramid from the input image.
        """
        self._build_gaussian_pyramid()

    def _init_after_change_image(self) -> None:
        """
        Initializes after set a image.
        """
        self._build_base_pyramid()

    def set_image(self, image: Union[torch.Tensor, str], auto: Optional[bool] = None) -> None:
        """
        Sets the input image for the pyramid and performs automatic decomposition and reconstruction if specified.

        Args:
            image (Union[torch.Tensor, str]): Input image as a tensor or filename.
            auto (Optional[bool]): Flag indicating whether to automatically decompose and reconstruct the pyramid. Default is None.
        """
        # Converts input image filename to tensor if necessary.
        if isinstance(image, str):
            transform = transforms.Compose([transforms.ToTensor()])
            self.image: torch.Tensor = TF.to_tensor(Image.open(image)).unsqueeze(0)

        assert self.image.dim() == 4, 'Image batch must be of shape [N,C,H,W]'

        # Build Base(Defaule Gaussian) Pyramid from input image
        self._init_after_change_image()

        # Auto Decomposition to Pyramid and Reconstruction for Output Image
        if auto is not None:
            self.auto = auto
        if self.auto:
            self.decomposition()
            self.reconstruction()

    def decomposition(self, method: Optional[str] = None) -> None:
        """
        Decomposes the image into pyramid layers based on the specified method.

        Args:
            method (str, optional): Method used for decomposition. Defaults to None.
        """
        if self.image is None:
            raise ValueError("No image to do decomposition!")
        if method is not None:
            self.dec_way = method
        if self.dec_way is not None:
            decomposition_method = getattr(self, f"decomposition_{self.dec_way}", None)
            if decomposition_method is not None and callable(decomposition_method):
                decomposition_method()
            else:
                raise ValueError(f"Invalid decomposition method (reconstruct_{self.dec_way}):", method)
        else:
            raise ValueError("No decomposition method specified")

    def reconstruction(self, method: Optional[str] = None) -> None:
        """
        Reconstructs the image from the pyramid layers based on the specified method.

        Args:
            method (str, optional): Method used for reconstruction. Defaults to None.
        """
        if method is not None:
            self.rec_way = method
        if self.rec_way is not None:
            reconstruct_method = getattr(self, f"reconstruction_{self.rec_way}", None)
            if reconstruct_method is not None and callable(reconstruct_method):
                reconstruct_method()
            else:
                raise ValueError(f"Invalid reconstruct method (reconstruct_{self.rec_way}):", method)
        else:
            raise ValueError("No reconstruct method specified")

    def __getitem__(self, index: Union[int, slice]) -> Union[torch.Tensor, List[torch.Tensor]]:
        """
        Get a layer or a subset of layers from the pyramid.

        Args:
            index (Union[int, slice]): Index or slice to select the layers.

        Returns:
            Union[torch.Tensor, List[torch.Tensor]]: Selected layer(s) from the pyramid.
        """
        return self.pyramid[index]

    def __setitem__(self, index: int, value: torch.Tensor) -> None:
        """
        Set a layer in the pyramid.

        Args:
            index (int): Index of the layer to be set.
            value (torch.Tensor): Tensor value to set the layer.
        """
        self.pyramid[index] = value

    def __len__(self) -> int:
        """
        Get the number of layers in the pyramid.

        Returns:
            int: Number of layers in the pyramid.
        """
        return len(self.pyramid)

    def append(self, item: torch.Tensor) -> None:
        """
        Appends a layer to the pyramid.

        Args:
            item (torch.Tensor): Pyramid layer tensor to append.
        """
        self.pyramid.append(item)


class Demo(Base):
    """
    Represents a demo class for showcasing pyramid development.

    This class inherits from the Base class and provides methods for decomposition and reconstruction
    of the pyramid using ordinary techniques.

    Attributes:
        Inherits attributes from the Base class.
    """

    def __init__(self, **kwargs) -> None:
        """
        Initializes a Demo object.

        Args:
            **kwargs: Additional keyword arguments to customize object attributes.

        Inherits attributes from the Base class.
        """
        # Add your own default params
        # self.layer = 5
        # self.dec_way = 'ordinary'  # Decomposition method
        # self.rec_way = 'ordinary'  # Reconstruction method

        # Do base default params
        super().__init__("Demo", **kwargs)

    # def _build_user_designed_base_pyramid(self) -> None:
    #     """
    #     Constructs your own pyramid from the input image.
    #     """
    #     if self.image is not None:
    #         pass
    #         # your own code
    #         #
    #         # Example: gaussian
    #         # image = self.image
    #         # self.gaussian = [image]
    #         # for _ in range(self.layer):
    #         #     image = self.pyr_down(image)
    #         #     self.gaussian.append(image)
    #     else:
    #         raise ValueError("You should first assign a image.")

    # @override
    # def _build_base_pyramid(self) -> None:
    #     """
    #     Builds the base (default Gaussian) pyramid from the input image.
    #     """
    #     # This is the default gaussian option
    #     self._build_gaussian_pyramid()
    #     # You can also change to your own base pyramid
    #     # self._build_user_designed_base_pyramid()
    #
    # @override
    # def _init_after_change_image(self) -> None:
    #     """
    #     Initializes after set a image.
    #     """
    #     self._build_base_pyramid()
    #     # You can do others after set an image

    def decomposition_ordinary(self) -> None:
        """
        Perform decomposition of the pyramid using ordinary techniques.

        This method is specific to Demo class and implements the decomposition process
        using ordinary techniques.
        """
        pass

    # def decomposition_your_method(self) -> None:
    #     """
    #     You can just change the name of funtion to adapt the `self.decom_way`
    #     """
    #     pass

    def reconstruction_ordinary(self) -> None:
        """
        Perform reconstruction of the pyramid using ordinary techniques.

        This method is specific to Demo class and implements the reconstruction process
        using ordinary techniques.
        """
        pass

    # def reconstruction_your_method(self) -> None:
    #     """
    #     You can just change the name of funtion to adapt the `self.recon_way`
    #     """
    #     pass

