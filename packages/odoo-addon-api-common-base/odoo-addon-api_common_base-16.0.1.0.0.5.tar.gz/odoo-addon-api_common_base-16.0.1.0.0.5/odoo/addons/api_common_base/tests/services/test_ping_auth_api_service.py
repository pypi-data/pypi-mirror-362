import json
from ..common_service import BaseRestCaseAdmin


class TestPingAuthAPiService(BaseRestCaseAdmin):
    def test_ping_auth_search(self):
        response = self.http_get("/api/ping/search")

        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content.decode("utf-8"))
        self.assertIn("message", content)

    def test_ping_auth_search_content(self):
        response = self.http_get_content("/api/ping/search")

        self.assertEqual(response["message"], "Called search on auth ping API")

    def test_ping_auth_create(self):
        my_id = "1234"
        response = self.http_post("/api/ping/create", data={"id": my_id})

        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content.decode("utf-8"))
        self.assertIn("message", content)
        self.assertEqual(
            content["message"], "Called auth create with id {}".format(my_id)
        )
