import uuid
from os import PathLike
from typing import List
import xml.etree.ElementTree as ET
from linlog.schemas import ImageTask, BoundingBoxAnnotation, PolygonAnnotation


def parse_filepath(
    file_paths: List[PathLike],
    exclude_rejected: bool = False,
    exclude_incomplete: bool = False,
):

    tasks = []

    for file_path in file_paths:
        root = ET.parse(open(file_path, 'r'))

        for image in root.iter('image'):
            _id = image.attrib.get(
                'll_id',
                image.attrib.get('id', str(uuid.uuid4()))
            )
            width = image.attrib.get('width', 0)
            height = image.attrib.get('height', 0)
            filename = image.attrib.get('name')

            task = ImageTask(
                attachment=filename,
                attachment_type='image',
                id=_id,
                global_key=None,
                filename=filename,
                media_specs=ImageTask.MediaSpecs(width=width, height=height)
            )

            annotations = []

            for box in image.iter('box'):
                annotations.append(
                    BoundingBoxAnnotation(
                        label=box.attrib.get('label'),
                        top=float(box.attrib.get('ytl')),
                        left=float(box.attrib.get('xtl')),
                        width=float(box.attrib.get('xbr')) -
                            float(box.attrib.get('xtl')),
                        height=float(box.attrib.get('ybr')) -
                            float(box.attrib.get('ytl')),
                        rotation=0,
                        is_model_run=False
                    )
                )

            for polygon in image.iter('polygon'):
                annotations.append(
                    PolygonAnnotation(
                        label=polygon.attrib.get('label'),
                        is_model_run=False,
                        segments=[
                            PolygonAnnotation.PolygonSegment(
                                path=[
                                    PolygonAnnotation.PolygonSegment.Vertices(
                                        x=float(v.split(',')[0]),
                                        y=float(v.split(',')[1])
                                    ) for v in
                                        polygon.attrib
                                            .get('points', '')
                                            .split(';')
                                ],
                                subtraction=[]
                            )
                        ]
                    )
                )

            task.annotations = annotations
            tasks.append(task)

    return tasks
