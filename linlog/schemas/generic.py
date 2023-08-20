from dataclasses import dataclass
from typing import Optional, TypedDict, List


@dataclass
class LabelAttribute:
    name: str
    attribute_type: str


@dataclass
class Label:
    name: str
    task_type: str
    attributes: Optional[List[LabelAttribute]]


class LatLngDict(TypedDict):

    lat: float
    lng: float
    epsg: Optional[int]


class TaskBoundsDict(TypedDict):

    nw: LatLngDict
    ne: LatLngDict
    se: LatLngDict
    sw: LatLngDict


class MinMaxZoomDict(TypedDict):

    min: float
    max: float
