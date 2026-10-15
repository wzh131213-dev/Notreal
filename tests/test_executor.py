import unittest
import os
import shutil
from video_generator.executor import CodeVideoExecutor

class TestCodeVideoExecutor(unittest.TestCase):

    def setUp(self):
        self.test_output_dir = "tests/test_videos"
        self.executor = CodeVideoExecutor(output_dir=self.test_output_dir)

    def tearDown(self):
        if os.path.exists(self.test_output_dir):
            shutil.rmtree(self.test_output_dir)

    def test_parse_dimensions(self):
        w169, h169 = self.executor.parse_dimensions("16:9", "720p")
        self.assertEqual(w169, 1280)
        self.assertEqual(h169, 720)

        w916, h916 = self.executor.parse_dimensions("9:16", "720p")
        self.assertEqual(w916, 406) # Even dimension adjustment
        self.assertEqual(h916, 720)

        w11, h11 = self.executor.parse_dimensions("1:1", "720p")
        self.assertEqual(w11, 720)
        self.assertEqual(h11, 720)

    def test_generate_and_execute(self):
        result = self.executor.generate_and_execute(
            prompt="Test abstract video rendering",
            aspect_ratio="16:9",
            duration=1.0,
            fps=10,
            resolution="480p"
        )
        self.assertEqual(result["status"], "completed")
        self.assertIsNotNone(result["video_url"])
        self.assertTrue(os.path.exists(os.path.join(self.test_output_dir, os.path.basename(result["video_url"]))))

if __name__ == '__main__':
    unittest.main()
