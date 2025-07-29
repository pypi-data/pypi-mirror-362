import odoo
import json
import requests

from odoo.addons.base_rest.tests.common import BaseRestCase

HOST = "127.0.0.1"
PORT = odoo.tools.config["http_port"]


class APICommonBaseRestCase(BaseRestCase):
    def setUp(self):
        super().setUp()
        self.api_key_test = self.env.ref("api_common_base.auth_api_key_admin_demo")
        self.session = requests.Session()

    def _add_api_key(self, headers):
        key_dict = {"API-KEY": self.api_key_test.key}
        if headers:
            headers.update(key_dict)
        else:
            headers = key_dict
        return headers

    def http_get(self, url, headers=None, params=None):
        headers = self._add_api_key(headers)
        if url.startswith("/"):
            url = "http://{}:{}{}".format(HOST, PORT, url)
        return self.session.get(url, headers=headers, params=params)

    def http_get_content(self, url, headers=None, params=None):
        response = self.http_get(url, headers=headers, params=params)
        self.assertEquals(response.status_code, 200)
        content = response.content.decode("utf-8")
        return json.loads(content)

    def http_post(self, url, data, headers=None):
        headers = self._add_api_key(headers)
        if url.startswith("/"):
            url = "http://{}:{}{}".format(HOST, PORT, url)
        return self.session.post(url, json=data, headers=headers)

    def http_public_get(self, url, headers=None, params=None):
        if url.startswith("/"):
            url = "http://{}:{}{}".format(HOST, PORT, url)
        return self.session.get(url, headers=headers, params=params)

    def http_public_post(self, url, data, headers=None):
        if url.startswith("/"):
            url = "http://{}:{}{}".format(HOST, PORT, url)
        return self.session.post(url, json=data, headers=headers)
