from os import PathLike
from typing import Callable, Iterator, List, Union
from pathlib import Path
from linlog.schemas import Task


ImportParser = Callable[[Iterator[Task]], None]


def import_tasks(
    importer: Callable[[Path], Union[List[Task], Task, None]],
    file_paths: List[PathLike],
    exclude_rejected: bool = False,
    exclude_incomplete: bool = False,
) -> List[Task]:
    tasks = importer(
        file_paths=file_paths,
        exclude_rejected=exclude_rejected,
        exclude_incomplete=exclude_incomplete
    )

    return tasks
