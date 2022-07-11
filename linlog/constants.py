from enum import Enum


BASE_URL = 'https://www.linearlogic.ai/api/v1'


class TaskType(Enum):
    Image = "image"
    Categorisation = "categorisation"
    NamedEntities = "ner"
