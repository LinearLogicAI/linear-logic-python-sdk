from os import PathLike
from typing import Callable, Iterator, List
from linlog.schemas import Task


ExportParser = Callable[[Iterator[Task]], None]


def export_tasks(
    exporter: ExportParser,
    tasks: List[Task],
    output_directory: PathLike,
) -> None:
    print("Converting tasks...")
    _, save_path = exporter(
        tasks=tasks,
        output_path=output_directory
    )
    print(f"Converted annotations saved at {save_path}")
