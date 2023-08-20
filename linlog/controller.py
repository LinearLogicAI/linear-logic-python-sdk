import requests
import copy
from typing import Tuple
from linlog.constants import BASE_URL
from requests.adapters import Response

from linlog.exceptions import NotFound

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

        res = self._http_request(
            method, url, headers, auth, params, body, files, data
        )

        if res.status_code not in [200, 201, 204]:
            if res.status_code == 404:
                raise NotFound(res.text)

            raise Exception(res.text, res.status_code)

        return res.json() if len(res.text) > 1 else None

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
        s = requests.Session()
        s.auth = auth

        params = params or {}
        body = body or None

        import json
        return requests.request(
            method=method,
            url=url,
            params=params,
            json=body,
            files=files,
            data=json.dumps(data) if not files else data,
            headers=headers,
            auth=auth
        )

    def get_request(self, endpoint, params=None):

        return self._perform_api_request(
            "GET",
            endpoint,
            headers=self.headers,
            auth=self.auth,
            params=params
        )

    def post_request(
        self,
        endpoint,
        data,
        params=None,
        files=None,
        headers=None
    ):
        if not headers:
            headers = {}

        _headers = copy.deepcopy(self.headers)
        for key in headers.keys():
            _headers[key] = headers[key]

        if bool(files) and 'Content-Type' in _headers.keys():
            del _headers['Content-Type']

        return self._perform_api_request(
            "POST",
            endpoint,
            headers=_headers,
            auth=self.auth,
            params=params,
            data=data,
            files=files
        )

    def put_request(
        self,
        endpoint,
        data,
        params=None,
        files=None,
        headers=None
    ):

        if not headers:
            headers = {}

        _headers = copy.deepcopy(self.headers)
        for key in headers.keys():
            _headers[key] = headers[key]

        if bool(files) and 'Content-Type' in _headers.keys():
            del _headers['Content-Type']

        return self._perform_api_request(
            "PATCH",
            endpoint,
            headers=_headers,
            auth=self.auth,
            params=params,
            data=data,
            files=files
        )

    def delete_request(self, endpoint, params=None):
        return self._perform_api_request(
            "DELETE",
            endpoint,
            headers=self.headers,
            auth=self.auth,
            params=params,
        )
