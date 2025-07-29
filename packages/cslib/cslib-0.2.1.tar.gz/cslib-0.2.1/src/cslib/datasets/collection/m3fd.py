from typing import Callable, Optional, Union
from pathlib import Path
from torchvision.datasets.vision import VisionDataset
from torchvision.datasets.utils import download_and_extract_archive
from PIL import Image
import shutil

__all__ = ['M3FD']

def move_folder_contents(src_folder: Path, dest_folder: Path):
    dest_folder.mkdir(parents=True, exist_ok=True)
    for item in src_folder.iterdir():
        try:
            item.replace(dest_folder / item.name)
        except Exception as e:
            print(f"Fail to move {item} to {dest_folder}: {e}")

class M3FD(VisionDataset):
    """ M3FD
    Paper: Target-aware Dual Adversarial Learning and a Multi-scenario Multi-Modality 
        Benchmark to Fuse Infrared and Visible for Object Detection
    Github: https://github.com/dlut-dimt/TarDAL

    This class can download from backup repository but its too slow.
    It's recommanded to download from Google Drive or Baidu Yun link above 
    and put them into correct folder.

    Google Drive: https://drive.google.com/drive/folders/1H-oO7bgRuVFYDcMGvxstT1nmy0WF_Y_6
    Baidu Yun: https://pan.baidu.com/s/1GoJrrl_mn2HNQVDSUdPCrw?pwd=M3FD

    For example, the input `root` is `/Users/kimshan/public/data/vision/torchvision`
    then make a folder named m3fd and unzip 
    .
    └── m3fd
        └── fusion
            ├── ir
            │  ├── 00000.png
            │  ├── 00011.png
            │  └── ...
            └── vis
               ├── 00000.png
               ├── 00011.png
               └── ...
    """
    file = [
        '00000', '00011', '00025', '00031', '00033', '00042', '00061', '00071', '00082', '00097', '00107', '00112', 
        '00118', '00147', '00149', '00150', '00159', '00177', '00196', '00202', '00210', '00215', '00232', '00242', 
        '00255', '00274', '00284', '00290', '00306', '00320', '00325', '00334', '00339', '00349', '00353', '00370', 
        '00385', '00386', '00388', '00389', '00390', '00400', '00405', '00409', '00419', '00421', '00434', '00441', 
        '00443', '00449', '00453', '00461', '00479', '00489', '00497', '00512', '00525', '00527', '00537', '00555', 
        '00572', '00587', '00606', '00621', '00633', '00643', '00652', '00653', '00661', '00671', '00676', '00677', 
        '00687', '00697', '00712', '00716', '00719', '00725', '00726', '00738', '00760', '00762', '00769', '00787', 
        '00800', '00801', '00805', '00818', '00825', '00826', '00829', '00834', '00857', '00867', '00871', '00878', 
        '00896', '00910', '00916', '00922', '00926', '00950', '00958', '00965', '00976', '00994', '01017', '01034', 
        '01043', '01079', '01093', '01101', '01115', '01122', '01136', '01147', '01156', '01165', '01186', '01204', 
        '01212', '01223', '01227', '01242', '01249', '01267', '01270', '01299', '01301', '01320', '01331', '01345', 
        '01388', '01393', '01406', '01413', '01415', '01422', '01432', '01437', '01442', '01443', '01454', '01462', 
        '01471', '01482', '01486', '01492', '01494', '01505', '01511', '01527', '01531', '01547', '01562', '01579', 
        '01584', '01587', '01599', '01608', '01640', '01659', '01670', '01673', '01707', '01710', '01724', '01729', 
        '01741', '01760', '01773', '01779', '01783', '01789', '01803', '01806', '01807', '01811', '01828', '01845', 
        '01856', '01861', '01867', '01899', '01911', '01912', '01913', '01919', '01929', '01937', '01947', '01954', 
        '01963', '01977', '01981', '01985', '01994', '01996', '02002', '02011', '02033', '02045', '02073', '02083', 
        '02090', '02102', '02119', '02120', '02142', '02163', '02180', '02195', '02213', '02233', '02236', '02249', 
        '02278', '02296', '02310', '02317', '02322', '02337', '02352', '02369', '02394', '02405', '02440', '02450', 
        '02455', '02464', '02473', '02478', '02486', '02495', '02522', '02527', '02530', '02533', '02544', '02556', 
        '02572', '02606', '02611', '02624', '02641', '02651', '02658', '02667', '02709', '02720', '02731', '02739', 
        '02754', '02757', '02762', '02778', '02786', '02816', '02821', '02846', '02860', '02869', '02896', '02956', 
        '03019', '03045', '03100', '03109', '03143', '03173', '03219', '03260', '03281', '03289', '03354', '03375', 
        '03381', '03409', '03417', '03433', '03438', '03462', '03473', '03575', '03589', '03600', '03640', '03708', 
        '03719', '03769', '03813', '03836', '03878', '03989', '04006', '04018', '04026', '04053', '04092', '04160']
    url = "https://github.com/CharlesShan-hub/M3FD-Fusion-Backup/archive/refs/heads/master.zip"
    md5 = "e11dcc73ff6f590d927631467930abb6"

    def __init__(
        self,
        root: Union[str, Path],
        transform: Optional[Callable] = None,
        download: bool = True
    ) -> None:
        super().__init__(str(root), transform=transform)
        self._base_folder = Path(self.root) / "m3fd"

        if download:
            self.download()
    
    def __getitem__(self, idx: int):
        ir_file = self._base_folder / 'fusion' / 'ir' / f'{self.file[idx]}.png'
        ir = Image.open(ir_file).convert("L")
        vis_file = self._base_folder / 'fusion' / 'vis' / f'{self.file[idx]}.png'
        vis = Image.open(vis_file).convert("RGB")
        if self.transform:
            ir = self.transform(ir)
            vis = self.transform(vis)
        return ir,vis
        
    def __len__(self):
        return len(self.file)
    
    def download(self):
        if not self._base_folder.exists():
            print(f"mkdir of: {self._base_folder}")
            self._base_folder.mkdir()
            (self._base_folder / 'fusion').mkdir()
            (self._base_folder / 'fusion' / 'ir').mkdir()
            (self._base_folder / 'fusion' / 'vis').mkdir()
        valid = True
        for name in self.file:
            if not (self._base_folder / 'fusion' / 'ir' / f'{name}.png').exists():
                valid = False
                print(self._base_folder / 'fusion' / 'ir' / f'{name}.png')
                break
            if not (self._base_folder / 'fusion' / 'vis' / f'{name}.png').exists():
                valid = False
                print(self._base_folder / 'fusion' / 'vis' / f'{name}.png')
                break
        if valid:
            return
        print("You can also download manully from `https://drive.google.com/drive/folders/1H-oO7bgRuVFYDcMGvxstT1nmy0WF_Y_6`")
        download_and_extract_archive(
                    url=self.url,
                    download_root=self._base_folder,
                    extract_root=self._base_folder,
                    filename="m3fd_temp.zip",
                    md5=self.md5,
                    remove_finished=True
                )
        move_folder_contents(
            src_folder=self._base_folder / 'M3FD-Fusion-Backup-master' / 'M3FD_Fusion' / 'Ir',
            dest_folder=self._base_folder / 'fusion' / 'ir'
        ) 
        move_folder_contents(
            src_folder=self._base_folder / 'M3FD-Fusion-Backup-master' / 'M3FD_Fusion' / 'Vis',
            dest_folder=self._base_folder / 'fusion' / 'vis'
        )
        shutil.rmtree(self._base_folder / 'M3FD-Fusion-Backup-master')
