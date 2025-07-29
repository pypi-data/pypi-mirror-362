import torch
from torch.utils.data import DataLoader
from torchvision.transforms import v2
from torchvision.datasets import CocoDetection
from tqdm import tqdm
from pathlib import Path
from cslib.utils import glance
from cslib.datasets.detection import GeneralDetection

def collate_fn(batch):
    '''
    Ref: https://medium.com/fullstackai/how-to-train-an-object-detector-with-your-own-coco-dataset-in-pytorch-319e7090da5
    Ref: https://paperswithcode.github.io/torchbench/coco/
    '''
    return tuple(zip(*batch))

def coco_example_glance():
    root_dir_50 = Path('/Volumes/Charles/DateSets/Detection/coco2017_50')
    dataset = GeneralDetection(root_dir_50)
    dataloader = DataLoader(dataset, batch_size=1, shuffle=False, num_workers=1, collate_fn=collate_fn)
    for imgs, annotations in dataloader:
        # print(annotations)
        # ({
        #     'boxes': BoundingBoxes([[  0.8200,   0.9200, 637.6300, 361.1700],
        #        [222.8900,  34.5400, 432.6200, 247.5600],
        #        [ 27.8400, 216.8600, 616.8300, 314.9500]], 
        #        format=BoundingBoxFormat.XYXY, 
        #        canvas_size=(640, 366)), 
        #     'labels': tensor([1, 1, 1]), 
        #     'image_id': tensor([2592]), 
        #     'area': tensor([223563.6719,  32698.2305,  21460.5254]), 
        #     'iscrowd': tensor([0, 0, 0])
        # },)
        glance(imgs[0],annotations=annotations)
        break

def coco_example_diy():
    root_dir_50 = Path('/Volumes/Charles/DateSets/Detection/coco2017_50')
    transform = v2.Compose([
        v2.Resize((224, 224), antialias=True), 
        v2.ToImage(), 
        v2.ToDtype(torch.float32, scale=True)
    ])
    dataset = GeneralDetection(root_dir_50, transform=transform)
    dataloader = DataLoader(dataset, batch_size=8, shuffle=True, num_workers=4,collate_fn=collate_fn)
    pbar = tqdm(dataloader, total=len(dataloader))
    for count, (images, labels) in enumerate(pbar):
        pbar.set_description(f"Processing [{count}/{len(dataloader)}]")

    
def coco_example_official():
    root_dir_50 = Path('/Volumes/Charles/DateSets/Detection/coco2017_50')
    transform = v2.Compose([
        v2.Resize((224, 224), antialias=True), 
        v2.ToImage(), 
        v2.ToDtype(torch.float32, scale=True)
    ])
    dataset = CocoDetection(
        root = (root_dir_50 / "train2017").__str__(), 
        annFile = (root_dir_50 / "annotations/instances_train2017.json").__str__(), 
        transform = transform)
    dataloader = DataLoader(dataset, batch_size=8, shuffle=True, num_workers=4,collate_fn=collate_fn)
    pbar = tqdm(dataloader, total=len(dataloader))
    for count, (images, labels) in enumerate(pbar):
        pbar.set_description(f"Processing [{count}/{len(dataloader)}]")


if __name__ == '__main__':
    ''' Coco - Mini size of 50 | 1000 | 3000

        Datasets Structure:
        coco/
        ├── annotations/
        │   ├── instances_train2017.json
        │   ├── instances_val2017.json
        ├── train2017/
        │   ├── <image_files>.jpg
        ├── val2017/
        │   ├── <image_files>.jpg
    '''
    # 1. Without transfrom & Without tqdm
    # batch size should be one, because images have different size
    # Just load one picture, and use glance to check img and box 
    # coco_example_glance()

    # 2. With transfrom & With tqdm -> diy dataset
    # coco_example_diy()

    # 3. With torch official class
    # coco_example_official()
    