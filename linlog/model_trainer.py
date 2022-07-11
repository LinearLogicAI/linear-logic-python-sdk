from typing import Dict, Union
from linlog import LinLogClient


class ModelTrainer:

    client: LinLogClient
    model_id: str = None
    model_version_id: str = None
    staged_data = {}
    step = 0
    did_init = False

    def __init__(self, client: LinLogClient):
        self.client = client

    def init(self,
             model_id: str,
             version_name: str,
             config: Dict[str, Union[str, int, float]] = None):

        assert version_name is not None, AssertionError("version_name cannot be none")

        endpoint = f"models/{model_id}/init"
        response = self.client.controller.post_request(
            endpoint,
            {
                "version_name": version_name,
                "config": config if bool(config) else {}
            }
        )

        self.model_id = model_id
        self.did_init = True
        self.model_version_id = response['ai_model_version']['id']
        return response

    def _assert_init(self):
        assert self.did_init, AssertionError("You must call the .init of the ModelTrainer before using this function.")

    def log(self, data, step=None, commit=True):
        self._assert_init()

        if not commit:
            self.staged_data = {**data, **self.staged_data}
            return

        endpoint = f"models/{self.model_version_id}/log"
        response = self.client.controller.post_request(
            endpoint,
            {
                **data,
                **self.staged_data,
                "step": step if step else self.step
            }
        )
        self.step += 1
        return response

    def finish(self):
        self._assert_init()

        endpoint = f"models/{self.model_version_id}/finish"
        return self.client.controller.post_request(
            endpoint,
            {
                "step": self.step
            }
        )


