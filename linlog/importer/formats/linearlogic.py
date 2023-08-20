import json
from os import PathLike
from typing import List
from linlog.schemas import Task


def parse_filepath(
    file_paths: List[PathLike],
    exclude_rejected: bool = False,
    exclude_incomplete: bool = False,
):
    tasks = []
    for file_path in file_paths:
        with open(file_path, "r") as f:
            root = json.load(f)
            for item in root.get('items', []):
                task = Task.from_json(item)

                if task.rejected and exclude_rejected:
                    continue

                if not task.complete and exclude_incomplete:
                    continue

                tasks.append(task)

    return tasks
