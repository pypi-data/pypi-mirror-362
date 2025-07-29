from typing import Union
from torch.utils.data import Dataset
from pathlib import Path
import torch
from pycocotools.coco import COCO
from PIL import Image
from torchvision.transforms import v2
from torchvision import tv_tensors

__all__ = [
    'GeneralDetection'
]

class GeneralDetection(Dataset):
    """
    Mini Coco

    Reference:
        Dataset: https://blog.csdn.net/weixin_40564352/article/details/134054670
        Code: https://medium.com/fullstackai/how-to-train-an-object-detector-with-your-own-coco-dataset-in-pytorch-319e7090da5
        Code: https://pytorch.org/vision/stable/auto_examples/transforms/plot_transforms_getting_started.html#sphx-glr-auto-examples-transforms-plot-transforms-getting-started-py
    """
    def __init__(self,
                 root_dir: Union[str, Path], 
                 transform: v2.Compose = v2.Compose([v2.ToImage(), v2.ToDtype(torch.float32, scale=True)])
        ) -> None:
        super().__init__()
        self.set_name = 'train2017'
        self.root_dir = Path(root_dir)
        self.ann_dir = self.root_dir / f'annotations/instances_{self.set_name}.json'
        self.img_dir = self.root_dir / self.set_name
        self.transform = transform
        self.coco = COCO(str(self.ann_dir)) # Initialize COCO api
        self.ids = list(sorted(self.coco.imgs.keys())) # Get image ids
    
    def __getitem__(self, index):
        # Own coco file
        coco = self.coco
        # Image ID
        img_id = self.ids[index]
        # List: get annotation id from coco
        ann_ids = coco.getAnnIds(imgIds=img_id)
        # Dictionary: target coco_annotation file for an image
        coco_annotation = coco.loadAnns(ann_ids)
        # path for input image
        path = coco.loadImgs(img_id)[0]['file_name']
        # open the input image
        img = Image.open(self.img_dir / path)

        # number of objects in the image
        num_objs = len(coco_annotation)

        # Bounding boxes for objects
        # In coco format, bbox = [xmin, ymin, width, height]
        # In pytorch, the input should be [xmin, ymin, xmax, ymax]
        boxes = []
        for i in range(num_objs):
            xmin = coco_annotation[i]['bbox'][0]
            ymin = coco_annotation[i]['bbox'][1]
            xmax = xmin + coco_annotation[i]['bbox'][2]
            ymax = ymin + coco_annotation[i]['bbox'][3]
            boxes.append([xmin, ymin, xmax, ymax])
        # boxes = torch.as_tensor(boxes, dtype=torch.float32)
        boxes = tv_tensors.BoundingBoxes(boxes,format="XYXY",canvas_size=img.size) # type: ignore
        # Labels (In my case, I only one class: target class or background)
        labels = torch.ones((num_objs,), dtype=torch.int64)
        # Tensorise img_id
        img_id = torch.tensor([img_id])
        # Size of bbox (Rectangular)
        areas = []
        for i in range(num_objs):
            areas.append(coco_annotation[i]['area'])
        areas = torch.as_tensor(areas, dtype=torch.float32)
        # Iscrowd
        iscrowd = torch.zeros((num_objs,), dtype=torch.int64)

        # Do transform
        img, boxes = self.transform(img, boxes)

        # Annotation is in dictionary format
        my_annotation = {}
        my_annotation["boxes"] = boxes
        my_annotation["labels"] = labels
        my_annotation["image_id"] = img_id
        my_annotation["area"] = areas
        my_annotation["iscrowd"] = iscrowd

        return img, my_annotation
    

    def __len__(self):
        return len(self.ids)
