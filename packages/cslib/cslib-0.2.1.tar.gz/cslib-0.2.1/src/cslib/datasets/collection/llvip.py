from typing import Callable, Optional, Union
from torchvision.datasets.vision import VisionDataset
from torchvision.datasets.utils import download_and_extract_archive, extract_archive
from pathlib import Path
from PIL import Image
import os
import shutil

__all__ = ['LLVIP']

def split_file(file_path, num_chunks):
    """
    split LLVIP.zip into 400 parts.
    """
    if not os.path.isfile(f'{file_path}.zip'):
        print(f"Error: {file_path} does not exist.")
        return

    file_size = os.path.getsize(f'{file_path}.zip')
    chunk_size = file_size // num_chunks
    remainder = file_size % num_chunks

    if not os.path.exists('parts'):
        os.makedirs('parts')
    with open(f'{file_path}.zip', 'rb') as f:
        for i in range(num_chunks):
            chunk_file_path = f"parts/{os.path.basename(file_path)}_part_{str(i).zfill(2)}"
            with open(chunk_file_path, 'wb') as chunk_file:
                # 如果是最后一个块，需要加上余数部分
                bytes_to_read = chunk_size + (remainder if i == num_chunks - 1 else 0)
                chunk_data = f.read(bytes_to_read)
                chunk_file.write(chunk_data)
                print(f"Created chunk: {chunk_file_path}")
# split_file('llvip', 400)

def merge_files(basefolder, num_chunks, output_file):
    """
    merge 400 parts into LLVIP.zip.
    """
    with open(Path(basefolder) / output_file, 'wb') as output:
        for i in range(num_chunks):
            chunk_file = Path(basefolder) / 'parts' / f"LLVIP_part_{str(i).zfill(2)}"
            if not os.path.isfile(chunk_file):
                print(f"Error: {chunk_file} does not exist.")
                return
            with open(chunk_file, 'rb') as chunk:
                shutil.copyfileobj(chunk, output)
            print(f"Merged {chunk_file}")
# merge_files('LLVIP', 400, 'merged_largefile.zip')

def move_folder_contents(src_folder: Path, dest_folder: Path):
    dest_folder.mkdir(parents=True, exist_ok=True)
    for item in src_folder.iterdir():
        if item.name.split('_')[0] == 'LLVIP':
            try:
                item.replace(dest_folder / item.name)
            except Exception as e:
                print(f"Fail to move {item} to {dest_folder}: {e}")

