import json
from typing import List
from linlog.data_types.labels import DatasetLabel
from linlog.data_types.task import Task


def export(tasks: List[Task], labels: List[DatasetLabel]):
    return [
        format_task(task) for task in tasks
    ]


def format_task(task: Task):
    return {
        "text": task['params']['attachment'],
        "tokens": task['tokens'],

    }