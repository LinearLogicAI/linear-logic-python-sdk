import numpy as np
from typing import Dict, Generic, List, TypeVar, Union


T = TypeVar("T")


class Paginator(list, Generic[T]):
    """Paginator for list endpoints"""

    def __init__(
        self,
        results: List[T],
        count: int,
        limit: int,
        offset: int,
        previous_url: Union[str, None],
        next_url: Union[str, None]
    ):
        super().__init__(results)
        self.results = results
        self.count = count
        self.limit = limit
        self.offset = offset
        self.next_url = next_url
        self.previous_url = previous_url


def convert_bbox_to_polygon(annotation) -> List[Dict[str, float]]:
    assert annotation['type'] == 'bounding-box', "Annotation instance must be a bounding box"

    vertices = [
        { "x": annotation['left'], "y": annotation['top'] },
        { "x": annotation['left'] + annotation['width'], "y": annotation['top'] },
        { "x": annotation['left'] + annotation['width'], "y": annotation['top'] + annotation['height'] },
        { "x": annotation['left'], "y": annotation['top'] + annotation['height'] }
    ]

    return vertices


def polygon_sequence(vertices, rounded: bool = False) -> List[Union[int, float]]:

    path: List[Union[int, float]] = []

    for point in vertices:
        # Clip coordinates to the image size
        x = max(point["x"], 0)
        y = max(point["y"], 0)
        if rounded:
            path.append(round(x))
            path.append(round(y))
        else:
            path.append(x)
            path.append(y)

    return path


def compute_polygon_area(xs, ys):

    return 0.5 * np.abs(np.dot(xs, np.roll(ys, 1)) - np.dot(ys, np.roll(xs, 1)))