class LLVIP(VisionDataset):
    """
    LLVIP dataset for visible-infrared paired image research.

    The LLVIP dataset is a collection of paired visible and infrared images for various research purposes,
    including image registration and fusion.

    Dataset can be downloaded from the following links:
    - Google Drive: https://drive.google.com/file/d/1VTlT3Y7e1h-Zsne4zahjx5q0TK2ClMVv/view?usp=sharing
    - Baidu Yun: https://pan.baidu.com/s/1eQO1Is2NPyd-mgmv1Csbfg Password: 14lc

    Raw data (unregistered image pairs and videos) for further research can be downloaded from:
    - Google Drive: https://drive.google.com/file/d/1a0zNvj1mBh1v_HFWJ43LFbNEq8YLXB9-/view?usp=sharing
    - Baidu Yun: https://pan.baidu.com/s/1VXMiWH1EJGVGoCEV7AMF6Q Password: cpfh

    If you encounter any issues with the dataset or algorithms, please contact:
    - shengjie.Liu@bupt.edu.cn
    - czhu@bupt.edu.cn
    - jiaxinyujxy@qq.com
    - tangwenqi@bupt.edu.cn

    The dataset is freely available for academic and non-academic entities for non-commercial purposes such as academic research, teaching, scientific publications, or personal experimentation. Usage of the dataset implies agreement with our license terms available at: https://github.com/bupt-ai-cz/LLVIP

    For more information, please visit GitHub page: https://github.com/bupt-ai-cz or the CVSM Group website: https://teacher.bupt.edu.cn/zhuchuang/en/index.htm

    To submit your experimental results at: https://paperswithcode.com/paper/llvip-a-visible-infrared-paired-dataset-for

    Args:
        root (str): Root directory of the dataset where the dataset should be stored.
        transform (callable, optional): A function/transform that takes in a PIL image
            and returns a transformed version. E.g, ``transforms.ToTensor``
        download (bool, optional): If true, downloads the dataset from the internet and
            puts it in the root directory. If dataset is already downloaded, it is not
            downloaded again.
    """
    url = [
        'https://github.com/CharlesShan-hub/LLVIP-Backup-Part1/archive/refs/heads/master.zip',
        'https://github.com/CharlesShan-hub/LLVIP-Backup-Part2/archive/refs/heads/master.zip',
        'https://github.com/CharlesShan-hub/LLVIP-Backup-Part3/archive/refs/heads/master.zip',
        'https://github.com/CharlesShan-hub/LLVIP-Backup-Part4/archive/refs/heads/master.zip',
        'https://github.com/CharlesShan-hub/LLVIP-Backup-Part5/archive/refs/heads/master.zip',
    ]
    md5 = [
        'fcd13ebf3378dec0cb954568a4f9d167',
        'a47a30755545ff41b4d7744bf7c4ca41',
        '5cc06bd87a7e35c93166ca57b509509e',
        '72796e85a6d786015a240702f6c935ec',
        '28c9a5e39d2366539d4aaf726893d9ca'
    ]

    def __init__(
            self, 
            root: Union[str, Path], 
            transform: Optional[Callable] = None, 
            download: bool = True,
            train: bool = False,
        ) -> None:
        super().__init__(root, transform=transform)
        self._base_folder = Path(self.root) / "llvip-temp"
        self._src_folder = Path(self.root) / "llvip"
        if download:
            self.download()
        if train:
            ir_folder = self._src_folder / 'infrared' / 'train'
            vis_folder = self._src_folder / 'visible' / 'train'
        else:
            ir_folder = self._src_folder / 'infrared' / 'test'
            vis_folder = self._src_folder / 'visible' / 'test'
        self.ir_path = sorted([f for f in ir_folder.iterdir() if f.suffix == '.jpg'], key=lambda x: int(x.stem))
        self.vis_path = sorted([f for f in vis_folder.iterdir() if f.suffix == '.jpg'], key=lambda x: int(x.stem))
        assert len(self.ir_path) == len(self.vis_path)

    def __getitem__(self, idx: int):
        ir = self._src_folder / 'fusion' / 'ir' / f'{self.ir_path[idx]}'
        vis = self._src_folder / 'fusion' / 'vis' / f'{self.vis_path[idx]}'
        if self.transform:
            ir = self.transform(Image.open(ir).convert("L"))
            vis = self.transform(Image.open(vis).convert("RGB"))
            return ir, vis
        return str(ir),str(vis)

    def __len__(self):
        return len(self.ir_path)

    def download(self):
        if self._src_folder.exists():
            # print(self._src_folder,'exists')
            return
        self._base_folder.mkdir()
        (self._base_folder / 'parts').mkdir()
        print("You can also download manully from `https://drive.google.com/file/d/1VTlT3Y7e1h-Zsne4zahjx5q0TK2ClMVv/view?usp=sharing`")
        for i in range(5):
            download_and_extract_archive(
                    url=self.url[i],
                    download_root=self._base_folder,
                    extract_root=self._base_folder,
                    filename=f"LLVIP-Backup-Part{i+1}-master.zip",
                    md5=self.md5[i],
                    remove_finished=True
                )
            move_folder_contents(
                src_folder=self._base_folder / f'LLVIP-Backup-Part{i+1}-master',
                dest_folder=self._base_folder / 'parts'
            )
        merge_files(self._base_folder, 400, 'merged.zip')
        print('Starting extract zip, this will take a few minutes...')
        extract_archive(
            from_path=self._base_folder / 'merged.zip',
            to_path=self._base_folder.parent,
            remove_finished=True
        )
        shutil.rmtree(self._base_folder)
        print('Download completed.')
