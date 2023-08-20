import datetime
import itertools
import json
from pathlib import Path
from typing import List
from linlog.schemas import Task


def export(tasks: List[Task], output_path: Path):
    root = create_root()
    root['item_count'] = len(tasks)
    root['labels'] = list(create_labels(tasks))
    root['items'] = [task.to_dict() for task in tasks]

    output_file_path = (output_path / "output").with_suffix(".json")

    with open(output_file_path, "w") as f:
        json.dump(root, f, indent=2)

    return root, output_file_path


def create_root():
    return {
        "version": "2.0",
        "dumped_at": str(datetime.datetime.now(tz=datetime.timezone.utc))
    }


def create_labels(tasks: List[Task]):
    annotations = list(itertools.chain(*[task.annotations for task in tasks]))
    labels = set([annotation.label for annotation in annotations])
    for idx, label in enumerate(labels):
        yield {"id": idx, "name": label}
