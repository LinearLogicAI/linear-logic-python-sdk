import json
import uuid
from linlog import LinLogClient
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Type, Union
from linlog.constants import (
    IMAGE_TASK_HEIGHT,
    IMAGE_TASK_MEDIA_SPECS,
    IMAGE_TASK_WIDTH,
    TASK_GLOBAL_KEY_KEY,
    TASK_FILENAME_KEY,
    TASK_COMPLETE_KEY,
    TASK_REJECTED_KEY,
    TASK_WORKFLOW_STAGE_KEY,
    TASK_ERRORS_KEY,
    TASK_IS_ERROR_KEY,
    TASK_PROCESSING_KEY,
    TASK_WARNINGS_KEY,
    TASK_PROJECT_ID_KEY,
    TASK_DATASET_ID_KEY,
    TASK_BATCH_KEY,
    TASK_ANNOTATIONS_KEY,
    TASK_ATTACHMENT_KEY,
    TASK_ATTACHMENT_TYPE_KEY,
    TASK_ID_KEY,
    TASK_PARAMS_KEY,
    TASK_TYPE_KEY,
    TASK_TAGS_KEY,
    TASK_METADATA_KEY,
    TASK_EXTERNAL_DATA_KEY,
    TASK_UNIQUE_ID_KEY,
    GEOTASK_ZOOM_KEY,
    GEOTASK_ZOOM_MIN_KEY,
    GEOTASK_ZOOM_MAX_KEY,
    GEOTASK_BOUNDS_KEY,
    GEOTASK_BOUNDS_NW_KEY,
    GEOTASK_BOUNDS_NE_KEY,
    GEOTASK_BOUNDS_SE_KEY,
    GEOTASK_BOUNDS_SW_KEY,
    TaskType
)
from linlog.schemas.annotation import Annotation
from linlog.schemas import LatLngDict, MinMaxZoomDict
from linlog.validators.task import validate_task_payload


@dataclass
class Task:
    """Internal base class, not to be used directly.

    .. todo ::
        Inherit common constructor parameters from here
    """

    attachment: str
    attachment_type: str

    id: str = None
    global_key: str = None
    filename: str = None
    complete: bool = False
    rejected: bool = False
    workflow_stage: str = None
    errors: List = field(default_factory=list)
    error: bool = False
    external_data: bool = False
    processing: bool = False
    annotations: List[Annotation] = field(default_factory=list)
    warnings: List = field(default_factory=list)
    project_id: Optional[str] = None
    dataset_id: Optional[str] = None
    batch: str = None
    unique_id: str = None
    task_type: str = None
    tags: List[str] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.id is None:
            self.id = uuid.uuid4()

    def __setattr__(self, __name: str, __value: Any) -> None:
        protected_fields = [
            TASK_ID_KEY,
            TASK_ATTACHMENT_KEY,
            TASK_ATTACHMENT_TYPE_KEY,
            TASK_DATASET_ID_KEY,
            TASK_PROJECT_ID_KEY,
            TASK_WORKFLOW_STAGE_KEY,
            TASK_GLOBAL_KEY_KEY,
            TASK_EXTERNAL_DATA_KEY,
            TASK_TYPE_KEY
        ]

        if __name in protected_fields and bool(self.__dict__.get(__name)):
            raise Exception(f"Task {__name}s cannot be changed")

        self.__dict__[__name] = __value

    @classmethod
    def from_json(cls, payload: Union[dict, List[dict]], many=False) -> 'Task':
        """Instantiates annotation object from schematized JSON dict
        payload."""

        if many:
            assert type(payload) is list, \
                "from_json requires payload to be a list when many=True"
        else:
            assert type(payload) is dict, \
                "from_json requires payload to be a dict when many=False"

        type_key_to_type: Dict[str, Type[Annotation]] = {
            TaskType.Image: ImageTask,
            TaskType.Geospatial: GeospatialTask,
        }

        if many:
            return [
                type_key_to_type.get(
                    p.get(TASK_TYPE_KEY, None),
                    ImageTask
                ).from_json(p) for p in payload
            ]

        type_key = payload.get(TASK_TYPE_KEY, None)
        TaskCls = type_key_to_type.get(type_key, ImageTask)
        task = TaskCls.from_json(payload)
        return task

    def to_dict(self) -> 'Task':
        pass

    def assign_to_user(self):
        raise NotImplementedError

    def assign_to_workflow(self):
        raise NotImplementedError

    def save(self, client: 'LinLogClient'):
        payload = self.to_dict()
        _ = validate_task_payload(payload)

        client.update_task(self.id, payload)
        return True

    def delete(self, client: LinLogClient):
        client.delete_tasks([self.id])
        return True


