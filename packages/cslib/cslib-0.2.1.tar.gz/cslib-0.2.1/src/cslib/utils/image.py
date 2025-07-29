"""
IO Utilities for Handling Images and Tensors

This module provides a set of functions for displaying images, 
converting between PyTorch tensors and NumPy arrays, 
and saving arrays as MATLAB .mat files.
"""

from typing import Union, Optional, TypeVar
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from PIL import Image
import torch
from scipy.io import savemat
from pathlib import Path
from torchvision.transforms import ToTensor
from skimage import color


__all__ = [
    'to_tensor',
    'to_image',
    'to_numpy',
    'glance',
    'path_to_gray',
    'path_to_rgb',
    'rgb_to_gray',
    'gray_to_rgb',
    'path_to_ycbcr',
    'rgb_to_ycbcr',
    'ycbcr_to_rgb',
    'save_array_to_img',
    'save_array_to_mat',
]


CLIP_MIN = 0.0
CLIP_MAX = 1.0


ImageType = TypeVar('ImageType', np.ndarray, torch.Tensor, Image.Image)


def _clip(image: ImageType) -> ImageType:
    if isinstance(image, np.ndarray):
        return image.clip(min=CLIP_MIN, max=CLIP_MAX)
    if isinstance(image, torch.Tensor):
        return image.clamp(min=CLIP_MIN, max=CLIP_MAX)
    if isinstance(image, Image.Image):
        return image


def _tensor_to_numpy(image: torch.Tensor) -> np.ndarray:
    if len(image.shape) == 4:
        if image.shape[0] != 1:
            raise ValueError("Batch number should be 1.")
        image = image[0,:,:,:]
    if len(image.shape) == 3:
        image = image.permute(1, 2, 0)
        if image.shape[-1] == 1:
            image = image[:,:,0]
    elif len(image.shape) != 2:
        raise ValueError("Image should be an image.")
    return image.detach().cpu().numpy()
    

def _tensor_to_image(image: torch.Tensor) -> Image.Image:
    image_array = _tensor_to_numpy(image)
    return _numpy_to_image(image_array)


def _image_to_numpy(image: Image.Image) -> np.ndarray:
    return np.array(image)/255.0


def _image_to_tensor(image: Image.Image, dtype: torch.dtype) -> torch.Tensor:
    return (ToTensor()(image).to(dtype))/255.0


def _numpy_to_image(image: np.ndarray) -> Image.Image:
    image = image * 255.0
    if len(image.shape) == 2:
        return Image.fromarray(image.astype(np.uint8), mode="L")
    else:
        return Image.fromarray(image.astype(np.uint8), mode="RGB") 


def _numpy_to_tensor(image: np.ndarray, dtype: torch.dtype) -> torch.Tensor:
    return (ToTensor()(image)).to(dtype)


def to_tensor(
        image: ImageType, 
        clip: bool = False,
        dtype: torch.dtype = torch.float32
    ) -> torch.Tensor:
    if isinstance(image, np.ndarray):
        tensor = _numpy_to_tensor(image, dtype)
    elif isinstance(image, Image.Image):
        tensor = _image_to_tensor(image, dtype)
    elif isinstance(image, torch.Tensor):
        tensor = image
    return _clip(tensor) if clip else tensor


def to_numpy(
        image: ImageType,
        clip: bool = False
    ) -> np.ndarray:
    if isinstance(image, torch.Tensor):
        array = _tensor_to_numpy(image)
    elif isinstance(image, Image.Image):
        array = _image_to_numpy(image)
    elif isinstance(image, np.ndarray):
        array = image
    return _clip(array) if clip else array


def to_image(
        image: ImageType,
        clip: bool = False
    ) -> Image.Image:
    if isinstance(image, np.ndarray):
        array = _clip(image) if clip else image
        return _numpy_to_image(array)
    elif isinstance(image, torch.Tensor):
        tensor = _clip(image) if clip else image
        return _tensor_to_image(tensor)
    return image


def gray_to_rgb(image: ImageType) -> ImageType:
    if isinstance(image, np.ndarray):
        return color.gray2rgb(image)
    elif isinstance(image, Image.Image):
        return image.convert('RGB')
    else:
        assert 1 < image.ndim < 5
        if image.ndim == 2:
            return image.unsqueeze(0).repeat(3, 1, 1)
        else:
            assert(image.shape[-3] == 1)
            return image.repeat(1, 3, 1, 1) if image.ndim == 4 else image.repeat(3, 1, 1)


