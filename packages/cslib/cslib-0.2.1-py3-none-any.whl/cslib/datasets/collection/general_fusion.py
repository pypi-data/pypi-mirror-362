from typing import List, Dict, Optional, Union
from torch.utils.data import Dataset
from torchvision import transforms
from pathlib import Path
from PIL import Image

class GeneralFusion(Dataset):
    """
    A dataset class for loading and processing infrared (IR), visible (VIS), and fused images.

    This class supports three main use cases:
    1. Basic usage: Load all images from IR and VIS directories, optionally with fused images.
    2. Specify fusion algorithms: Load images for specific fusion algorithms from a parent directory.
    3. Specify image IDs: Load only the images specified by img_id.

    Attributes:
        ir_dir (Path): Directory containing infrared images.
        vis_dir (Path): Directory containing visible images.
        fused_dir (Optional[Path]): Directory containing fused images (or parent directory of fused images).
        transform (Optional[Callable]): Transformation to apply to the images.
        suffix (str): File suffix for images (e.g., 'png', 'jpg').
        algorithms (Optional[Union[str, List[str]]]): Fusion algorithm(s) to use.
        img_id (Optional[Union[str, List[str]]]): Specific image IDs to load.
        all_img_id (Union[List[str], Dict[str, List[str]]]): List or dictionary of image IDs.
        fused_dirs (Optional[Dict[str, Path]]): Dictionary of fusion algorithm directories.
        bias_helper_dict (Dict[int, List]): Helper dictionary for mapping indices to algorithms.

    Methods:
        __len__(): Returns the total number of images in the dataset.
        __getitem__(idx): Returns a dictionary containing the IR, VIS, and fused images for the given index.
        _recover_from_idx(idx): Helper method to recover the algorithm and index from a global index.

    Example:
        >>> dataset = GeneralFusion(ir_dir='/path/to/ir', vis_dir='/path/to/vis', fused_dir='/path/to/fused', algorithms=['cpfusion', 'datfuse'])
        >>> dataloader = DataLoader(dataset, batch_size=1, shuffle=False)
        >>> for batch in dataloader:
        >>>     print(batch['ir'], batch['vis'], batch['fused'], batch['algorithm'])

    Note:
        - If fused_dir is provided, it must contain subdirectories named after the fusion algorithms.
        - If img_id is provided, it must be a list of image IDs (without file suffix).
        - The dataset assumes that all images have the same suffix.
    """
    def __init__(
            self, 
            ir_dir: Union[str, Path], 
            vis_dir: Union[str, Path], 
            fused_dir: Optional[Union[str, Path]], 
            transform: Optional[transforms.Compose] = None,
            suffix: str = 'png', 
            algorithms: Optional[Union[str, List[str]]] = None,
            img_id: Optional[Union[str, List[str]]] = None, 
        ):
        """
        Initialize the GeneralFusion dataset.

        Args:
            ir_dir (Union[str, Path]): Directory containing infrared images.
            vis_dir (Union[str, Path]): Directory containing visible images.
            fused_dir (Optional[Union[str, Path]]): Directory containing fused images (or parent directory of fused images).
            transform (Optional[Callable]): Transformation to apply to the images.
            suffix (str): File suffix for images (e.g., 'png', 'jpg').
            algorithms (Optional[Union[str, List[str]]]): Fusion algorithm(s) to use.
            img_id (Optional[Union[str, List[str]]]): Specific image IDs to load.
        """
        # Base Paths
        self.ir_dir: Path = Path(ir_dir)
        self.vis_dir: Path = Path(vis_dir)
        self.fused_dir: Optional[Path] = Path(fused_dir) if fused_dir != None else None
        
        # Enable Multiple Fused Algorithms
        if isinstance(self.fused_dir, Path):
            if algorithms is None:
                self.fused_dirs = {
                    self.fused_dir.name: self.fused_dir
                }
            else:
                if isinstance(algorithms, str):
                    algorithms = [algorithms]
                self.fused_dirs = {
                    a: self.fused_dir / a for a in algorithms
                }
        
        # Check Path
        assert self.ir_dir.exists()
        assert self.vis_dir.exists()
        if isinstance(self.fused_dir, Path):
            for _,p in self.fused_dirs.items():
                assert p.exists()

        # Default Transform
        if transform is None:
            transform = transforms.Compose([transforms.ToTensor()])
        self.transform = transform

        # Checking and Enable Specified Image IDs
        if img_id is None or len(img_id) == 0:
            # 1. All Images
            all_ir_imgs = sorted(list(self.ir_dir.glob(f"*.{suffix}")))
            all_vis_imgs = sorted(list(self.vis_dir.glob(f"*.{suffix}")))
            all_img_id = [i.name for i in all_vis_imgs]
            if self.fused_dir is None: # doesn't need fused, assert num equals
                # 1.1 All Images without fused
                assert len(all_ir_imgs) == len(all_vis_imgs), "Number of IR and VIS must be equal"
                self.all_img_id: Union[List, Dict] = all_img_id
            else: 
                # 1.2 All Images with fused - maybe shrink range
                self.all_img_id: Union[List, Dict] = {}
                for algorithms,p in self.fused_dirs.items():
                    all_fused_imgs = sorted(list(p.glob(f"*.{suffix}")))
                    if len(all_fused_imgs) != len(all_vis_imgs):
                        # For We believe that if the lengths are equal, 
                        # the file names are the same, for saving time.
                        for i in all_fused_imgs:
                            vis_path = self.vis_dir / i.name
                            ir_path = self.ir_dir / i.name
                            if not vis_path.exists():
                                raise FileNotFoundError(f"Visible image not found: {vis_path}")
                            if not ir_path.exists():
                                raise FileNotFoundError(f"Infrared image not found: {ir_path}")
                    self.all_img_id[algorithms] = [i.name for i in all_fused_imgs]
        else:
            # 2. Enable Specified Image IDs
            all_img_id = [f'{i}.{suffix}' for i in img_id]
            for img_name in all_img_id:
                vis_path = self.vis_dir / img_name
                ir_path = self.ir_dir / img_name
                if not vis_path.exists():
                    raise FileNotFoundError(f"Visible image not found: {vis_path}")
                if not ir_path.exists():
                    raise FileNotFoundError(f"Infrared image not found: {ir_path}")
            if self.fused_dir is None: # doesn't need fused, assert num equals
                # 2.1 Specified Images without fused
                self.all_img_id: Union[List, Dict] = all_img_id
            else: 
                # 2.2 Specified Images with fused
                self.all_img_id: Union[List, Dict] = {}
                for algorithms,p in self.fused_dirs.items():
                    all_fused_imgs = sorted(list(p.glob(f"*.{suffix}")))
                    for i in all_img_id:
                        if not (p / i).exists():
                            raise FileNotFoundError(f"Fused image not found: {p / i}")
                    self.all_img_id[algorithms] = all_img_id
        
        # Build Bias Helper Dict
        self.bias_helper_dict = {}
        if isinstance(self.all_img_id, dict):
            bias = 0
            for algorithms,ids in self.all_img_id.items():
                self.bias_helper_dict[bias] = [algorithms,len(ids)]
                bias = bias + len(ids)
        
    def _recover_from_idx(self, idx: int) -> tuple:
        """
        Recover the algorithm and index from a global index.

        Args:
            idx (int): Global index.

        Returns:
            tuple: (local_index, algorithm)
        """
        assert isinstance(self.all_img_id, dict)
        for bias, (algorithms, length) in self.bias_helper_dict.items():
            if bias <= idx < bias + length:
                return idx - bias, algorithms
        raise ValueError("idx is out of range")
    
    def __len__(self) -> int:
        if isinstance(self.all_img_id, dict):
            count = 0
            for _, value in self.all_img_id.items():
                count += len(value)
            return count
        else:
            return len(self.all_img_id)

    def __getitem__(self, idx) -> dict:
        if isinstance(self.all_img_id, dict):
            idx, algorithms = self._recover_from_idx(idx)
            ir_image = Image.open(((self.ir_dir / self.all_img_id[algorithms][idx])).__str__())
            vis_image = Image.open(((self.vis_dir / self.all_img_id[algorithms][idx])).__str__())
            fused_image = Image.open(((self.fused_dirs[algorithms] / self.all_img_id[algorithms][idx])).__str__())

            ir_image = self.transform(ir_image)
            vis_image = self.transform(vis_image)
            fused_image = self.transform(fused_image)

            return {
                'id': self.all_img_id[algorithms][idx].split('.')[0],
                'ir': ir_image,
                'vis': vis_image,
                'fused': fused_image,
                'algorithm': algorithms,
            }

        if isinstance(self.all_img_id, list):
            ir_image = Image.open(((self.ir_dir / self.all_img_id[idx])).__str__())
            vis_image = Image.open(((self.vis_dir / self.all_img_id[idx])).__str__())

            ir_image = self.transform(ir_image)
            vis_image = self.transform(vis_image)

            return {
                'id': self.all_img_id[idx].split('.')[0],
                'ir': ir_image,
                'vis': vis_image,
            }
        
        raise ValueError("all_img_id should be list or dict")