import numpy as np
from typing import List, Union
from linlog.constants import AnnotationType
from linlog.schemas.annotation import BoundingBoxAnnotation, PolygonAnnotation


def convert_bbox_to_polygon(
    annotation: BoundingBoxAnnotation
) -> PolygonAnnotation:
    assert annotation.annotation_type == AnnotationType.BoundingBox, \
        "Annotation instance must be a bounding box"

    return PolygonAnnotation(
        label=annotation.label,
        segments=[
            PolygonAnnotation.PolygonSegment(
                path=[
                    PolygonAnnotation.PolygonSegment.Vertices(
                        x=annotation.left,
                        y=annotation.top
                    ),
                    PolygonAnnotation.PolygonSegment.Vertices(
                        x=annotation.left + annotation.width,
                        y=annotation.top
                    ),
                    PolygonAnnotation.PolygonSegment.Vertices(
                        x=annotation.left + annotation.width,
                        y=annotation.top + annotation.height
                    ),
                    PolygonAnnotation.PolygonSegment.Vertices(
                        x=annotation.left,
                        y=annotation.top + annotation.height
                    )
                ],
                subtraction=[]
            )
        ],
        is_model_run=False
    )


def polygon_sequence(
    vertices,
    rounded: bool = False
) -> List[Union[int, float]]:

    path: List[Union[int, float]] = []

    for (_x, _y) in vertices:
        # Clip coordinates to the image size
        x = max(_x, 0)
        y = max(_y, 0)
        if rounded:
            path.append(round(x))
            path.append(round(y))
        else:
            path.append(x)
            path.append(y)

    return path


def compute_polygon_area(xs, ys):
    return 0.5 * np.abs(
        np.dot(xs, np.roll(ys, 1)) - np.dot(ys, np.roll(xs, 1))
    )


def decode_rle(points: List[Union[int, float]]):
    result = []
    for i in range(0, len(points), 2):
        x, y = points[i:i+2]
        result.append((x, y))
    return result
