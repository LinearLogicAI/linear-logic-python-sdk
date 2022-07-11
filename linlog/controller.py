import requests
from typing import Tuple
from linlog.constants import BASE_URL
from requests.adapters import Response, Retry, HTTPAdapter

HTTP_TOTAL_RETRIES = 3
HTTP_RETRY_BACKOFF_FACTOR = 2
HTTP_STATUS_FORCE_LIST = [408, 429] + list(range(500, 531))
HTTP_RETRY_ALLOWED_METHODS = frozenset({"GET", "POST", "DELETE"})


class Controller:

    api_key = None
    base_url = None
    auth = None
    headers = {}
    headers_multipart_form_data = {}

    def __init__(self,
                 api_key: Tuple[str, str],
                 user_agent_extension=None,
                 base_url=BASE_URL):

        if api_key == "" or not bool(api_key):
            raise Exception("Please provide a valid API Key.")

        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Content-Type": "application/json",
        }

        if api_key[1] == "":
            self.auth = None
            self.headers["Authorization"] = f"Token {api_key[0]}"
        else:
            self.auth = self.api_key

        self.headers_multipart_form_data = {}

    def _perform_api_request(
            self,
            method,
            endpoint,
            headers=None,
            auth=None,
            params=None,
            body=None,
            files=None,
            data=None,
    ):
        """Generic HTTP request method with error handling."""
        url = f"{self.base_url}/{endpoint}"
        res = self._http_request(method, url, headers, auth, params, body, files, data)

        if not res.status_code == 200:
            raise Exception(res.text, res.status_code)

        return res.json()

    @staticmethod
    def _http_request(
            method,
            url,
            headers=None,
            auth=None,
            params=None,
            body=None,
            files=None,
            data=None,
    ) -> Response:

        sess = requests.Session()
        retry_strategy = Retry(
            total=HTTP_TOTAL_RETRIES,
            backoff_factor=HTTP_RETRY_BACKOFF_FACTOR,
            status_forcelist=HTTP_STATUS_FORCE_LIST,
            allowed_methods=HTTP_RETRY_ALLOWED_METHODS,
            raise_on_status=False,
        )

        s = requests.Session()

        sess.mount('http://', HTTPAdapter(max_retries=retry_strategy))
        sess.mount('https://', HTTPAdapter(max_retries=retry_strategy))

        params = params or {}
        body = body or None

        res = s.request(
            method=method,
            url=url,
            headers=headers,
            auth=auth,
            params=params,
            json=body,
            files=files,
            data=data,
        )

        return res

    def get_request(self, endpoint, params=None):
        return self._perform_api_request(
            "GET",
            endpoint,
            headers=self.headers,
            auth=self.auth,
            params=params
        )

    def post_request(self, endpoint, data, params=None):
        return self._perform_api_request(
            "POST",
            endpoint,
            headers=self.headers,
            auth=self.auth,
            params=params,
            body=data
        )
