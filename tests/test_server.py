import unittest
from fastapi.testclient import TestClient
from backend.server import app

class TestServerAPI(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_get_history(self):
        response = self.client.get("/api/history")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_generate_video_api(self):
        payload = {
            "prompt": "Test cosmic explosion",
            "aspect_ratio": "16:9",
            "duration": 1.0,
            "fps": 10,
            "resolution": "480p"
        }
        response = self.client.post("/api/generate", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "completed")
        self.assertIn("video_url", data)

        # Test get video code endpoint
        video_id = data["id"]
        code_resp = self.client.get(f"/api/code/{video_id}")
        self.assertEqual(code_resp.status_code, 200)
        self.assertEqual(code_resp.json()["id"], video_id)

if __name__ == '__main__':
    unittest.main()
