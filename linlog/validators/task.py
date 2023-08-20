from ast import Dict
from typing import List, Tuple, Union
from linlog.constants import (
    PROJECT_TYPE_KEY,
    TASK_ANNOTATIONS_KEY,
    TASK_ATTACHMENT_KEY,
    TASK_ATTACHMENT_TYPE_KEY,
    TASK_PARAMS_KEY,
    TASK_TYPE_KEY,
    TASK_TAGS_KEY,
    ProjectType,
    TaskType
)


def validate_project_payload(
    project: Dict,
    raise_exception=True
) -> Tuple[bool, Union[None, List[str]]]:

    errors = []

    if type(project) is not dict:
        errors.append("Project payload must be a dict instance")

    if project.get(PROJECT_TYPE_KEY) not in ProjectType.get_all():
        errors.append(
            f"Project type '{project.get(PROJECT_TYPE_KEY)}' is not valid"
        )

    if raise_exception:
        raise Exception(errors)

    return len(errors) == 0, errors


def validate_task_payload(
    task: Dict,
    raise_exception=True
) -> Tuple[bool, Union[None, List[str]]]:

    errors = []

    if type(task) is not dict:
        errors.append("Task payload must be a dict instance")

    if task.get(TASK_TYPE_KEY) not in TaskType.get_all():
        errors.append(f"Task type '{task.get(TASK_TYPE_KEY)}' is not valid")

    if type(task.get(TASK_PARAMS_KEY)) is not dict:
        errors.append("Task params are required")

    if type(task[TASK_PARAMS_KEY].get(TASK_ATTACHMENT_KEY)) is not str:
        invalid_type = type(task.get(TASK_ATTACHMENT_KEY))
        errors.append(
            f"Task attachments must be strings, got {invalid_type}"
        )

    if type(task[TASK_PARAMS_KEY].get(TASK_ATTACHMENT_TYPE_KEY)) is not str:
        invalid_type = type(task.get(TASK_ATTACHMENT_TYPE_KEY))

        errors.append(
            f"Task attachment types must be strings, got {invalid_type}"
        )

    if type(task.get(TASK_TAGS_KEY, [])) is not list:
        errors.append(
            f"Task tags must be a list, got {type(task.get(TASK_TAGS_KEY))}"
        )

    if len(task.get(TASK_ANNOTATIONS_KEY, [])) > 0:
        pass

    if raise_exception and len(errors) > 0:
        raise Exception(errors)

    return len(errors) == 0, errors
