import json
from ..common_service import BaseRestCaseAdmin


class TestPublicPing(BaseRestCaseAdmin):
    def test_ping_public_search(self):
        response = self.http_public_get("/public-api/ping/search")

        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content.decode("utf-8"))
        self.assertIn("message", content)

    def test_ping_public_create(self):
        my_id = "1234"
        response = self.http_public_post("/public-api/ping/create", data={"id": my_id})

        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content.decode("utf-8"))
        self.assertIn("message", content)
        self.assertEqual(
            content["message"], "Called public create with id {}".format(my_id)
        )
