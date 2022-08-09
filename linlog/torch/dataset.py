import torch
import math
import numpy as np
from linlog.utils import compute_polygon_area, convert_bbox_to_polygon
from linlog.dataset import LocalDataset
from torch.utils.data import Dataset as TorchDatset
from torchvision import transforms


class ObjectDetectionDataset(TorchDatset):

    dataset: LocalDataset

    def __init__(self, path: str, transform=None):
        self.dataset = LocalDataset(path)
        self.transform = transform

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()

        convert_tensor = transforms.ToTensor()
        image, task = self.dataset[idx]

        def get_area(annotation):
            vertices = convert_bbox_to_polygon(annotation)
            x_coords = [v['x'] for v in vertices]
            y_coords = [v['y'] for v in vertices]

            return np.sum([compute_polygon_area(x_coord, y_coord) for x_coord, y_coord in zip(x_coords, y_coords)])

        if len(task.get('annotations', [])) == 0:
            boxes = torch.zeros((0, 4), dtype=torch.float32)
            area = torch.as_tensor([0], dtype=torch.float32)
        else:
            boxes = torch.as_tensor([[ 
                a['left'], a['top'], a['left'] + a['width'], a['top'] + a['height'] 
            ] for a in task.get('annotations', [])], dtype=torch.float32)

            area = torch.as_tensor(
                [get_area(a) for a in task.get('annotations', [])],
                dtype=torch.float32
            )


        # there is only one class
        labels = torch.as_tensor([self.dataset.label_mapping[a['label']] for a in task.get('annotations', [])], dtype=torch.int64)

        image_id = torch.tensor([idx])
        
        # suppose all instances are not crowd
        iscrowd = torch.zeros((len(task.get('annotations', [])),), dtype=torch.int64)
        
        masks = []

        for annotation in task.get('annotations', []):
            mask = np.zeros((image.size[:2]))

            x = math.floor(annotation['left'])
            x1 = math.ceil(x + annotation['width'])

            y = math.floor(annotation['top'])
            y1 = math.ceil(y + annotation['height'])

            mask[x:x1,y:y1] = 1
            masks.append(mask)

        masks = torch.tensor(masks)

        target = {}
        target["boxes"] = boxes
        target["labels"] = labels
        target["image_id"] = image_id
        target["area"] = area
        target["masks"] = masks
        target["iscrowd"] = iscrowd

        if self.transform is not None:
            image, target = self.transform(image, target)

        return convert_tensor(image), target
