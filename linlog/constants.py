import os
import linlog
from enum import Enum


BASE_URL = 'https://linearlogic.ai/api/v1'

MODULE_ROOT = os.path.expanduser("~") + os.sep + ".linear-logic"


class TaskType(Enum):
    Image = "image"
    OCR = "ocr"
    Video = "video"
    Categorisation = "categorisation"
    NamedEntities = "ner"

