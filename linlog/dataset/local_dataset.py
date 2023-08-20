import os
from typing import List
from linlog import schemas
from linlog.importer import get_importer
from linlog.exporter import get_exporter
from linlog.importer.importer import import_tasks
from linlog.exporter.exporter import export_tasks
from dataclasses import dataclass, field


@dataclass
class LocalDataset:

    tasks: List[schemas.Task] = field(default_factory=list)

    def load(self, filepaths: List[os.PathLike], format: str = 'linearlogic'):
        importer = get_importer(format)
        results = import_tasks(
            importer,
            filepaths
        )
        self.tasks.extend(results)

    def export(self, format: str, output_directory: os.PathLike):
        exporter = get_exporter(format)
        export_tasks(
            exporter,
            self.tasks,
            output_directory
        )

    def __len__(self):
        return len(self.tasks)

    def __getitem__(self, index) -> schemas.Task:
        return self.tasks[index]
