import os
import unittest
from linlog import LinLogClient


test_api_key = os.environ["LINEAR_LOGIC_TEST_KEY"]
test_project_id = os.environ["TEST_PROJECT_ID"]


class TestClient(unittest.TestCase):

    client = LinLogClient.init_from_credentials("miguel@linearlogic.ai", test_api_key)

    def test_list_projects(self):
        self.client.get_projects()

    def test_can_find_project_by_id(self):
        self.client.get_project(test_project_id)

    def test_list_project_batches(self):
        self.client.get_project_batches(test_project_id)

    def test_list_project_tasks(self):
        self.client.get_project_tasks(test_project_id)


