import json
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, List, Union, Type, Optional
from linlog.constants import (
    ANNOTATION_ATTRIBUTES_KEY,
    ANNOTATION_ID_KEY,
    ANNOTATION_IOU_KEY,
    ANNOTATION_IS_MODEL_RUN_KEY,
    ANNOTATION_LABEL_KEY,
    ANNOTATION_SOURCE_KEY,
    ANNOTATION_TYPE_KEY,
    BOUNDING_BOX_HEIGHT_KEY,
    BOUNDING_BOX_ROTATION_KEY,
    BOUNDING_BOX_TOP_KEY,
    BOUNDING_BOX_LEFT_KEY,
    BOUNDING_BOX_WIDTH_KEY,
    POLYGON_SEGMENTS_KEY,
    POLYGON_SEGMENTS_PATH_KEY,
    POLYGON_SEGMENTS_SUBTRACTION_KEY,
    AnnotationType
)


class Annotation:
    """Internal base class, not to be used directly.

    .. todo ::
        Inherit common constructor parameters from here
    """
    label: str
    is_model_run: bool
    annotation_type: str = None
    attributes: dict = field(default_factory=dict)

    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name == 'id' and bool(self.__dict__.get('id')):
            raise Exception("Annotation ids cannot be changed")

        self.__dict__[__name] = __value

    @classmethod
    def from_json(cls, payload: Union[dict, List[dict]], many=False):
        """Instantiates annotation object from schematized JSON dict
        payload."""

        if many:
            assert type(payload) is list, \
                "from_json requires payload to be a list when many=True"
        else:
            assert type(payload) is dict, \
                "from_json requires payload to be a dict when many=False"

        type_key_to_type: Dict[str, Type[Annotation]] = {
            AnnotationType.BoundingBox: BoundingBoxAnnotation,
        }
        if many:
            return [
                type_key_to_type.get(
                    p.get(ANNOTATION_TYPE_KEY, None),
                    BoundingBoxAnnotation
                ).from_json(p) for p in payload
            ]

        type_key = payload.get(ANNOTATION_TYPE_KEY, None)
        AnnotationCls = type_key_to_type.get(type_key, BoundingBoxAnnotation)
        return AnnotationCls.from_json(payload)

    def to_dict(self) -> Dict:
        """Serializes annotation object to schematized JSON dict."""
        raise NotImplementedError(
            "For serialization, use a specific subclass "
            "(e.g. SegmentationAnnotation), not the base annotation class."
        )

    def to_json(self) -> str:
        """Serializes annotation object to schematized JSON string."""
        return json.dumps(self.to_dict(), allow_nan=False)


@dataclass
class BoundingBoxAnnotation(Annotation):

    label: str
    top: Union[float, int]
    left: Union[float, int]
    width: Union[float, int]
    height: Union[float, int]
    rotation: Union[float, int]
    is_model_run: bool
    id: Optional[str] = None
    iou: Optional[float] = None
    source: Optional[str] = None
    annotation_type = AnnotationType.BoundingBox
    attributes: dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.id is None:
            self.id = str(uuid.uuid4())

    @classmethod
    def from_json(cls, payload: dict) -> 'BoundingBoxAnnotation':
        return cls(
            id=payload.get(ANNOTATION_ID_KEY, None),
            label=payload.get(ANNOTATION_LABEL_KEY, 0),
            source=payload.get(ANNOTATION_SOURCE_KEY, None),
            is_model_run=payload.get(ANNOTATION_IS_MODEL_RUN_KEY, False),
            left=payload.get(BOUNDING_BOX_LEFT_KEY, 0),
            top=payload.get(BOUNDING_BOX_TOP_KEY, 0),
            width=payload.get(BOUNDING_BOX_WIDTH_KEY, 0),
            height=payload.get(BOUNDING_BOX_HEIGHT_KEY, 0),
            rotation=payload.get(BOUNDING_BOX_ROTATION_KEY, 0),
            iou=payload.get(ANNOTATION_IOU_KEY, 0),
            attributes=payload.get(ANNOTATION_ATTRIBUTES_KEY, dict())
        )

    def to_dict(self) -> Dict:
        return {
            ANNOTATION_ID_KEY: self.id,
            ANNOTATION_LABEL_KEY: self.label,
            ANNOTATION_TYPE_KEY: AnnotationType.BoundingBox,
            ANNOTATION_SOURCE_KEY: self.source,
            ANNOTATION_IS_MODEL_RUN_KEY: self.is_model_run,
            BOUNDING_BOX_TOP_KEY: self.top,
            BOUNDING_BOX_LEFT_KEY: self.left,
            BOUNDING_BOX_WIDTH_KEY: self.width,
            BOUNDING_BOX_HEIGHT_KEY: self.height,
            BOUNDING_BOX_ROTATION_KEY: self.rotation,
            ANNOTATION_IOU_KEY: self.iou,
            ANNOTATION_ATTRIBUTES_KEY: self.attributes
        }

    @property
    def has_iou(self) -> bool:
        return bool(self.iou)

    def __eq__(self, other) -> bool:
        return (
            self.id == other.id
            and self.label == other.label
            and self.x == other.x
            and self.y == other.y
            and self.width == other.width
            and self.height == other.height
            and self.task_id == other.task_id
            and self.id == other.id
        )

    def __str__(self) -> str:
        return f"BoundingBoxAnnotation(id={self.id})"


