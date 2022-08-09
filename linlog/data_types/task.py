from dataclasses import dataclass


@dataclass
class TaskParams:

    attachment: str

    attachment_type: str


@dataclass
class Task:

    id: str

    params: TaskParams
    

