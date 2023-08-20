import os
import json
from typing import Dict, List
from linlog.constants import BASE_URL, MODULE_ROOT
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

        self.auth_credentials = (email, password) \
            if auth_type == "credentials" else (email, "")
        self.auth_type = auth_type
        self.controller = Controller(
            self.auth_credentials,
            base_url=base_url if base_url else BASE_URL
        )

    @staticmethod
    def local(base_url: str = None):
        try:
            with open(MODULE_ROOT + os.sep + "auth.json", "r") as f:
                auth = json.load(f)
                if auth['mode'] == "credentials":
                    return LinLogClient(
                        auth['email'],
                        auth['password'],
                        base_url, "credentials"
                    )
                else:
                    return LinLogClient(auth['token'], "", base_url)
        except FileNotFoundError:
            raise Exception(
                "Authentication credentials not provided, use "
                "'linlog authenticate'"
            )

    @staticmethod
    def init_from_credentials(email: str, password: str, base_url: str = None):
        return LinLogClient(email, password, base_url, "credentials")

    @staticmethod
    def init_from_token(token, base_url: str = None):
        return LinLogClient(token, "", base_url)

    def get_organisation(self):
        endpoint = "organisations"
        return self.controller.get_request(endpoint)

    def create_project(self, project_title: str, project_type: str):
        endpoint = "projects"
        return self.controller.post_request(endpoint, {
            "title": project_title,
            "type": project_type
        })

    def copy_project_taxonomy(self,
                              origin_project_id: str,
                              target_project_id: str):
        """
        :param origin_project_id: the project where the taxonomy will be
                                  stored in to
        :param target_project_id: the project where the taxonomy comes from
        """

        endpoint = f"projects/{origin_project_id}/import-taxonomy"
        return self.controller.post_request(endpoint, {
            "project_id": target_project_id
        })

    def get_project_workflows(self, id: str):
        endpoint = f"projects/{id}/workflows"
        return self.controller.get_request(endpoint)

    def get_workflow_templates(self):
        endpoint = "workflows/templates"
        return self.controller.get_request(endpoint)

    def set_project_workflow_template(self, project_id: str, template: str):
        endpoint = f"workflows/{project_id}/template"
        return self.controller.post_request(endpoint, {'template': template})

    def delete_project(self, id: str):
        endpoint = f"projects/{id}"
        return self.controller.delete_request(endpoint)

    def get_projects(self) -> List[Dict]:
        endpoint = "projects"
        return self.controller.get_request(endpoint)

    def get_project(self, id: str) -> Dict:
        """
        :param id: project ID
        """
        endpoint = f"projects/{id}"
        return self.controller.get_request(endpoint)

    def update_project(self, project_id: str, payload: Dict) -> Dict:
        """
        :param id: project ID
        """
        endpoint = f"projects/{project_id}"
        self.controller.put_request(
            endpoint,
            payload
        )

    def get_project_batches(self, id: str):
        endpoint = f"projects/{id}/batches"
        return self.controller.get_request(endpoint)

    def get_project_tasks(self, id: str, **kwargs) -> Paginator[Dict]:

        for key in kwargs:
            if key not in [
                'limit', 'offset',
                'status',
                'created_date',
                'created_date__gte',
                'created_date__lte',
                'created_date__gt',
                'created_date__lt',
                'complete',
                'rejected',
                'work_started'
            ]:
                raise Exception(f"Invalid kwarg key: {key}")

        endpoint = f"projects/{id}/tasks"
        response = self.controller.get_request(endpoint, params=kwargs)

        limit = kwargs.get('limit', 100)
        offset = kwargs.get('offset', 0)

        return Paginator[Dict](
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
                                   annotations=None,
                                   external_data=False,
                                   complete: bool = False,
                                   unique_id: str = None):
        endpoint = 'tasks/categorisation'

        self.controller.post_request(endpoint, {
            "project": project_id,
            "attachment": attachment,
            "attachment_type": attachment_type,
            "batch_name": batch_name if batch_name else "main (default)",
            "annotations": annotations if bool(annotations) else [],
            "type": 'categorisation',
            "complete": complete,
            "unique_id": unique_id,
            "external_data": external_data
        })

    def create_geospatial_task(
        self,
        project_id: str,
        attachment: str,
        zoom: 'MinMaxZoomDict',
        bounds: 'TaskBoundsDict',
        batch_name: str = None,
        annotations=None,
        external_data=False,
        complete: bool = False,
        unique_id: str = None
    ):
        endpoint = 'tasks/geo'

        self.controller.post_request(endpoint, {
            "project": project_id,
            "attachment": attachment,
            "attachment_type": "geospatial",
            "batch_name": batch_name if batch_name else "main (default)",
            "annotations": annotations if bool(annotations) else [],
            "type": "geospatial",
            "complete": complete,
            "unique_id": unique_id,
            "external_data": external_data,
            "zoom": zoom,
            "bounds": bounds
        })

    def create_image_task(
        self,
        project_id: str,
        attachment: str,
        attachment_type: str = "image",
        batch_name: str = None,
        annotations=None,
        external_data=False,
        complete: bool = False,
        unique_id: str = None
    ):
        endpoint = 'tasks/image'

        self.controller.post_request(endpoint, {
            "project": project_id,
            "attachment": attachment,
            "attachment_type": attachment_type,
            "batch_name": batch_name if batch_name else "main (default)",
            "annotations": annotations if bool(annotations) else [],
            "type": 'image',
            "complete": complete,
            "unique_id": unique_id,
            "external_data": external_data
        })

    def upload_image_task(
        self,
        project_id: str,
        image_path: str,
        task_type: str = "image",
        annotations=None,
        complete: bool = False,
        unique_id: str = None
    ):

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
                "unique_id": unique_id,
                "image": {}
            })
        }

        self.controller.post_request(endpoint,
                                     data=data,
                                     files=files,
                                     headers={})

    def create_project_label(self, project_id: str, payload: Dict) -> Dict:
        """
        :param id: project ID
        """
        endpoint = f"projects/{project_id}/create-label"
        return self.controller.post_request(
            endpoint,
            payload
        )

    def update_project_label(self, label_object_id: str, payload: Dict):
        endpoint = f"project-labels/{label_object_id}"
        return self.controller.put_request(
            endpoint,
            payload
        )

    def delete_project_label(self, label_object_id: str):
        endpoint = f"project-labels/{label_object_id}"
        return self.controller.delete_request(endpoint)

    def update_task(self, task_id: str, payload: Dict):
        endpoint = f"tasks/{task_id}"
        return self.controller.put_request(
            endpoint,
            {"task": payload}
        )

    def get_datasets(self):
        endpoint = "datasets"
        return self.controller.get_request(endpoint)['results']

    def get_dataset(self, id: str):
        endpoint = f"datasets/{id}"
        return self.controller.get_request(endpoint)

    def get_dataset_tasks(self, id: str, **kwargs):
        for key in kwargs:
            if key not in [
                'limit',
                'offset',
                'created_date',
                'created_date__gte',
                'created_date__lte',
                'created_date__gt',
                'created_date__lt',
                'exclude_annotations'
            ]:
                raise Exception(f"Invalid kwarg key: {key}")

        limit = min(kwargs.get('limit', 50), 200)
        offset = kwargs.get('offset', 0)

        endpoint = f"search/tasks?dataset={id}&offset={offset}&limit={limit}"
        response = self.controller.post_request(
            endpoint,
            data={
                'exclude_annotations': kwargs.get('exclude_annotations', True)
            })

        return Paginator[str](
            response["results"],
            response["count"],
            limit,
            offset,
            response["previous"],
            response["next"]
        )

    def delete_tasks(self, task_ids: List[str]):
        endpoint = "tasks"
        return self.controller.post_request(endpoint, {"task_ids": task_ids})

    def create_model_run(self,
                         dataset_id: str,
                         model_version_id: str,
                         task_id: str,
                         annotation,
                         confidence_score: float = None):

        if bool(confidence_score):
            assert 0 <= confidence_score <= 1, \
                "Confidence score must be a value between 0 and 1"

        endpoint = "datasets/model-run"
        return self.controller.post_request(endpoint, {
            "dataset": dataset_id,
            "model_version": model_version_id,
            "task": task_id,
            "annotation": annotation,
            "confidence_score": confidence_score
        })
