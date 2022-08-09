import json
from datetime import datetime
from typing import List
from linlog.data_types.labels import DatasetLabel
from linlog.data_types.task import Task


def export(tasks: List[Task], labels: List[DatasetLabel]):
    return {
        "config": {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "labels": labels,
        },
        "tasks": tasks
    }
