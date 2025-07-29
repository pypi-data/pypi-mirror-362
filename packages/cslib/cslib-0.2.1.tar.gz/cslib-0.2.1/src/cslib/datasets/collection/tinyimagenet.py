from typing import Any, Union, Tuple, Dict, List
from pathlib import Path
import shutil
import torch
from torchvision.datasets.folder import ImageFolder
from torchvision.datasets.imagenet import load_meta_file
from torchvision.datasets.utils import check_integrity, verify_str_arg, download_and_extract_archive

__all__ = ['TinyImageNet']

META_FILE = "meta.bin"
ARCHIVE_URL = "http://cs231n.stanford.edu/tiny-imagenet-200.zip"
ARCHIVE_MD5 = "90528d7ca1a48142e341f4ef8d21d0de"
FOLDER_NAME = "tiny-imagenet-200"

class TinyImageNet(ImageFolder):
    """
    TinyImageNet Dataset.

    This class inherits from ImageNet and modifies the required attributes and methods
    to support the TinyImageNet dataset.

    This class would auto-download into torchvision folder.
    """
    def __init__(
            self, 
            root: Union[str, Path], 
            split: str = "train", 
            download: bool = False,
            **kwargs: Any
        ) -> None:
        root = self.root = Path(root).expanduser()
        self.split = verify_str_arg(split, "split", ("train", "val", "test"))

        if download:
            self.download()

        if not check_integrity(self.root / FOLDER_NAME / META_FILE):
            generate_tiny_imagenet_meta(self.root)

        wnid_to_classes = load_meta_file(self.root / FOLDER_NAME)[0]

        super().__init__(self.split_folder, **kwargs)
        self.root = Path(root) / FOLDER_NAME

        self.wnids = self.classes
        self.wnid_to_idx = self.class_to_idx
        self.classes = [wnid_to_classes[wnid] for wnid in self.wnids]
        self.class_to_idx = {cls: idx for idx, clss in enumerate(self.classes) for cls in clss}
    
    def download(self):
        def _check_integrity():
            if not ((self.root / FOLDER_NAME).exists() and (self.root / FOLDER_NAME).is_dir()):
                return False
            if not check_integrity(self.root / "tiny-imagenet-200.zip", ARCHIVE_MD5):
                return False
            return True

        if _check_integrity():
            return
        download_and_extract_archive(ARCHIVE_URL,self.root, md5=ARCHIVE_MD5)

    @property
    def split_folder(self) -> Path:
        return self.root / FOLDER_NAME / self.split

    def extra_repr(self) -> str:
        return "Split: {split}".format(**self.__dict__)

def generate_tiny_imagenet_meta(root: Union[str, Path]) -> None:
    wnids_file = Path(root) / FOLDER_NAME / "wnids.txt"
    with open(wnids_file, "r") as f:
        wnids = [line.strip() for line in f.readlines()]

    words_file = Path(root) / FOLDER_NAME / "words.txt"
    wnid_to_classes: Dict[str, Tuple[str, ...]] = {}
    with open(words_file, "r") as f:
        for line in f.readlines():
            parts = line.strip().split("\t")
            wnid = parts[0]
            classes = tuple(parts[1].split(", "))
            if wnid in wnids:
                wnid_to_classes[wnid] = classes
                
    val_annotations_file = Path(root) / FOLDER_NAME / "val" / "val_annotations.txt"
    val_wnids: List[str] = []
    with open(val_annotations_file, "r") as f:
        for line in f.readlines():
            parts = line.strip().split("\t")
            val_wnids.append(parts[1])

    torch.save((wnid_to_classes, val_wnids), Path(root) / FOLDER_NAME / META_FILE)
    print(f"Meta file saved at {Path(root) / FOLDER_NAME / META_FILE}")

    image_path = Path(root) / FOLDER_NAME / 'val' / 'images'
    with open(val_annotations_file, "r") as f:
        for line in f.readlines():
            parts = line.strip().split("\t")
            folder_path = Path(root) / FOLDER_NAME / 'val' / parts[1]
            (folder_path / 'images').mkdir(parents=True, exist_ok=True)
            shutil.move(image_path / parts[0], folder_path / 'images' / parts[0])
            with open(folder_path / f'{parts[1]}.txt' , "a+") as f2:
                f2.write(line)
    image_path.rmdir()