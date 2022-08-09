import numpy as np
from typing import Iterator, List, Dict, Union
from datetime import date
from linlog.data_types.labels import DatasetLabel
from linlog.data_types.task import Task
from linlog.utils import compute_polygon_area, convert_bbox_to_polygon, polygon_sequence


def export(tasks: List[Task], labels: List[DatasetLabel]):

    categories: Dict[str, int] = format_categories(map(lambda l: l['label'], labels))
    tag_categories: Dict[str, int] = {}
    output = {
        "info": _create_info(),
        "licenses": _create_license(),
        "images": format_images(tasks),
        "annotations": list(format_annotations(tasks, categories)),
        "categories": list(_build_categories(categories)),
        "tag_categories": list(),
    }

    return output

def _build_categories(categories: Dict[str, int]) -> Iterator[Dict[str, Union[str, float, int]]]:
    for name, id in categories.items():
        yield {"id": id, "name": name, "supercategory": "root"}

def format_image(task):
    tags = []

    return {
        "license": 0,
        "file_name": task.get('meta', {}).get('filename'),
        "coco_url": "n/a",
        "height": task.get('media_specs', {}).get("height"),
        "width": task.get('media_specs', {}).get("width"),
        "date_captured": "",
        "flickr_url": "n/a",
        "linear_logic_url": task['params']['attachment'],
        "id": task['id'],
        "tag_ids": [],
    }

def format_images(tasks):
    return [format_image(task) for task in tasks]


def format_annotation(annotation, categories):
    if annotation['type'] == 'bounding-box':
        annotation['vertices'] = convert_bbox_to_polygon(annotation)
        annotation['type'] = 'polygon'

        return format_annotation(annotation, categories)

    elif annotation['type'] == 'polygon':

        x_coords = [v['x'] for v in annotation['vertices']]
        y_coords = [v['y'] for v in annotation['vertices']]
        min_x = np.min([np.min(x_coord) for x_coord in x_coords])
        min_y = np.min([np.min(y_coord) for y_coord in y_coords])
        max_x = np.max([np.max(x_coord) for x_coord in x_coords])
        max_y = np.max([np.max(y_coord) for y_coord in y_coords])
        w = max_x - min_x
        h = max_y - min_y
        
        # Compute the area of the polygon
        poly_area = np.sum([compute_polygon_area(x_coord, y_coord) for x_coord, y_coord in zip(x_coords, y_coords)])
        sequence = polygon_sequence(annotation['vertices'])
        
        return {
            "id": annotation['id'],
            "image_id": annotation['id'],
            "category_id": categories[annotation['label']],
            "segmentation": sequence,
            "area": poly_area,
            "bbox": [min_x, min_y, w, h],
            "iscrowd": 0,
            #"extra": _build_extra(annotation),
        }


def format_annotations(tasks, categories):
    output = []
    for task in tasks:
        output.extend([format_annotation(annotation, categories) for annotation in task['annotations']])
    return output

def format_categories(labels: List[str]) -> Dict[str, int]:
    categories: Dict[str, int] = {}
    for label in labels:
        if label not in categories:
            categories[label] = len(categories)
    return categories


def _create_info() -> Dict[str, str]:
    today = date.today()
    return {
        "description": "Exported from Linear Logic",
        "url": "n/a",
        "version": "n/a",
        "year": today.year,
        "contributor": "n/a",
        "date_created": today.strftime("%Y/%m/%d"),
    }


def _create_license(url: str = "n/a", 
                    id: int = 0, 
                    name: str = "placeholder license") -> List[Dict[str, Union[str, int, float]]]:
    return [
      {
        "url": url, 
        "id": id, 
        "name": name
      }
    ]

