from typing import Callable, Optional, Union
from pathlib import Path
from torchvision.datasets.vision import VisionDataset
from torchvision.datasets.utils import check_integrity, download_and_extract_archive
import cv2
from PIL import Image

__all__ = ['INO']

class INO(VisionDataset):
    file = {
        'INO Crossroads':{
            'url': 'https://inostorage.blob.core.windows.net/media/1546/ino_crossroads.zip',
            'md5': '0856f906e660290d3f581c9e71f5b544',
            'extract_root_modify': True,
            'addition': 'INO_Crossroads',
            'vis': True,
            'ir': False,
            'mask': False,
            'resolution': (320,240),
            'length': 760,
            'img_p_sed': 10,
        },
        'INO Trees and runner':{
            'url': 'https://inostorage.blob.core.windows.net/media/2518/ino_treesandrunner.zip',
            'md5': 'd9fff5d4f4a982b8a2ea147c363fc62f',
            'extract_root_modify': False,
            'addition': 'INO_TreesAndRunner',
            'vis': True,
            'ir': True,
            'mask': False,
            'resolution': (328,254),
            'length': 558,
            'img_p_sed': 10,
        },
        'INO Visitor parking':{
            'url': 'https://inostorage.blob.core.windows.net/media/2517/ino_visitorparking.zip',
            'md5': 'e1d9606f24ba421fc61194184b8800d2',
            'extract_root_modify': False,
            'addition': 'INO_VisitorParking',
            'vis': True,
            'ir': True,
            'mask': False,
            'resolution': (328,254),
            'length': 472,
            'img_p_sed': 10,
        },
        'INO Main entrance':{
            'url': 'https://inostorage.blob.core.windows.net/media/2520/ino_mainentrance.zip',
            'md5': '9adb72f3f5daeeeb39167cff27776459',
            'extract_root_modify': False,
            'addition': 'INO_MainEntrance',
            'vis': True,
            'ir': False,
            'mask': False,
            'resolution': (328,254),
            'length': 551,
            'img_p_sed': 10,
        },
        'INO Parking evening':{
            'url': 'https://inostorage.blob.core.windows.net/media/2519/ino_parkingevening.zip',
            'md5': 'a8010c369b174d7231734ba9e5a6dd46',
            'extract_root_modify': False,
            'addition': 'INO_ParkingEvening',
            'vis': True,
            'ir': True,
            'mask': False,
            'resolution': (328,254),
            'length': 820,
            'img_p_sed': 10,
        },
        'INO Close person':{
            'url': 'https://inostorage.blob.core.windows.net/media/1551/ino_closeperson.zip',
            'md5': '99aac2b32d35db80000e78dcfb50c5bd',
            'extract_root_modify': False,
            'addition': 'INO_ClosePerson',
            'vis': True,
            'ir': True,
            'mask': False,
            'resolution': (512,184),
            'length': 240,
            'img_p_sed': 10,
        },
        'INO Coat deposit':{
            'url': 'https://inostorage.blob.core.windows.net/media/1552/ino_coatdeposit.zip',
            'md5': '04f7c4bda7605639fbd321c4a44a411b',
            'extract_root_modify': True,
            'addition': 'INO_CoatDeposit',
            'vis': True,
            'ir': True,
            'mask': True,
            'resolution': (512,184),
            'length': 2030,
            'img_p_sed': 10,
        },
        'INO Multiple deposit':{
            'url': 'https://inostorage.blob.core.windows.net/media/1554/ino_multipledeposit.zip',
            'md5': '86e61100abcc96cfdf31e02d4a4eb418',
            'extract_root_modify': True,
            'addition': 'INO_MultipleDeposit',
            'vis': True,
            'ir': True,
            'mask': True,
            'resolution': (448,324),
            'length': 2400,
            'img_p_sed': 10,
        },
        'INO Backyard runner':{
            'url': 'https://inostorage.blob.core.windows.net/media/1550/ino_backyardrunner.zip',
            'md5': 'f3611ed4bc5484807b3e3f9566f4c837',
            'extract_root_modify': True,
            'addition': 'INO_BackyardRunner',
            'vis': True,
            'ir': True,
            'mask': False,
            'resolution': (448,324),
            'length': 1201,
            'img_p_sed': 10,
        },
        'INO Group fight':{
            'url': 'https://inostorage.blob.core.windows.net/media/1553/ino_groupfight.zip',
            'md5': 'a9e289258592dd19d0ee7a80ddaea3fc',
            'extract_root_modify': True,
            'addition': 'INO_GroupFight',
            'vis': True,
            'ir': True,
            'mask': True,
            'resolution': (452,332),
            'length': 1482,
            'img_p_sed': 10,
        },
        'INO Parking snow':{
            'url': 'https://inostorage.blob.core.windows.net/media/1555/ino_parkingsnow.zip',
            'md5': '81e2df675174a299b030d1977869c442',
            'extract_root_modify': True,
            'addition': 'INO_ParkingSnow',
            'vis': True,
            'ir': True,
            'mask': True,
            'resolution': (448,324),
            'length': 2941,
            'img_p_sed': 10,
        },
        'Highway I':{
            'url': 'https://inostorage.blob.core.windows.net/media/1548/highwayi.zip',
            'md5': '99c35b03c278a6f3585307150f3d03cf',
            'extract_root_modify': True,
            'addition': 'HighwayI',
            'vis': False,
            'ir': False,
            'mask': False,
            'resolution': (320,240),
            'length': 440,
            'img_p_sed': 14,
        },
        'Lobby':{
            'url': 'https://inostorage.blob.core.windows.net/media/1556/lobby.zip',
            'md5': '55b80978681510e16a764c7990c7132d',
            'extract_root_modify': True,
            'addition': 'Lobby',
            'vis': False,
            'ir': False,
            'mask': False,
            'resolution': (160,128),
            'length': 2545,
            'img_p_sed': 10,
        },
        'Campus':{
            'url': 'https://inostorage.blob.core.windows.net/media/1547/campus.zip',
            'md5': 'a43f27ef135a304da1b3806684688ef4',
            'extract_root_modify': True,
            'addition': 'Campus',
            'vis': False,
            'ir': False,
            'mask': False,
            'resolution': (160,128),
            'length': 2438,
            'img_p_sed': 10,
        },
        'Highway III':{
            'url': 'https://inostorage.blob.core.windows.net/media/1549/highwayiii.zip',
            'md5': '2eb33705a561847afebc022cba247f65',
            'extract_root_modify': True,
            'addition': 'HighwayIII',
            'vis': False,
            'ir': False,
            'mask': True,
            'resolution': (320,240),
            'length': 2237,
            'img_p_sed': 10,
        }
    }

    def __init__(
        self,
        root: Union[str, Path],
        transform: Optional[Callable] = None,
        download: bool = True,
        mode: str = 'image',
    ) -> None:
        super().__init__(root, transform=transform)
        self._base_folder = Path(self.root) / "ino"
        self.mode = mode

        if download:
            self.download()
        
        if mode == 'image':
            self.to_image()
        else:
            ValueError("Not Realise yet!")
    
    def __getitem__(self, idx: int):
        if self.mode == 'image':
            ir_file = self.ir_image[idx]
            ir = Image.open(ir_file).convert("L")
            vis_file = self.vis_image[idx]
            vis = Image.open(vis_file).convert("RGB")
            mask_file = self.mask_flag[idx]
            mask = Image.open(mask_file).convert("RGB") if mask_file is not None else None
            if self.transform:
                ir = self.transform(ir)
                vis = self.transform(vis)
                if mask is not None:
                    mask = self.transform(mask)
            return ir,vis,mask
        else:
            ValueError("Not Realise yet!")
        
    def __len__(self) -> int:
        assert self.mode == 'image'
        return len(self.ir_image)
        # if self.mode == 'image':
        #     return len(self.ir_image)
        # else:
        #     ValueError("Not Realise yet!")

    def _check_integrity(self,info):
        if not check_integrity(self._base_folder / f"{info['addition'].lower()}.zip", info["md5"]):
            return False
        
        if not ((self._base_folder/info['addition']).exists() and (self._base_folder/info['addition']).is_dir()):
            return False

        return True
    
    def download(self):
        for _,info in self.file.items():
            if self._check_integrity(info):
                continue
            if info['extract_root_modify']:
                extract_root = self._base_folder / info['addition']
            else:
                extract_root = None
            download_and_extract_archive(
                url=f"{info['url']}",
                download_root=self._base_folder,
                extract_root=extract_root,
                md5=info['md5'],
            )
            if info['addition'] == 'INO_MultipleDeposit':
                (self._base_folder / 'INO_MultipleDeposit' / 'INO_MulitpleDeposit').rename(self._base_folder / 'INO_MultipleDeposit' / 'INO_MultipleDeposit')
                (self._base_folder / 'INO_MultipleDeposit' / 'INO_MultipleDeposit' / 'INO_MulitpleDeposit_RGB.avi').rename(self._base_folder / 'INO_MultipleDeposit' / 'INO_MultipleDeposit' / 'INO_MultipleDeposit_RGB.avi')
                (self._base_folder / 'INO_MultipleDeposit' / 'INO_MultipleDeposit' / 'INO_MulitpleDeposit_T.avi').rename(self._base_folder / 'INO_MultipleDeposit' / 'INO_MultipleDeposit' / 'INO_MultipleDeposit_T.avi')
            if info['addition'] == 'INO_Crossroads':
                (self._base_folder / 'INO_Crossroads' / 'INO_Crossroads' / 'INO_Crossroads.avi').rename(self._base_folder / 'INO_Crossroads' / 'INO_Crossroads' / 'INO_Crossroads_RGB.avi')
            if info['addition'] == 'INO_ParkingSnow':
                (self._base_folder / 'INO_ParkingSnow' / 'INO_ParkingSnow' / 'CSMulti_AM_VIRXCam2000_RGB.avi').rename(self._base_folder / 'INO_ParkingSnow' / 'INO_ParkingSnow' / 'INO_ParkingSnow_RGB.avi')
                (self._base_folder / 'INO_ParkingSnow' / 'INO_ParkingSnow' / 'CSMulti_AM_VIRXCam2000_T.avi').rename(self._base_folder / 'INO_ParkingSnow' / 'INO_ParkingSnow' / 'INO_ParkingSnow_T.avi')
    
    def _extract_frames_by_interval(self, video_path, output_folder):
        cap = cv2.VideoCapture(str(video_path))

        if not cap.isOpened():
            print(f"Failed to open video: {video_path}")
            return

        frame_rate = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        print(f"Processing video: {video_path}")
        print(f"Frame rate: {frame_rate}, Total frames: {total_frames}")

        interval_frames = int(frame_rate)

        frame_idx = 0
        while frame_idx < total_frames:
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
            ret, frame = cap.read()
            if not ret:
                print(f"Failed to read frame {frame_idx} from {video_path}")
                break

            output_path = output_folder / f"{frame_idx}.png"
            cv2.imwrite(str(output_path), frame)

            frame_idx += interval_frames

        cap.release()

    def to_image(self):
        self.ir_image = []
        self.vis_image = []
        self.mask_flag = []
        for _,info in self.file.items():
            img_path = self._base_folder / info['addition'] / info['addition']
            ir_path = img_path / 'ir'
            vis_path = img_path / 'vis'
            mask_path = img_path / f"{info['addition']}_mask.bmp"

            # Process IR video
            if info['ir']:
                if not ir_path.exists():
                    ir_path.mkdir(parents=True, exist_ok=True)
                    ir_video_path = img_path / f"{info['addition']}_T.avi"
                    assert ir_video_path.exists()
                    self._extract_frames_by_interval(ir_video_path, ir_path)

            # Process VIS video
            if info['vis']:
                if not vis_path.exists():
                    vis_path.mkdir(parents=True, exist_ok=True)
                    vis_video_path = img_path / f"{info['addition']}_RGB.avi"
                    assert vis_video_path.exists()
                    self._extract_frames_by_interval(vis_video_path, vis_path)

            if info['vis'] and info['ir']:
                self.ir_image.extend(sorted([str(file) for file in ir_path.glob("*.png")]))
                self.vis_image.extend(sorted([str(file) for file in vis_path.glob("*.png")]))
                self.mask_flag.extend([mask_path if mask_path.exists() else None] * len(list(vis_path.glob("*.png"))))
                assert len(self.vis_image) == len(self.ir_image)

    