@dataclass
class ImageTask(Task):

    @dataclass
    class MediaSpecs:
        width: int
        height: int

    media_specs: MediaSpecs = None

    VALID_ATTACHMENT_TYPES = ['image']

    def __init__(
        self,
        attachment,
        attachment_type,
        id=None,
        global_key=None,
        filename=None,
        complete=False,
        rejected=False,
        errors=[],
        error=False,
        processing=False,
        warnings=[],
        project_id=None,
        dataset_id=None,
        batch=None,
        annotations=[],
        tags=[],
        workflow_stage=None,
        metadata={},
        external_data=False,
        unique_id=None,
        task_type=None,
        media_specs=None
    ):
        if attachment_type not in self.VALID_ATTACHMENT_TYPES:
            raise ValueError(
                "attachment_type for ImageTask is invalid! " +
                f"Got: \"{attachment_type}\", expected one of: " +
                f"{','.join(self.VALID_ATTACHMENT_TYPES)}"
            )

        super().__init__(
            id=id,
            global_key=global_key,
            filename=filename,
            complete=complete,
            rejected=rejected,
            errors=errors,
            error=error,
            processing=processing,
            warnings=warnings,
            project_id=project_id,
            dataset_id=dataset_id,
            batch=batch,
            task_type=TaskType.Image,
            attachment=attachment,
            attachment_type=attachment_type,
            annotations=annotations,
            tags=tags,
            workflow_stage=workflow_stage,
            metadata=metadata,
            external_data=external_data,
            unique_id=unique_id
        )
        self.media_specs = media_specs

    @classmethod
    def from_json(cls, payload: dict, validate_payload=True) -> 'ImageTask':
        success, _ = validate_task_payload(
            payload, raise_exception=validate_payload
        )

        if not success:
            return None

        return cls(
            id=payload.get(TASK_ID_KEY, None),
            global_key=payload.get(TASK_GLOBAL_KEY_KEY, None),
            filename=payload.get(TASK_FILENAME_KEY, None),
            complete=payload.get(TASK_COMPLETE_KEY, False),
            rejected=payload.get(TASK_REJECTED_KEY, False),
            errors=payload.get(TASK_ERRORS_KEY, []),
            error=payload.get(TASK_IS_ERROR_KEY, False),
            processing=payload.get(TASK_PROCESSING_KEY, False),
            warnings=payload.get(TASK_WARNINGS_KEY, []),
            project_id=payload.get(TASK_PROJECT_ID_KEY, None),
            dataset_id=payload.get(TASK_DATASET_ID_KEY, None),
            batch=payload.get(TASK_BATCH_KEY, None),
            task_type=TaskType.Image,
            attachment=payload.get(TASK_PARAMS_KEY, {})
                .get(TASK_ATTACHMENT_KEY, None),
            attachment_type=payload.get(TASK_PARAMS_KEY, {})
                .get(TASK_ATTACHMENT_TYPE_KEY, None),
            annotations=Annotation.from_json(
              payload.get(TASK_ANNOTATIONS_KEY, []),
              many=True
            ),
            tags=payload.get(TASK_TAGS_KEY, []),
            workflow_stage=payload.get(TASK_WORKFLOW_STAGE_KEY, None),
            metadata=payload.get(TASK_METADATA_KEY, {}),
            external_data=payload.get(TASK_EXTERNAL_DATA_KEY, False),
            unique_id=payload.get(TASK_UNIQUE_ID_KEY, None),
            media_specs=ImageTask.MediaSpecs(
                width=payload
                        .get(IMAGE_TASK_MEDIA_SPECS, {})
                        .get(IMAGE_TASK_WIDTH, 0),
                height=payload
                        .get(IMAGE_TASK_MEDIA_SPECS, {})
                        .get(IMAGE_TASK_HEIGHT, 0),
            )
        )

    def to_dict(self) -> Dict:
        return {
            TASK_ID_KEY: self.id,
            TASK_GLOBAL_KEY_KEY: self.global_key,
            TASK_FILENAME_KEY: self.filename,
            TASK_COMPLETE_KEY: self.complete,
            TASK_REJECTED_KEY: self.rejected,
            TASK_WORKFLOW_STAGE_KEY: self.workflow_stage,
            TASK_ERRORS_KEY: self.errors,
            TASK_IS_ERROR_KEY: self.error,
            TASK_PROCESSING_KEY: self.processing,
            TASK_WARNINGS_KEY: self.warnings,
            TASK_PROJECT_ID_KEY: self.project_id,
            TASK_DATASET_ID_KEY: self.dataset_id,
            TASK_BATCH_KEY: self.batch,
            TASK_TYPE_KEY: self.task_type,
            TASK_PARAMS_KEY: {
                TASK_ATTACHMENT_KEY: self.attachment,
                TASK_ATTACHMENT_TYPE_KEY: self.attachment_type
            },
            TASK_ANNOTATIONS_KEY: list(map(
                lambda annotation: annotation.to_dict(), self.annotations
            )),
            TASK_TAGS_KEY: self.tags,
            TASK_METADATA_KEY: self.metadata,
            TASK_EXTERNAL_DATA_KEY: self.external_data,
            TASK_UNIQUE_ID_KEY: self.unique_id,
            IMAGE_TASK_MEDIA_SPECS: {
                IMAGE_TASK_WIDTH: self.media_specs.width,
                IMAGE_TASK_HEIGHT: self.media_specs.height
            }
        }

    def to_json(self) -> str:
        """Serializes annotation object to schematized JSON string."""
        return json.dumps(self.to_dict(), allow_nan=False)

    def __str__(self) -> str:
        return f"ImageTask(id={self.id})"


