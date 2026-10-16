import os
import sys
import tempfile
import unittest
from unittest.mock import MagicMock, patch

from audio_to_lrc import AudioToLRCConverter, main


class TestAudioToLRCConverter(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_clean_lrc_output(self):
        raw_lrc = "```lrc\n[00:12.34] Hello World\n[00:15.67] Second Line\n```"
        cleaned = AudioToLRCConverter._clean_lrc_output(raw_lrc)
        expected = "[00:12.34] Hello World\n[00:15.67] Second Line"
        self.assertEqual(cleaned, expected)

    @patch("audio_to_lrc.genai.Client")
    def test_convert_file_success(self, mock_client_cls):
        mock_client = MagicMock()
        mock_client_cls.return_value = mock_client
        mock_response = MagicMock()
        mock_response.text = "[00:01.00] Test line 1\n[00:05.00] Test line 2"
        mock_client.models.generate_content.return_value = mock_response

        converter = AudioToLRCConverter(api_key="fake-key", model="gemini-2.5-flash")

        # Create a dummy mp3 file
        input_mp3 = os.path.join(self.temp_dir.name, "test.mp3")
        with open(input_mp3, "wb") as f:
            f.write(b"dummy mp3 data")

        output_lrc = os.path.join(self.temp_dir.name, "output.lrc")
        result = converter.convert_file(input_mp3, output_lrc)

        self.assertEqual(result, "[00:01.00] Test line 1\n[00:05.00] Test line 2")
        self.assertTrue(os.path.exists(output_lrc))
        with open(output_lrc, "r", encoding="utf-8") as f:
            saved_content = f.read()
        self.assertEqual(saved_content, "[00:01.00] Test line 1\n[00:05.00] Test line 2")

    @patch("audio_to_lrc.genai.Client")
    def test_convert_file_default_output_name(self, mock_client_cls):
        mock_client = MagicMock()
        mock_client_cls.return_value = mock_client
        mock_response = MagicMock()
        mock_response.text = "[00:02.00] Default output name test"
        mock_client.models.generate_content.return_value = mock_response

        converter = AudioToLRCConverter(api_key="fake-key")

        input_mp3 = os.path.join(self.temp_dir.name, "song.mp3")
        expected_lrc = os.path.join(self.temp_dir.name, "song.lrc")
        with open(input_mp3, "wb") as f:
            f.write(b"dummy mp3 data")

        result = converter.convert_file(input_mp3)

        self.assertTrue(os.path.exists(expected_lrc))
        self.assertEqual(result, "[00:02.00] Default output name test")

    def test_convert_file_file_not_found(self):
        converter = AudioToLRCConverter(api_key="fake-key")
        non_existent_file = os.path.join(self.temp_dir.name, "missing.mp3")
        with self.assertRaises(FileNotFoundError):
            converter.convert_file(non_existent_file)

    @patch("audio_to_lrc.AudioToLRCConverter")
    def test_cli_main(self, mock_converter_cls):
        mock_instance = MagicMock()
        mock_converter_cls.return_value = mock_instance
        mock_instance.convert_file.return_value = "[00:00.00] CLI test"

        input_mp3 = os.path.join(self.temp_dir.name, "cli_test.mp3")
        with open(input_mp3, "wb") as f:
            f.write(b"dummy data")

        test_args = ["audio_to_lrc.py", "-i", input_mp3, "-k", "test_key"]
        with patch.object(sys, "argv", test_args):
            main()

        mock_converter_cls.assert_called_once_with(api_key="test_key", model="gemini-2.5-flash")
        mock_instance.convert_file.assert_called_once_with(input_mp3, None)


if __name__ == "__main__":
    unittest.main()
