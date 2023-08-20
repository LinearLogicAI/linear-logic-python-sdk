import json
import numpy as np
import itertools
from tqdm import tqdm
from pathlib import Path
from typing import Iterator, List, Dict, Union
from datetime import date
from linlog.constants import AnnotationType
from linlog.schemas.annotation import Annotation, PolygonAnnotation
from linlog.schemas.task import ImageTask
from linlog.helpers import (
    compute_polygon_area,
    convert_bbox_to_polygon,
    polygon_sequence
)


def export(tasks: List[ImageTask], output_path: Path):

    label_lookup = list(_build_categories(tasks))
    output = {
        "info": _create_info(),
        "licenses": _create_license(),
        "images": format_images(tasks),
        "annotations": list(format_annotations(tasks, label_lookup)),
        "categories": list(_build_categories(tasks)),
        "tag_categories": list(),
    }

    output_file_path = (output_path / "output-coco").with_suffix(".json")

    with open(output_file_path, "w") as f:
        json.dump(output, f, indent=2)
    return output, output_file_path


def _build_categories(
    tasks: List[ImageTask]
) -> Iterator[Dict[str, Union[str, float, int]]]:

    annotations = list(itertools.chain(*[task.annotations for task in tasks]))
    labels = set([annotation.label for annotation in annotations])
    for idx, label in enumerate(labels):
        yield {"id": idx, "name": label, "supercategory": "root"}


def format_image(task: ImageTask):
    return {
        "license": 0,
        "file_name": task.filename,
        "coco_url": "n/a",
        "height": task.media_specs.height,
        "width": task.media_specs.width,
        "date_captured": "",
        "flickr_url": "n/a",
        "linear_logic_url": task.attachment,
        "id": task.id,
        "tag_ids": [],
    }


def format_images(tasks):
    return [format_image(task) for task in tqdm(tasks, desc="[COCO] Images")]


def format_annotation(task: ImageTask, annotation: Annotation, label_lookup):
    if annotation.annotation_type == AnnotationType.BoundingBox:
        return format_annotation(
            task, convert_bbox_to_polygon(annotation), label_lookup
        )

    elif annotation.annotation_type == AnnotationType.Polygon:
        polygon_annotation: PolygonAnnotation = annotation

        x_coords = [v.x for v in polygon_annotation.segments[0].path]
        y_coords = [v.y for v in polygon_annotation.segments[0].path]
        min_x = float(np.min([np.min(x_coord) for x_coord in x_coords]))
        min_y = float(np.min([np.min(y_coord) for y_coord in y_coords]))
        max_x = float(np.max([np.max(x_coord) for x_coord in x_coords]))
        max_y = float(np.max([np.max(y_coord) for y_coord in y_coords]))
        w = max_x - min_x
        h = max_y - min_y

        # Compute the area of the polygon
        poly_area = float(
            compute_polygon_area(x_coords, y_coords)
        )
        sequence = polygon_sequence(zip(x_coords, y_coords))

        label = next((sub for sub in label_lookup if
            sub['name'] == annotation.label), None)
        if not label:
            print(
                f"[warning] unknown label \"{annotation.label}\", "
                "skipping annotation")
            return None

        return {
            "id": annotation.id,
            "image_id": task.id,
            "category_id": label['id'],
            "segmentation": sequence,
            "area": poly_area,
            "bbox": [min_x, min_y, w, h],
            "iscrowd": 0,
        }


def format_annotations(tasks: List[ImageTask], label_lookup):
    output = []
    for task in tqdm(tasks, desc="[COCO] Annotations"):
        output.extend([
            format_annotation(task, annotation, label_lookup)
            for annotation in task.annotations
        ])
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


def _create_license(
    url: str = "n/a",
    id: int = 0,
    name: str = "placeholder license"
) -> List[Dict[str, Union[str, int, float]]]:

    return [
      {
        "url": url,
        "id": id,
        "name": name
      }
    ]