def rgb_to_gray(image: ImageType) -> ImageType:
    if isinstance(image, np.ndarray):
        return color.rgb2gray(image)
    elif isinstance(image, Image.Image):
        return image.convert('L')
    else:
        assert image.ndim in [3, 4], "Input must be a 3-channel RGB image or a batch of 3-channel RGB images."
        assert image.shape[-3] == 3, "Input must have 3 channels for RGB."
        coeffs = torch.tensor([0.2125, 0.7154, 0.0721], dtype=image.dtype, device=image.device)
        if image.ndim == 4:
            return (image * coeffs.view(1, 3, 1, 1)).sum(dim=1, keepdim=True)
        else:
            return (image * coeffs.view(3, 1, 1)).sum(dim=0, keepdim=True)


def rgb_to_ycbcr(image: ImageType) -> ImageType:
    if isinstance(image, np.ndarray):
        return color.rgb2ycbcr(image)
    elif isinstance(image, Image.Image):
        return image.convert('YCbCr')
    else:
        assert image.ndim in [3, 4], "Input must be a 3-channel RGB image or a batch of 3-channel RGB images."
        assert image.shape[-3] == 3, "Input must have 3 channels for RGB."
        rgb_to_ycbcr_matrix = torch.tensor([
            [65.481, 128.553, 24.966], [-37.797, -74.203, 112.0], [112.0, -93.786, -18.214]
        ], dtype=image.dtype, device=image.device)
        offset = torch.tensor([16, 128, 128], dtype=image.dtype, device=image.device)
        if image.ndim == 4:
            return torch.einsum('nchw,cd->ndhw', image, rgb_to_ycbcr_matrix.T) + offset.view(1, 3, 1, 1)
        else:
            return torch.einsum('chw,cd->dhw', image, rgb_to_ycbcr_matrix.T) + offset.view(3, 1, 1)


def ycbcr_to_rgb(image: ImageType) -> ImageType:
    if isinstance(image, np.ndarray):
        return color.ycbcr2rgb(image)
    elif isinstance(image, Image.Image):
        return image.convert('RGB')
    else:
        assert image.ndim in [3, 4], "Input must be a 3-channel RGB image or a batch of 3-channel RGB images."
        assert image.shape[-3] == 3, "Input must have 3 channels for RGB."
        ycbcr_to_rgb_matrix = torch.tensor([
            [65.481, 128.553, 24.966], [-37.797, -74.203, 112.0], [112.0, -93.786, -18.214]
        ], dtype=image.dtype, device=image.device).inverse()
        offset = torch.tensor([-16, -128, -128], dtype=image.dtype, device=image.device)
        if image.ndim == 4:
            return (torch.einsum('nchw,cd->ndhw', image + offset.view(1, 3, 1, 1), ycbcr_to_rgb_matrix.T))
        else:
            return (torch.einsum('chw,cd->dhw', image + offset.view(3, 1, 1), ycbcr_to_rgb_matrix.T))


def path_to_gray(path: Union[str, Path]) -> np.ndarray:
    """
    Load an image from the given path and convert it to Gray format.
    
    Output: Gary image, range from 0 to 1, channel number is 1
    """
    image = np.array(Image.open(path))
    if len(image.shape) == 3:
        return color.rgb2gray(image)
    elif len(image.shape) != 2:
        raise ValueError(f"Wrong shape of image: {image.shape}")
    return image/255.0


def path_to_rgb(path: Union[str, Path]) -> np.ndarray:
    """
    Load an image from the given path and convert it to RGB format.

    Output: RGB image, range from 0 to 1, channel number is 3
    """
    image = np.array(Image.open(path))
    if len(image.shape) == 2:
        return color.gray2rgb(image)/255.0
    elif len(image.shape) != 3:
        raise ValueError(f"Wrong shape of image: {image.shape}")
    return image/255.0


def path_to_ycbcr(path: Union[str, Path]) -> np.ndarray:
    """
    Load an image from the given path and convert it to YCbCr format.

    Output: YCbCr image, range from 0 to 1, channel number is 3
    """
    image = np.array(Image.open(path))
    if len(image.shape) == 2:
        image = color.gray2rgb(image)
    return color.rgb2ycbcr(image)