@dataclass
class GeospatialTask(Task):

    zoom_min: int = 0
    zoom_max: int = 0

    bounds_nw: LatLngDict = None
    bounds_ne: LatLngDict = None
    bounds_se: LatLngDict = None
    bounds_sw: LatLngDict = None

    VALID_ATTACHMENT_TYPES = ['geospatial']

    def __init__(
        self,
        attachment: str,
        attachment_type: str,
        zoom: MinMaxZoomDict,
        bounds: List[LatLngDict],
        id=None,
        global_key=None,
        filename=None,
        complete=False,
        rejected=False,
        errors=[],
        error=False,
        processing=False,
        warnings=[],
        project_id=None,
        dataset_id=None,
        batch=None,
        annotations=[],
        tags=[],
        workflow_stage=None,
        metadata={},
        external_data=False,
        unique_id=None,
        task_type=None
    ):
        if attachment_type not in self.VALID_ATTACHMENT_TYPES:
            raise ValueError(
                "attachment_type for GeospatialTask is invalid! " +
                f"Got: \"{attachment_type}\", expected one of: " +
                f"{','.join(self.VALID_ATTACHMENT_TYPES)}"
            )

        if len(bounds) != 4:
            raise ValueError(
                "Bounds must be a list with 4 LatLng dictionaries " +
                "(northWest, northEast, southEast, southWest)"
            )

        super().__init__(
            id=id,
            global_key=global_key,
            filename=filename,
            complete=complete,
            rejected=rejected,
            errors=errors,
            error=error,
            processing=processing,
            warnings=warnings,
            project_id=project_id,
            dataset_id=dataset_id,
            batch=batch,
            task_type=TaskType.Geospatial,
            attachment=attachment,
            attachment_type=attachment_type,
            annotations=annotations,
            tags=tags,
            workflow_stage=workflow_stage,
            metadata=metadata,
            external_data=external_data,
            unique_id=unique_id,
        )

        self.zoom_min = zoom.get(GEOTASK_ZOOM_MIN_KEY, 0)
        self.zoom_max = zoom.get(GEOTASK_ZOOM_MAX_KEY, 0)
        self.bounds_nw = bounds.get('nw')
        self.bounds_ne = bounds.get('ne')
        self.bounds_se = bounds.get('se')
        self.bounds_sw = bounds.get('sw')

    @classmethod
    def from_json(
        cls,
        payload: dict,
        validate_payload=True
    ) -> 'GeospatialTask':
        success, _ = validate_task_payload(
            payload, raise_exception=validate_payload
        )

        if not success:
            return None

        return cls(
            id=payload.get(TASK_ID_KEY, None),
            global_key=payload.get(TASK_GLOBAL_KEY_KEY, None),
            filename=payload.get(TASK_FILENAME_KEY, None),
            complete=payload.get(TASK_COMPLETE_KEY, False),
            rejected=payload.get(TASK_REJECTED_KEY, False),
            errors=payload.get(TASK_ERRORS_KEY, []),
            error=payload.get(TASK_IS_ERROR_KEY, False),
            processing=payload.get(TASK_PROCESSING_KEY, False),
            warnings=payload.get(TASK_WARNINGS_KEY, []),
            project_id=payload.get(TASK_PROJECT_ID_KEY, None),
            dataset_id=payload.get(TASK_DATASET_ID_KEY, None),
            batch=payload.get(TASK_BATCH_KEY, None),
            task_type=TaskType.Image,
            attachment=payload
                       .get(TASK_PARAMS_KEY, {})
                       .get(TASK_ATTACHMENT_KEY, None),
            attachment_type=payload
                            .get(TASK_PARAMS_KEY, {})
                            .get(TASK_ATTACHMENT_TYPE_KEY, None),
            annotations=Annotation.from_json(
              payload.get(TASK_ANNOTATIONS_KEY, []),
              many=True
            ),
            tags=payload.get(TASK_TAGS_KEY, []),
            workflow_stage=payload.get(TASK_WORKFLOW_STAGE_KEY, None),
            metadata=payload.get(TASK_METADATA_KEY, {}),
            external_data=payload.get(TASK_EXTERNAL_DATA_KEY, False),
            unique_id=payload.get(TASK_UNIQUE_ID_KEY, None),
            zoom=payload.get(GEOTASK_ZOOM_KEY, {}),
            bounds=payload.get(GEOTASK_BOUNDS_KEY, [])
        )

    def to_dict(self) -> Dict:
        return {
            TASK_ID_KEY: self.id,
            TASK_GLOBAL_KEY_KEY: self.global_key,
            TASK_FILENAME_KEY: self.filename,
            TASK_COMPLETE_KEY: self.complete,
            TASK_REJECTED_KEY: self.rejected,
            TASK_WORKFLOW_STAGE_KEY: self.workflow_stage,
            TASK_ERRORS_KEY: self.errors,
            TASK_IS_ERROR_KEY: self.error,
            TASK_PROCESSING_KEY: self.processing,
            TASK_WARNINGS_KEY: self.warnings,
            TASK_PROJECT_ID_KEY: self.project_id,
            TASK_DATASET_ID_KEY: self.dataset_id,
            TASK_BATCH_KEY: self.batch,
            TASK_TYPE_KEY: self.task_type,
            TASK_PARAMS_KEY: {
                TASK_ATTACHMENT_KEY: self.attachment,
                TASK_ATTACHMENT_TYPE_KEY: self.attachment_type
            },
            TASK_ANNOTATIONS_KEY: list(map(
                lambda annotation: annotation.to_dict(), self.annotations
            )),
            TASK_TAGS_KEY: self.tags,
            TASK_METADATA_KEY: self.metadata,
            TASK_EXTERNAL_DATA_KEY: self.external_data,
            TASK_UNIQUE_ID_KEY: self.unique_id,
            GEOTASK_ZOOM_KEY: self.get_zoom(),
            GEOTASK_BOUNDS_KEY: self.get_bounds()
        }

    def get_zoom(self):
        return {
            GEOTASK_ZOOM_MIN_KEY: self.zoom_min,
            GEOTASK_ZOOM_MAX_KEY: self.zoom_max
        }

    def get_bounds(self):
        return {
            GEOTASK_BOUNDS_NW_KEY: self.bounds_nw,
            GEOTASK_BOUNDS_NE_KEY: self.bounds_ne,
            GEOTASK_BOUNDS_SE_KEY: self.bounds_se,
            GEOTASK_BOUNDS_SW_KEY: self.bounds_sw,
        }

    def to_json(self) -> str:
        """Serializes annotation object to schematized JSON string."""
        return json.dumps(self.to_dict(), allow_nan=False)

    def __str__(self) -> str:
        return f"GeospatialTask(id={self.id})"
