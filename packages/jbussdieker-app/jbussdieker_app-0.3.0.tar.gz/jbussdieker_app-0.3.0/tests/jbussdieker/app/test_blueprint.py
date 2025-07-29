import unittest
from jbussdieker.app.factory import create_app


class TestBlueprint(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_main_route(self):
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("jbussdieker app v", resp.get_data(as_text=True))

    def test_healthz_route(self):
        resp = self.client.get("/healthz")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_data(as_text=True), "OK")


if __name__ == "__main__":
    unittest.main()