def glance(
        img: Union[ImageType, list, tuple], 
        annotations: Union[list, tuple] = (),
        clip: bool = False,
        title: Union[str, list] = "",
        hide_axis: bool = True,
        tight_layout: bool = True,
        shape: tuple = (1,1), 
        suptitle: str = "",
        figsize: Optional[tuple] = None,
        auto_contrast: Union[bool, list] = True,
        plot_3d: Union[bool, list] = False,
        save: bool = False,
        save_path: str = "./glance.png",
        each_save: bool = False,
        each_save_dir: str = "./glance_outputs"):
    """
    Display a PyTorch tensor or NumPy array as an image.

    Can input:
    * tensor: 4 dims, batch number should only be 1. channel can be 3 or 1.
    * tensor: 3 dims, channel can be 3 or 1.
    * tensor: 2 dims.
    * ndarray: 2 dims, channel can be 3 or 1.
    * ndarray: 2 dims.
    * Image: auto convert to numpy.
    """
    # convert images to numpy arrays
    if isinstance(img, torch.Tensor):
        if len(img.shape) == 4 and img.shape[0] > 1:
            imgs = [i.unsqueeze(0) for i in img]
            images:list[Optional[np.ndarray]] = [to_numpy(i, clip) for i in imgs]
        else:
            images:list[Optional[np.ndarray]] = [to_numpy(img, clip)]
    if isinstance(img, list) or isinstance(img, tuple):
        if shape[0]*shape[1] != len(img):
            shape = (1,len(img)) 
        images:list[Optional[np.ndarray]] = [(None if i is None else to_numpy(i,clip)) for i in img]
    
    # convert configs to list
    if isinstance(auto_contrast,bool):
        auto_contrast_list: list = [auto_contrast] * (shape[0] * shape[1])
    else:
        auto_contrast_list: list = auto_contrast
    if isinstance(plot_3d,bool):
        plot_3d_list: list = [plot_3d] * (shape[0] * shape[1])
    else:
        plot_3d_list: list = plot_3d

    # plot images
    try:
        plt.figure(figsize=figsize)
        print("uv cannot use `TkAgg` backends! ")
        # https://github.com/astral-sh/uv/issues/6893
    except:
        import matplotlib
        # other backends:
        # https://matplotlib.org/stable/users/explain/figure/backends.html
        matplotlib.use('macosx')
        plt.figure(figsize=figsize)
    
    (H,W) = shape
    for k in range(H*W):
        plt.subplot(H, W, k+1)
        image = images[k]
        if image is None:
            continue
        if each_save:
            save_array_to_img(image, f"{each_save_dir}/{k}.png")
        if image.ndim == 2:
            if plot_3d_list[k]:# 3d
                ax = plt.subplot(H,W,k+1,projection='3d')
                x = np.arange(image.shape[1])
                y = np.flip(np.arange(image.shape[0]))
                x, y = np.meshgrid(x, y)
                surf = ax.plot_surface(x, y, image, cmap='viridis') # type: ignore
                plt.colorbar(surf, shrink=0.5, aspect=5)
            else: # 2d
                if auto_contrast_list[k] == False:
                    plt.imshow((image*255).astype(np.uint8), cmap='gray', vmax=255, vmin=0)
                else:
                    plt.imshow((image*255).astype(np.uint8), cmap='gray')
        else:
            plt.imshow((image*255).astype(np.uint8), cmap='viridis')
        if len(annotations)>0:
            if hasattr(annotations[k-1],'boxes'):
                for anno in annotations[k-1]['boxes']:
                    x_min, y_min, x_max, y_max = [anno[i] for i in range(4)]
                    rect = patches.Rectangle((x_min, y_min), x_max - x_min, y_max - y_min,
                                linewidth=1, edgecolor='r', facecolor='none')
                    plt.gca().add_patch(rect)
        if title != "": plt.title(title[k] if isinstance(title,list) else title)
        if hide_axis: plt.axis('off')
        if tight_layout: plt.tight_layout()
    if suptitle != "": plt.suptitle(suptitle)
    if save:
        plt.savefig(save_path)
    else:
        plt.show()


def save_array_to_img(
        image: ImageType, 
        filename: Union[str, Path], 
        clip: bool = False
    ) -> None:
    to_image(image,clip).save(filename)


def save_array_to_mat(
        image: ImageType, 
        base_filename: str = 'glance', 
        clip: bool = False,
        log: bool = False
    ) -> None:
    """
    Save a NumPy array or PyTorch tensor as MATLAB .mat files.
    """
    # transform torch.tensor to np.array
    image_array = to_numpy(image,clip)

    # Save Image
    if image_array.ndim == 2:
        savemat(f"{base_filename}_gray.mat", {'gray': image_array})
        if log:
            print(f"Gray image have saved as {base_filename}_gray.mat")
    elif image_array.ndim == 3 and image_array.shape[2] == 3:
        savemat(f"{base_filename}_red.mat", {'red': image_array[:, :, 0]})
        savemat(f"{base_filename}_green.mat", {'green': image_array[:, :, 1]})
        savemat(f"{base_filename}_blue.mat", {'blue': image_array[:, :, 2]})
        if log:
            print(f"RGB image have saved as {base_filename}_red.mat, {base_filename}_green.mat and {base_filename}_blue.mat")
    else:
        raise ValueError("Image array should be 2D(Gray) or 3D (RGB).")
