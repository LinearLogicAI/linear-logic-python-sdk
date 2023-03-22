import time
import os
import json
import requests
import shutil
from typing import List
from awesome_progress_bar import ProgressBar
from linlog.client import LinLogClient
from linlog.constants import MODULE_ROOT
from linlog.data_types.task import Task
from linlog.dataset.base_dataset import BaseDataset
from linlog.exporter.formats import coco, linlog


class RemoteDataset(BaseDataset):

    def __init__(self, client: LinLogClient, id: str) -> None:
        self.id = id
        self.client = client

        self._load_dataset()

    def _load_dataset(self) -> None:

        dataset = self.client.get_dataset(self.id)
        self.name = dataset['name']
        self.dataset_type = dataset['type']
        self.labels = dataset['labels']
    
    def fetch_tasks(self) -> List[Task]:
        tasks = self.client.get_dataset_tasks(self.id, offset=0, limit=50)
        self.tasks.extend(tasks)

        total = tasks.count // tasks.limit
        bar = ProgressBar(total, bar_length=80, prefix="Fetching tasks from server", use_eta=True)
        
        while tasks.offset + tasks.limit < tasks.count:
            bar.iter()
            tasks = self.client.get_dataset_tasks(self.id, limit=tasks.limit, offset=tasks.offset + tasks.limit)
            self.tasks.extend(tasks)

        bar.stop()
        return self.tasks

    def pull(self):
        self.tasks = self.fetch_tasks()

    def export(self, 
               format: str="linear-logic", 
               pull: bool=True):

        root = MODULE_ROOT + os.sep + "datasets"
        dataset_root = root + os.sep + self.name

        if not os.path.isdir(root):
            os.mkdir(root)

        if pull:
            self.pull()
        elif len(self.tasks) == 0:
            raise Exception("No tasks to export, try using pull=True")

        if os.path.isdir(dataset_root):
            shutil.rmtree(dataset_root)
            
        os.mkdir(dataset_root)

        if format == "coco":
            output = coco.export(self.tasks, self.labels)

            with open(root + os.sep + self.name + ".json", "w") as f:
                json.dump(output, f, indent=2)
        else:
            output = linlog.export(self.tasks, self.labels)
            output["config"]["name"] = self.name
            output["config"]["dataset_type"] = self.dataset_type

            os.mkdir(dataset_root + os.sep + "tasks")
            os.mkdir(dataset_root + os.sep + "images")

            with open(dataset_root + os.sep + "config.json", "w") as f:
                json.dump(output["config"], f, indent=2)

            for task in output['tasks']:
                with open(dataset_root + os.sep + "tasks" + os.sep + task['id'] + ".json", "w") as f:
                    json.dump(task, f, indent=2)

            if task['params']['attachment_type'] == 'image':
                total = len(output['tasks'])
                bar = ProgressBar(total, bar_length=80, prefix="Downloading images", use_eta=True)
                bar.iter()

                for task in output['tasks']:
                    img_data = requests.get(task['params']['attachment']).content
                    with open(dataset_root + os.sep + "images" + os.sep + task['id'] + '.jpg', 'wb') as handler:
                        handler.write(img_data)
                    bar.iter()

                bar.stop()

        return dataset_root

    def __getitem__(self, index):
        return self.tasks[index]
        