@dataclass
class PolygonAnnotation(Annotation):

    @dataclass
    class PolygonSegment:

        @dataclass
        class Vertices:
            x: Union[float, int]
            y: Union[float, int]

        path: List[Vertices]
        subtraction: List[Vertices]

        def __init__(
            self,
            path: List[Vertices],
            subtraction: List[Vertices]
        ) -> None:
            self.path = path
            self.subtraction = subtraction

        @classmethod
        def from_json(cls, payload: Dict):
            return cls(
                path=[
                    PolygonAnnotation.Vertices(
                        x=v.get('x', 0),
                        y=v.get('y', 0)
                    ) for v in payload.get(POLYGON_SEGMENTS_PATH_KEY, [])
                ],
                subtraction=[
                    PolygonAnnotation.Vertices(
                        x=v.get('x', 0),
                        y=v.get('y', 0)
                    ) for v in payload
                        .get(POLYGON_SEGMENTS_SUBTRACTION_KEY, [])
                ]
            )

        def to_dict(self):
            return {
                POLYGON_SEGMENTS_PATH_KEY: [
                    {"x": v.x, "y": v.y} for v in self.path
                ],
                POLYGON_SEGMENTS_SUBTRACTION_KEY: [
                    {"x": v.x, "y": v.y} for v in self.subtraction
                ]
            }

    label: str
    segments: List[PolygonSegment]
    is_model_run: bool
    id: Optional[str] = None
    iou: Optional[float] = None
    source: Optional[str] = None
    annotation_type = AnnotationType.Polygon
    attributes: dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.id is None:
            self.id = str(uuid.uuid4())

    @classmethod
    def from_json(cls, payload: dict) -> 'PolygonAnnotation':
        return cls(
            id=payload.get(ANNOTATION_ID_KEY, None),
            label=payload.get(ANNOTATION_LABEL_KEY, 0),
            source=payload.get(ANNOTATION_SOURCE_KEY, None),
            is_model_run=payload.get(ANNOTATION_IS_MODEL_RUN_KEY, False),
            iou=payload.get(ANNOTATION_IOU_KEY, None),
            segments=[
                PolygonAnnotation.PolygonSegment.from_json(segment)
                for segment in payload.get(POLYGON_SEGMENTS_KEY, [])
            ]
        )

    def to_dict(self) -> Dict:
        return {
            ANNOTATION_ID_KEY: self.id,
            ANNOTATION_LABEL_KEY: self.label,
            ANNOTATION_TYPE_KEY: AnnotationType.Polygon,
            ANNOTATION_SOURCE_KEY: self.source,
            ANNOTATION_IS_MODEL_RUN_KEY: self.is_model_run,
            ANNOTATION_IOU_KEY: self.iou,
            POLYGON_SEGMENTS_KEY: [
                segment.to_dict() for segment in self.segments
            ],
            ANNOTATION_ATTRIBUTES_KEY: self.attributes
        }

    @property
    def has_iou(self) -> bool:
        return bool(self.iou)

    def __eq__(self, other) -> bool:
        return (
            self.id == other.id
            and self.label == other.label
            and self.task_id == other.task_id
            and self.id == other.id
        )

    def __str__(self) -> str:
        return f"BoundingBoxAnnotation(id={self.id})"
