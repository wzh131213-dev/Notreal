import unittest
import os
import shutil
import tempfile
from io import StringIO
from unittest.mock import patch

from video_generator.cli import main


class TestCLI(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_cli_list_providers(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            code = main(["list-providers"])
            self.assertEqual(code, 0)
            self.assertIn("non-production", fake_out.getvalue())

    def test_cli_generate_json(self):
        out_path = os.path.join(self.temp_dir, "cli_test.mp4")
        with patch('sys.stdout', new=StringIO()) as fake_out:
            code = main(["generate", "--prompt", "A rocket launching", "--output", out_path, "--provider", "local-mock", "--json"])
            self.assertEqual(code, 0)
            self.assertIn('"status": "completed"', fake_out.getvalue())
            self.assertTrue(os.path.exists(out_path))


if __name__ == "__main__":
    unittest.main()
