from dataclasses import dataclass


@dataclass
class DatasetLabel:

    label: str
    
    type: str


@dataclass
class ProjectLabel:

    id: str

    label: str
    
    type: str

