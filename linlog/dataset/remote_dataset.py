from dataclasses import dataclass, field
import os
import shutil
from typing import List
from awesome_progress_bar import ProgressBar
from linlog.client import LinLogClient
from linlog.constants import MODULE_ROOT
from linlog.exporter import get_exporter
from linlog.exporter.exporter import export_tasks
from linlog.schemas.dataset import Dataset
from linlog.schemas.task import Task


@dataclass
class RemoteDataset:

    ll_dataset: Dataset = None
    tasks: List[Task] = field(default_factory=list)

    def __init__(self, client: LinLogClient, id: str) -> None:
        self.client = client
        self.ll_dataset = Dataset.get_by_id(client, id)
        self.tasks = []

    def fetch_tasks(self, exclude_annotations=True) -> List[Task]:

        response = self.ll_dataset.get_tasks(
            self.client,
            offset=0,
            limit=20,
            exclude_annotations=exclude_annotations
        )
        self.tasks.extend(response)

        total = response.count // response.limit
        bar = ProgressBar(
            total,
            bar_length=80,
            prefix="Fetching tasks from server",
            use_eta=True
        )

        while response.offset + response.limit < response.count:
            bar.iter()
            response = self.ll_dataset.get_tasks(
                self.client,
                limit=response.limit,
                offset=response.offset + response.limit,
                exclude_annotations=exclude_annotations
            )
            self.tasks.extend(response)

        bar.stop()
        return self.tasks

    def pull(self):
        self.tasks = []
        self.fetch_tasks(exclude_annotations=False)

    def export(
        self,
        output_directory: os.PathLike,
        format: str = "linearlogic",
        pull: bool = False
    ):
        root = MODULE_ROOT + os.sep + "datasets"
        dataset_root = root + os.sep + self.ll_dataset.name

        if not os.path.isdir(root):
            os.mkdir(root)

        if pull:
            self.pull()
        elif len(self.tasks) == 0:
            raise Exception("No tasks to export, try using pull=True")

        if os.path.isdir(dataset_root):
            shutil.rmtree(dataset_root)

        export_tasks(
            get_exporter(format if format else 'linearlogic'),
            self.tasks,
            output_directory
        )

        return dataset_root

    def __getitem__(self, index):
        return self.tasks[index]

    def __len__(self):
        return len(self.tasks)

    def __str__(self) -> str:
        return f"RemoteDataset(id={self.ll_dataset.id})"
