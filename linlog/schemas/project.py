import uuid
import random
import datetime
from linlog.constants import TaskType
from linlog import schemas
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union
from linlog.client import LinLogClient
from linlog.constants import (
    IN_MEMORY_PREFIX,
    PROJECT_ANNOTATION_ATTRIBUTES_KEY,
    PROJECT_COMPLETED_TASKS_KEY,
    PROJECT_ID_KEY,
    PROJECT_CREATED_DATE_KEY,
    PROJECT_DATETIME_FORMAT,
    PROJECT_ITEM_COUNT_KEY,
    PROJECT_TITLE_KEY,
    PROJECT_TYPE_KEY,
    PROJECT_OBJECTS_TO_ANNOTATE_KEY,
    OBJECT_TO_ANNOTATE_ID_KEY,
    OBJECT_TO_ANNOTATE_NAME_KEY,
    OBJECT_TO_ANNOTATE_DISPLAY_NAME_KEY,
    OBJECT_TO_ANNOTATE_TASK_TYPE_KEY,
    OBJECT_TO_ANNOTATE_RAW_COLOUR_CODE_KEY,
)


@dataclass
class ObjectToAnnotate:

    name: str
    task_type: str

    id: Optional[str] = None
    display_name: Optional[str] = None

    colour_r: Optional[Union[int, float]] = None
    colour_g: Optional[Union[int, float]] = None
    colour_b: Optional[Union[int, float]] = None

    def __post_init__(self) -> None:
        if self.id is None:
            self.id = IN_MEMORY_PREFIX + str(uuid.uuid4())

        if self.colour_r is None:
            self.colour_r = round(random.random() * 255)
        if self.colour_g is None:
            self.colour_g = round(random.random() * 255)
        if self.colour_b is None:
            self.colour_b = round(random.random() * 255)

    @classmethod
    def from_json(cls, payload: dict) -> 'ObjectToAnnotate':
        return cls(
            id=payload.get(OBJECT_TO_ANNOTATE_ID_KEY, None),
            name=payload.get(OBJECT_TO_ANNOTATE_NAME_KEY, None),
            display_name=payload
                .get(OBJECT_TO_ANNOTATE_DISPLAY_NAME_KEY, None),
            task_type=payload.get(OBJECT_TO_ANNOTATE_TASK_TYPE_KEY, None),
            colour_r=payload
                .get(OBJECT_TO_ANNOTATE_RAW_COLOUR_CODE_KEY, {})
                .get('r', 0),
            colour_g=payload
                .get(OBJECT_TO_ANNOTATE_RAW_COLOUR_CODE_KEY, {})
                .get('g', 0),
            colour_b=payload
                .get(OBJECT_TO_ANNOTATE_RAW_COLOUR_CODE_KEY, {})
                .get('b', 0)
        )

    def to_dict(self) -> Dict:
        return {
            OBJECT_TO_ANNOTATE_ID_KEY: self.id,
            OBJECT_TO_ANNOTATE_NAME_KEY: self.name,
            OBJECT_TO_ANNOTATE_DISPLAY_NAME_KEY: self.display_name,
            OBJECT_TO_ANNOTATE_TASK_TYPE_KEY: self.task_type,
            OBJECT_TO_ANNOTATE_RAW_COLOUR_CODE_KEY: {
                "r": self.colour_r,
                "g": self.colour_g,
                "b": self.colour_b
            }
        }

    def _to_internal_payload(self):
        payload = self.to_dict()
        payload[OBJECT_TO_ANNOTATE_RAW_COLOUR_CODE_KEY + "_r"] = self.colour_r
        payload[OBJECT_TO_ANNOTATE_RAW_COLOUR_CODE_KEY + "_g"] = self.colour_g
        payload[OBJECT_TO_ANNOTATE_RAW_COLOUR_CODE_KEY + "_b"] = self.colour_b
        return payload

    def delete(self, client: 'LinLogClient'):
        client.delete_project_label(self.id)
        return True

    def save(self, client: 'LinLogClient'):
        payload = self.to_dict()
        client.update_project_label(self.id, payload)
        return True

    def __eq__(self, other) -> bool:
        return self.id == other.id

    def __str__(self) -> str:
        return f"ObjectToAnnotate(id={self.id},name={self.name})"


