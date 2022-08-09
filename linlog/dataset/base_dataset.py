import os
import json
import random
from typing import Dict, List
from linlog.client import LinLogClient
from linlog.exporter.formats import coco, linlog
from linlog.data_types.labels import DatasetLabel


class BaseDataset(object):

    id: str 
    client: LinLogClient

    name: str
    dataset_type: str
    labels: List[DatasetLabel]
    tasks: List = []

    @property
    def label_mapping(self) ->  Dict[str, int]:
        categories: Dict[str, int] = {}
        for obj in self.labels:
            if obj['label'] not in categories and bool(obj['label']):
                categories[obj['label']] = len(categories)
        return categories

    def fetch_tasks():
        raise NotImplementedError

    def export(self, 
               root: str, 
               format: str="linear-logic", 
               pull: bool=True):

        if os.path.isdir(root):
            raise FileExistsError("Root directory already exists")

        if pull:
            self.pull()
        elif len(self.tasks) == 0:
            raise Exception("No tasks to export, try using pull=True")

        os.mkdir(root)

        if format == "coco":
            output = coco.export(self.tasks, self.labels)

            with open(root + os.sep + self.name + ".json", "w") as f:
                json.dump(output, f, indent=2)
        else:
            output = linlog.export(self.tasks, self.labels)
            os.mkdir(root + os.sep + "tasks")

            with open(root + os.sep + "config.json", "w") as f:
                json.dump(output["config"], f, indent=2)

            for task in output['tasks']:
                with open(root + os.sep + "tasks" + os.sep + task['id'] + ".json", "w") as f:
                    json.dump(task, f, indent=2)

    def shuffle_tasks(self):
        random.shuffle(self.tasks)

    def __len__(self):
        return len(self.tasks)

