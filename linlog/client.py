from linlog import constants
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

    def create_task(self,
                    task_type: constants.TaskType, ):
        pass

    def get_projects(self):
        endpoint = "projects"
        return self.controller.get_request(endpoint)

    def get_project(self, id: str):
        endpoint = f"projects/{id}"
        return self.controller.get_request(endpoint)

    def get_project_batches(self, id: str):
        endpoint = f"projects/{id}/batches"
        return self.controller.get_request(endpoint)

    def get_project_tasks(self, id: str, kwargs=None):
        if kwargs is None:
            kwargs = {}

        for key in kwargs.keys():
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

    def get_datasets(self):
        endpoint = "datasets"
        return self.controller.get_request(endpoint)

    def get_dataset(self, id: str):
        endpoint = f"datasets/{id}"
        return self.controller.get_request(endpoint)

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
