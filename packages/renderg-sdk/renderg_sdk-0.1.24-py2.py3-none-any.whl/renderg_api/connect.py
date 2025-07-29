import copy
import json

import requests
from tenacity import retry
from tenacity import stop_after_attempt, wait_random

from renderg_api.constants import HEADERS
from renderg_api.exception import RenderGAPIError
from renderg_api.urls import assemble_api_url, ApiUrl


class Connect(object):

    def __init__(self, auth_key, protocol, domain, cluster_id, header=None):
        self.cluster_id = cluster_id
        self.urls = ApiUrl

        self._auth_key = auth_key
        self.domain = domain
        self._protocol = protocol
        if header:
            HEADERS.update(header)
        self._headers = HEADERS
        self._headers["Authorization"] = auth_key

        self._session = requests.Session()

    @property
    def headers(self):
        return self._headers

    @retry(reraise=True, stop=stop_after_attempt(5),
           wait=wait_random(min=1, max=2))
    def post(self, api_url, data=None, params=None, validator=True):
        if not data:
            data = {}

        if validator:
            # todo data validator
            pass

        request_url = assemble_api_url(self.domain, api_url, self._protocol)
        data = json.dumps(data)

        response = self._session.post(request_url, data=data, headers=self._headers, params=params)
        response_json = response.json()

        if not response.ok:
            response_code = response_json.get('error_code')
            raise RenderGAPIError(response_code, response_json.get("msg", ""), response.url)

        return response_json

    @retry(reraise=True, stop=stop_after_attempt(5),
           wait=wait_random(min=1, max=2))
    def get(self, api_url, data=None, params=None, validator=True):
        if not data:
            data = {}

        if validator:
            # todo data validator
            pass

        request_url = assemble_api_url(self.domain, api_url, self._protocol)
        data = json.dumps(data)

        response = self._session.get(request_url, data=data, headers=self._headers, params=params)
        response_json = response.json()

        if not response.ok:
            response_code = response_json.get('error_code')
            raise RenderGAPIError(response_code, response_json.get("msg", ""), response.url)

        return response_json
