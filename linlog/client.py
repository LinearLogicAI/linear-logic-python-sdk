import json
from typing import List
from linlog.constants import BASE_URL
from linlog.controller import Controller
from linlog.utils import Paginator


class LinLogClient:

    auth_credentials = None
    controller = None
    auth_type = None

    def __init__(self,
                 email: str,
                 password: str,
                 base_url: str = None,
                 auth_type: str = "token"):

        self.auth_credentials = (email, password) if auth_type == "credentials" else (email, "")
        self.auth_type = auth_type
        self.controller = Controller(self.auth_credentials, base_url=base_url if base_url else BASE_URL)

    @staticmethod
    def init_from_credentials(email: str, password: str, base_url: str = None):
        return LinLogClient(email, password, base_url, "credentials")

    @staticmethod
    def init_from_token(token, base_url: str = None):
        return LinLogClient(token, "", base_url)

    def get_organisation(self):
        endpoint = f"organisations"
        return self.controller.get_request(endpoint)

    def create_project(self,
                       title: str,
                       project_type: str,
                       objects_to_annotate,
                       **args):
        endpoint = "projects"
        return self.controller.post_request(endpoint, {
            "title": title,
            "type": project_type,
            "objects_to_annotate": objects_to_annotate,
            **args
        })

    def copy_project_taxonomy(self,
                              origin_project_id: str,
                              target_project_id: str):
        """
        :param origin_project_id: the project where the taxonomy will be imported into
        :param target_project_id: the project where the taxonomy comes from
        """

        endpoint = f"projects/{origin_project_id}/import-taxonomy"
        return self.controller.post_request(endpoint, {
            "project_id": target_project_id
        })

    def get_project_workflows(self, id: str):
        endpoint = f"projects/{id}/workflows"
        return self.controller.get_request(endpoint)

    def set_project_workflows(self, project_id: str, workflows):
        endpoint = f"projects/{project_id}/workflows"
        return self.controller.post_request(endpoint, workflows)

    def delete_project(self, id: str):
        endpoint = f"projects/{id}"
        return self.controller.delete_request(endpoint)

    def get_projects(self):
        endpoint = "projects"
        return self.controller.get_request(endpoint)

    def get_project(self, id: str):
        endpoint = f"projects/{id}"
        return self.controller.get_request(endpoint)

    def get_project_batches(self, id: str):
        endpoint = f"projects/{id}/batches"
        return self.controller.get_request(endpoint)

    def get_project_tasks(self, id: str, **kwargs):

        for key in kwargs:
            if key not in [
                'limit', 'offset', 'status', 'created_date', 'created_date__gte', 'created_date__lte',
                'created_date__gt', 'created_date__lt', 'complete', 'rejected', 'work_started'
            ]:
                raise Exception(f"Invalid kwarg key: {key}")

        endpoint = f"projects/{id}/tasks"
        response = self.controller.get_request(endpoint, params=kwargs)

        limit = kwargs.get('limit', 100)
        offset = kwargs.get('offset', 0)

        return Paginator[str](
            response["results"],
            response["count"],
            limit,
            offset,
            response["previous"],
            response["next"]
        )

    def create_categorisation_task(self,
                                   project_id: str,
                                   attachment: str,
                                   attachment_type: str = "text",
                                   batch_name: str = None,
                                   annotations = None,
                                   complete: bool = False):
        endpoint = 'tasks/categorisation'

        self.controller.post_request(endpoint, {
            "project": project_id,
            "attachment": attachment,
            "attachment_type": attachment_type,
            "batch_name": batch_name if batch_name else "main (default)",
            "annotations": annotations if bool(annotations) else [],
            "type": 'categorisation',
            "complete": complete
        })

    def upload_image_task(self,
                          project_id: str,
                          image_path: str,
                          task_type: str = "image",
                          annotations = None,
                          complete: bool = False):

        endpoint = 'tasks/image/upload'

        if not annotations:
            annotations = []

        files = {
            'image': open(image_path, 'rb')
        }
        data = {
            "payload": json.dumps({
                "project": project_id,
                "batch_name": None,
                "external_data": False,
                "complete": complete,
                "annotations": annotations,
                "type": task_type,
                "image": {}
            })
        }

        self.controller.post_request(endpoint,
                                     data=data,
                                     files=files,
                                     headers={})

    def get_datasets(self):
        endpoint = "datasets"
        return self.controller.get_request(endpoint)

    def get_dataset(self, id: str):
        endpoint = f"datasets/{id}"
        return self.controller.get_request(endpoint)

    def delete_tasks(self, task_ids: List[str]):
        endpoint = f"tasks"
        return self.controller.post_request(endpoint, { "task_ids": task_ids })

    def create_model_run(self,
                         dataset_id: str,
                         model_version_id: str,
                         task_id: str,
                         annotation,
                         confidence_score: float = None):

        if bool(confidence_score):
            assert 0 <= confidence_score <= 1, "Confidence score must be a value between 0 and 1"

        endpoint = f"datasets/model-run"
        return self.controller.post_request(endpoint, {
            "dataset": dataset_id,
            "model_version": model_version_id,
            "task": task_id,
            "annotation": annotation,
            "confidence_score": confidence_score
        })
