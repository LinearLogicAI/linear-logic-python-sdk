import json
import os
import shutil
from glob import glob
from PIL import Image
from typing import ByteString, Tuple
from linlog.constants import MODULE_ROOT
from linlog.data_types.task import Task
from linlog.dataset.base_dataset import BaseDataset


class LocalDataset(BaseDataset):
    
    root: str

    def __init__(self, root: str) -> None:
        self.root = MODULE_ROOT + os.sep + "datasets" + os.sep + root

        with open(self.root + os.sep + "config.json", "r") as f:
            config = json.load(f)
            self.name = config['name']
            self.labels = config['labels']

        self.pull()

    def _load_dataset(self) -> None:

        dataset = self.client.get_dataset(self.id)
        self.name = dataset['name']
        self.dataset_type = dataset['type']
        self.labels = dataset['labels']

    def pull(self):
        for task_fp in glob(self.root + os.sep + "tasks" + os.sep + "*.json"):
            with open(task_fp, "r") as f:
                data = json.load(f)
                self.tasks.append(data)

    def export(self, format: str):
        root = MODULE_ROOT + os.sep + "tensorflow"
        dataset_dir = root + os.sep + self.name

        if not os.path.exists(root):
            os.mkdir(root)

        if os.path.exists(dataset_dir):
            shutil.rmtree(dataset_dir)

        os.mkdir(dataset_dir)

        if format == "tensorflow":
            from linlog.exporter.formats.tensorflow import handle_tf_export
            handle_tf_export(dataset_dir, self)

    def __len__(self):
        return len(self.tasks)

    def __getitem__(self, index) -> Tuple[Task, ByteString]:
        items = self.tasks[index]

        if type(index) is int:
            img = Image.open(self.root + os.sep + "images" + os.sep + items['id'] + ".jpg")
            return (img, items)

        response = []

        for item in items:
            img = Image.open(self.root + os.sep + "images" + os.sep + item['id'] + ".jpg")
            response.append((img, item))

        return response
