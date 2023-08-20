import json
from os import PathLike
from tqdm import tqdm
from typing import Dict, List
from linlog.schemas import ImageTask, BoundingBoxAnnotation, PolygonAnnotation
from linlog.helpers import decode_rle


def parse_filepath(
    file_paths: List[PathLike],
    exclude_rejected: bool = False,
    exclude_incomplete: bool = False,
):
    tasks = []
    for file_path in file_paths:
        with open(file_path, "r") as f:
            source = json.load(f)
            label_lookup = build_label_lookup(source['categories'])
            for image in tqdm(source['images']):
                task = create_task(image, source['annotations'], label_lookup)
                tasks.append(task)

    return tasks


def build_label_lookup(categories):
    return {
        categories[i]['id']: categories[i]['name'] for i in
            range(len(categories))
    }


def create_task(payload: Dict, annotations_store, label_lookup):
    task = ImageTask(
        attachment=payload.get('file_name'),
        attachment_type='image',
        id=payload.get('id'),
        filename=payload.get('file_name'),
        media_specs=ImageTask.MediaSpecs(
            width=payload.get('width', 0),
            height=payload.get('height', 0)
        )
    )

    annotations = []

    for annotation in find_annotations(payload.get('id'), annotations_store):
        if annotation.get('bbox', []):
            x, y, w, h = annotation['bbox']
            annotations.append(
                BoundingBoxAnnotation(
                    label=label_lookup.get(annotation['category_id']),
                    top=y,
                    left=x,
                    width=w,
                    height=h,
                    rotation=0,
                    is_model_run=False,
                )
            )
        if annotation.get('segmentation'):
            if type(annotation['segmentation']) is not list:
                continue

            annotations.append(
                PolygonAnnotation(
                    label=label_lookup.get(annotation['category_id']),
                    is_model_run=False,
                    attributes={},
                    segments=[
                        PolygonAnnotation.PolygonSegment(
                            path=[
                                PolygonAnnotation.PolygonSegment.Vertices(
                                    x=v[0],
                                    y=v[1]
                                ) for v in decode_rle(
                                    annotation['segmentation'][0]
                                )
                            ],
                            subtraction=[]
                        )
                    ]
                )
            )

    task.annotations = annotations
    return task


def find_annotations(image_id, annotations):
    return filter(
        lambda annotation: annotation.get('image_id') == image_id,
        annotations
    )
