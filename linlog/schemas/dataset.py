import uuid
import datetime
from linlog.constants import TaskType
from linlog import schemas
from dataclasses import dataclass, field
from linlog.client import LinLogClient
from linlog.constants import (
    IN_MEMORY_PREFIX,
    DATASET_ID_KEY,
    DATASET_DATETIME_FORMAT,
    DATASET_CREATED_DATE_KEY,
    DATASET_NAME_KEY,
    DATASET_TYPE_KEY,
    DATASET_LABELS_KEY,
    DATASET_ITEM_COUNT_KEY,
    DATASET_OBJECT_COUNT_KEY,
    DATASET_LABEL_NAME_KEY,
    DATASET_LABEL_TYPE_KEY,
)


@dataclass
class DatasetLabel:

    label: str
    type: str

    @classmethod
    def from_json(cls, payload: dict) -> 'DatasetLabel':
        return cls(
            label=payload.get(DATASET_LABEL_NAME_KEY, None),
            type=payload.get(DATASET_LABEL_TYPE_KEY, None),
        )

    def to_dict(self) -> Dict:
        return {
            DATASET_LABEL_NAME_KEY: self.label,
            DATASET_LABEL_TYPE_KEY: self.type,
        }

    def __eq__(self, other) -> bool:
        return self.label == other.label and self.type == other.type

    def __str__(self) -> str:
        return f"DatasetLabel(label={self.label},type={self.type})"


@dataclass
class Dataset:

    name: str
    type: str

    id: str = None
    created_date: datetime.datetime = None
    item_count: int = 0
    object_count: int = 0
    completed_tasks: int = 0
    labels: List[DatasetLabel] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.id is None:
            self.id = IN_MEMORY_PREFIX + str(uuid.uuid4())

    @classmethod
    def from_json(cls, payload: dict) -> 'Dataset':
        return cls(
            id=payload.get(DATASET_ID_KEY, None),
            created_date=datetime.datetime.strptime(
                payload.get(DATASET_CREATED_DATE_KEY),
                DATASET_DATETIME_FORMAT
            ) if payload.get(DATASET_CREATED_DATE_KEY) else None,
            name=payload.get(DATASET_NAME_KEY, None),
            type=payload.get(DATASET_TYPE_KEY, None),
            item_count=payload.get(DATASET_ITEM_COUNT_KEY, 0),
            object_count=payload.get(DATASET_OBJECT_COUNT_KEY, 0),
            labels=[DatasetLabel.from_json(label) for label in
                payload.get(DATASET_LABELS_KEY, [])]
        )

    def to_dict(self) -> Dict:
        return {
            DATASET_ID_KEY: self.id,
            DATASET_CREATED_DATE_KEY: self.created_date
                .strftime(DATASET_DATETIME_FORMAT)
                if self.created_date else None,
            DATASET_NAME_KEY: self.name,
            DATASET_TYPE_KEY: self.type,
            DATASET_ITEM_COUNT_KEY: self.item_count,
            DATASET_OBJECT_COUNT_KEY: self.object_count,
            DATASET_LABELS_KEY: [label.to_dict() for label in self.labels]
        }

    @classmethod
    def create(
        self,
        client: LinLogClient,
        project_title: str,
        project_type: str
    ):
        return Dataset.from_json(
            client.create_project(project_title, project_type)
        )

    @classmethod
    def get_by_id(self, client: LinLogClient, id: str):
        return Dataset.from_json(
            client.get_dataset(id)
        )

    @classmethod
    def get_all(self, client: LinLogClient):
        return list(map(
            lambda dataset: Dataset.from_json(dataset), client.get_datasets()
        ))

    def get_tasks(self, client: LinLogClient, **kwargs):

        tasks = client.get_dataset_tasks(self.id, **kwargs)
        tasks.transform_results(lambda task: schemas.Task.from_json(task))
        return tasks

    def save(self, client: LinLogClient):
        payload = self.to_dict()
        client.update_project(self.id, payload)
        return True

    def delete(self, client: LinLogClient):
        client.delete_project(self.id)
        return True

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
        return f"Dataset(id={self.id})"
