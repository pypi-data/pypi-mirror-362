# https://image-net.org/data/ILSVRC/2012/ILSVRC2012_img_val.tar

import os
from pathlib import Path
from typing import Any, Union

from torchvision.datasets.imagenet import parse_devkit_archive, parse_val_archive, META_FILE, load_meta_file
from torchvision.datasets.folder import ImageFolder
from torchvision.datasets.utils import check_integrity, download_url

__all__ = ['ImageNetVal']

FOLDER_NAME = "imagenet-1k"
VAL_URL = "https://image-net.org/data/ILSVRC/2012/ILSVRC2012_img_val.tar"
KIT_URL = "https://image-net.org/data/ILSVRC/2012/ILSVRC2012_devkit_t12.tar.gz"
VAL_MD5 = "29b22e2961454d5413ddabcf34fc5622"
KIT_MD5 = "fa75699e90414af021442c21a62c3abf"

class ImageNetVal(ImageFolder):
    """`ImageNet <http://image-net.org/>`_ 2012 Classification Dataset.

    .. note::
        Before using this class, it is required to download ImageNet 2012 dataset from
        `here <https://image-net.org/challenges/LSVRC/2012/2012-downloads.php>`_ and
        place the files ``ILSVRC2012_devkit_t12.tar.gz`` and ``ILSVRC2012_img_train.tar``
        or ``ILSVRC2012_img_val.tar`` based on ``split`` in the root directory.

    Args:
        root (str or ``pathlib.Path``): Root directory of the ImageNet Dataset.
        split (string, optional): The dataset split, supports ``train``, or ``val``.
        transform (callable, optional): A function/transform that takes in a PIL image
            and returns a transformed version. E.g, ``transforms.RandomCrop``
        target_transform (callable, optional): A function/transform that takes in the
            target and transforms it.
        loader (callable, optional): A function to load an image given its path.

     Attributes:
        classes (list): List of the class name tuples.
        class_to_idx (dict): Dict with items (class_name, class_index).
        wnids (list): List of the WordNet IDs.
        wnid_to_idx (dict): Dict with items (wordnet_id, class_index).
        imgs (list): List of (image path, class_index) tuples
        targets (list): The class_index value for each image in the dataset
    """

    def __init__(
            self, 
            root: Union[str, Path], 
            download: bool = False,
            **kwargs: Any
        ) -> None:
        root = self.root = Path(os.path.expanduser(root)) / FOLDER_NAME
        self.split = "val"

        if root.exists() == False:
            root.mkdir()

        if download:
            self.download()

        self.parse_archives()
        wnid_to_classes = load_meta_file(self.root)[0]

        super().__init__(self.split_folder, **kwargs)
        self.root = root / FOLDER_NAME

        self.wnids = self.classes
        self.wnid_to_idx = self.class_to_idx
        self.classes = [wnid_to_classes[wnid] for wnid in self.wnids]
        self.class_to_idx = {cls: idx for idx, clss in enumerate(self.classes) for cls in clss}

    def parse_archives(self) -> None:
        if not check_integrity(os.path.join(self.root, META_FILE)):
            parse_devkit_archive(self.root)

        if not os.path.isdir(self.split_folder):
            parse_val_archive(self.root)
    
    def download(self):
        def _check_integrity():
            if not (self.root.exists() and self.root.is_dir()):
                return False
            # if not check_integrity(self.root.parent / 'ILSVRC2012_img_val.tar', VAL_MD5):
            #     raise ValueError("ImageNet-1k val: ILSVRC2012_img_val.tar is wrong, please delete it.")
            # if not check_integrity(self.root.parent / 'ILSVRC2012_devkit_t12.tar.gz', KIT_MD5):
            #     raise ValueError("ImageNet-1k val: ILSVRC2012_devkit_t12.tar.gz is wrong, please delete it.")
            return True

        if _check_integrity():
            return
        # download_url(VAL_URL,self.root, md5="29b22e2961454d5413ddabcf34fc5622")
        download_url(KIT_URL,self.root, md5="fa75699e90414af021442c21a62c3abf")

    @property
    def split_folder(self) -> str:
        return os.path.join(self.root, self.split)

    def extra_repr(self) -> str:
        return "Split: {split}".format(**self.__dict__)
