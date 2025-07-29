from typing import List, Optional, Union, Callable
import torch
from torch.utils.data import Dataset
from torchvision import transforms
import os
from PIL import Image
from pathlib import Path

__all__ = ['GeneralSR']

class GeneralSR(Dataset):
    def __init__(self, root_dir: Union[str, Path], upscale_factor: str,\
                 transform: Optional[Callable[[Image.Image], torch.Tensor]] = None, \
                 suffix: str = 'png', img_id: Optional[List[str]] = None, \
                 check: bool = True, only_path: bool = True):
        # Base Paths and Config
        self.root_dir = root_dir
        self.upscale_factor = upscale_factor
        self.upsacle_root_dir = Path(root_dir,f'X{upscale_factor}')
        self.gt_dir = Path(self.upsacle_root_dir, "GT")
        self.upsacle_dir = Path(self.upsacle_root_dir, "LR")
        self.only_path = only_path

        # Set default transform if none provided
        if transform is None:
            transform = transforms.Compose([
                transforms.ToTensor(),
            ])
        self.transform = transform

        # Get HR and LR Path
        self.lr_paths = sorted([Path(self.upsacle_dir,i) for i in os.listdir(self.upsacle_dir) if i.endswith(f'.{suffix}')])
        self.gt_paths = sorted([Path(self.gt_dir,i) for i in os.listdir(self.gt_dir) if i.endswith(f'.{suffix}')])
        if img_id is not None:
            self.gt_paths = [i for i in self.gt_paths if os.path.splitext(i.name)[0] in img_id]
            self.lr_paths = [i for i in self.lr_paths if os.path.splitext(i.name)[0] in img_id]
            
        # Check
        assert len(self.gt_paths) == len(self.lr_paths)
        if check:
            for i,j in zip(self.gt_paths, self.lr_paths):
                assert os.path.splitext(i.name)[0] == os.path.splitext(j.name)[0]
        
    def __len__(self):
        return len(self.gt_paths)

    def __getitem__(self, idx):
        # Load images
        gt_image = self.gt_paths[idx].__str__()
        lr_image = self.lr_paths[idx].__str__()
        img_id = os.path.splitext(self.gt_paths[idx].name)[0]

        # Apply transform if specified
        if self.only_path == False:
            gt_image = self.transform(Image.open(gt_image))
            lr_image = self.transform(Image.open(lr_image))

        # Return a dictionary with all images
        sample = {
            'gt': gt_image,
            'lr': lr_image,
            'id': img_id
        }
        return sample