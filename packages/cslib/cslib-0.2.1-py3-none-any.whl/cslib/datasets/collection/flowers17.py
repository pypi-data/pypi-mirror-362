from pathlib import Path
from typing import Any, Callable, Optional, Tuple

import PIL.Image

from torchvision.datasets.utils import check_integrity, download_and_extract_archive, download_url, verify_str_arg
from torchvision.datasets.vision import VisionDataset

__all__ = ['Flowers17']

class Flowers17(VisionDataset):
    """`Oxford 17 Flower <https://www.robots.ox.ac.uk/~vgg/data/flowers/17/>`_ Dataset.

    Modified from pytorch Flowers102 by Charles Shan.

    .. warning::

        This class needs `scipy <https://docs.scipy.org/doc/>`_ to load target files from `.mat` format.

    Oxford 17 Flower is an image classification dataset consisting of 17 flower categories. The
    flowers were chosen to be flowers commonly occurring in the United Kingdom. Each class consists of
    between 80 images.

    The images have large scale, pose and light variations. In addition, there are categories that
    have large variations within the category, and several very similar categories.

    Args:
        root (string): Root directory of the dataset.
        split (string, optional): The dataset split, supports ``"train"`` (default), ``"val"``, or ``"test"``.
        transform (callable, optional): A function/transform that takes in an PIL image and returns a
            transformed version. E.g, ``transforms.RandomCrop``.
        target_transform (callable, optional): A function/transform that takes in the target and transforms it.
        download (bool, optional): If true, downloads the dataset from the internet and
            puts it in root directory. If dataset is already downloaded, it is not
            downloaded again.
    """
    
    _download_url_prefix = "https://www.robots.ox.ac.uk/~vgg/data/flowers/17/"
    _file_dict = {  # filename, md5
        "image": ("17flowers.tgz", "b59a65d8d1a99cd66944d474e1289eab"),
        "setid": ("datasplits.mat", "4828cddfd0d803c5abbdebcb1e148a1e"),
        # "setid": ("setid.mat", "a5357ecc9cb78c4bef273ce3793fc85c"),
    }
    _splits_map = {
        "train": ["trn1","trn2","trn3"], 
        "val": ["val1","val2","val3"], 
        "test": ["tst1","tst2","tst3"]
    }

    def __init__(
        self,
        root: str,
        split: str = "train",
        transform: Optional[Callable] = None,
        target_transform: Optional[Callable] = None,
        download: bool = False,
    ) -> None:
        super().__init__(root, transform=transform, target_transform=target_transform)
        self._split = verify_str_arg(split, "split", ("train", "val", "test"))
        self._base_folder = Path(self.root) / "flowers-17"
        self._images_folder = self._base_folder / "jpg"

        if download:
            self.download()

        if not self._check_integrity():
            raise RuntimeError("Dataset not found or corrupted. You can use download=True to download it")

        from scipy.io import loadmat

        self.names = {
            0: 'Daffodil',    # 1
            1: 'Snowdrop',    # 81
            2: 'LilyValley',  # 161
            3: 'Bluebell',    # 241
            4: 'Crocus',      # 321
            5: 'Iris',        # 401
            6: 'TigerLily',   # 481
            7: 'Tulip',       # 561
            8: 'Fritillary',  # 641
            9: 'Sunflower',   # 721
            10:'Daisy',       # 801
            11:'Coltsfoot',   # 881
            12:'Dandelion',   # 961
            13:'Cowslip',     # 1041
            14:'Buttercup',   # 1121
            15:'Windflower',  # 1201
            16:'Pansy',       # 1281
        }

        set_ids = loadmat(self._base_folder / self._file_dict["setid"][0], squeeze_me=True)
        image_ids = sum([set_ids[self._splits_map[self._split][i]].tolist() for i in range(3)], [])

        image_id_to_label = {i+1: i//80 for i in range(80*17)}

        self._labels = []
        self._image_files = []
        for image_id in image_ids:
            self._labels.append(image_id_to_label[image_id])
            self._image_files.append(self._images_folder / f"image_{image_id:04d}.jpg")

    def __len__(self) -> int:
        return len(self._image_files)

    def __getitem__(self, idx: int) -> Tuple[Any, Any]:
        image_file, label = self._image_files[idx], self._labels[idx]
        image = PIL.Image.open(image_file).convert("RGB")

        if self.transform:
            image = self.transform(image)

        if self.target_transform:
            label = self.target_transform(label)

        return image, label

    def extra_repr(self) -> str:
        return f"split={self._split}"

    def _check_integrity(self):
        if not (self._images_folder.exists() and self._images_folder.is_dir()):
            return False

        for id in ["setid"]:#["label", "setid"]:
            filename, md5 = self._file_dict[id]
            if not check_integrity(str(self._base_folder / filename), md5):
                return False
        return True

    def download(self):
        if self._check_integrity():
            return
        download_and_extract_archive(
            f"{self._download_url_prefix}{self._file_dict['image'][0]}",
            str(self._base_folder),
            md5=self._file_dict["image"][1],
        )
        for id in ['setid']:#["label", "setid"]:
            filename, md5 = self._file_dict[id]
            download_url(self._download_url_prefix + filename, str(self._base_folder), md5=md5)