@dataclass
class Project:

    title: str
    type: str

    id: str = None
    created_date: datetime.datetime = None
    item_count: int = 0
    completed_tasks: int = 0
    annotation_attributes: List[schemas.ProjectAttribute] = \
        field(default_factory=list)
    objects_to_annotate: List[ObjectToAnnotate] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.id is None:
            self.id = IN_MEMORY_PREFIX + str(uuid.uuid4())

    @classmethod
    def from_json(cls, payload: dict) -> 'Project':
        return cls(
            id=payload.get(PROJECT_ID_KEY, None),
            created_date=datetime.datetime.strptime(
                payload.get(PROJECT_CREATED_DATE_KEY),
                PROJECT_DATETIME_FORMAT
            ) if payload.get(PROJECT_CREATED_DATE_KEY) else None,
            title=payload.get(PROJECT_TITLE_KEY, None),
            type=payload.get(PROJECT_TYPE_KEY, None),
            item_count=payload.get(PROJECT_ITEM_COUNT_KEY, 0),
            completed_tasks=payload.get(PROJECT_COMPLETED_TASKS_KEY, 0),
            annotation_attributes=list(map(
                lambda attribute: schemas.ProjectAttribute
                    .from_json(attribute),
                payload.get(PROJECT_ANNOTATION_ATTRIBUTES_KEY, [])
            )),
            objects_to_annotate=[
                ObjectToAnnotate.from_json(oa) for oa in
                payload.get(PROJECT_OBJECTS_TO_ANNOTATE_KEY, [])
            ]
        )

    def to_dict(self) -> Dict:
        return {
            PROJECT_ID_KEY: self.id,
            PROJECT_CREATED_DATE_KEY: self.created_date
                .strftime(PROJECT_DATETIME_FORMAT)
                if self.created_date else None,
            PROJECT_TITLE_KEY: self.title,
            PROJECT_TYPE_KEY: self.type,
            PROJECT_ITEM_COUNT_KEY: self.item_count,
            PROJECT_COMPLETED_TASKS_KEY: self.completed_tasks,
            PROJECT_OBJECTS_TO_ANNOTATE_KEY: list(map(
                lambda oa: oa.to_dict(), self.objects_to_annotate
            ))
        }

    @classmethod
    def create(
        self,
        client: LinLogClient,
        project_title: str,
        project_type: str
    ):
        return Project.from_json(
            client.create_project(project_title, project_type)
        )

    @classmethod
    def get_by_id(self, client: LinLogClient, id: str):
        return Project.from_json(
            client.get_project(id)
        )

    @classmethod
    def get_all(self, client: LinLogClient):
        return list(map(
            lambda project: Project.from_json(project), client.get_projects()
        ))

    def get_batches(self, client: LinLogClient):
        return client.get_project_batches(self.id)

    def get_tasks(self, client: LinLogClient, **kwargs):
        return list(map(
            lambda task: schemas.Task.from_json(task),
            client.get_project_tasks(self.id, **kwargs)
        ))

    def save(self, client: LinLogClient) -> None:
        payload = self.to_dict()
        client.update_project(self.id, payload)

    def delete(self, client: LinLogClient) -> None:
        client.delete_project(self.id)
        return True

    def create_labels(
        self,
        client: LinLogClient,
        labels: List[ObjectToAnnotate]
    ) -> None:
        for label in labels:
            self.create_label(client, label)

    def create_label(self, client: LinLogClient, label: ObjectToAnnotate):
        label_payload = label.to_dict()
        new_label = client.create_project_label(self.id, label_payload)
        self.objects_to_annotate.append(new_label)

    def create_task(self, client: LinLogClient, task: 'schemas.Task'):
        if task.task_type != self.type:
            raise Exception(
                "Task type does not match project" +
                f" type ({task.task_type}!={self.type})"
            )

        if task.task_type == TaskType.Image:
            client.create_image_task(
                project_id=self.id,
                attachment=task.attachment,
                attachment_type=task.attachment_type,
                batch_name=task.batch,
                annotations=[
                    annotation.to_dict() for annotation in task.annotations
                ],
                external_data=task.external_data,
                complete=task.complete,
                unique_id=task.unique_id
            )
        elif task.task_type == TaskType.Geospatial:
            client.create_geospatial_task(
                project_id=self.id,
                attachment=task.attachment,
                batch_name=task.batch,
                annotations=[
                    annotation.to_dict() for annotation in task.annotations
                ],
                external_data=task.external_data,
                complete=task.complete,
                unique_id=task.unique_id,
                zoom=task.get_zoom(),
                bounds=task.get_bounds()
            )
        elif task.task_type == TaskType.Categorisation:
            client.create_categorisation_task(
                project_id=self.id,
                attachment=task.attachment,
                attachment_type=task.attachment_type,
                batch_name=task.batch,
                annotations=[
                    annotation.to_dict() for annotation in task.annotations
                ],
                external_data=task.external_data,
                complete=task.complete,
                unique_id=task.unique_id
            )

    def __eq__(self, other) -> bool:
        return self.id == other.id

    def __str__(self) -> str:
        return f"Project(id={self.id})"
