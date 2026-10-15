import unittest
import os
import shutil
import tempfile

from video_generator import VideoGenerator, GenerationConfig, NonProductionProvider, LocalMockProvider, HuggingFaceInferenceProvider
from video_generator.utils import validate_dimensions, sanitize_prompt


class TestVideoGenerator(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_providers_properties(self):
        non_prod = NonProductionProvider()
        self.assertEqual(non_prod.name, "non-production-ai")
        self.assertFalse(non_prod.is_production)

        mock_prov = LocalMockProvider()
        self.assertEqual(mock_prov.name, "local-mock")
        self.assertFalse(mock_prov.is_production)

        hf_prov = HuggingFaceInferenceProvider()
        self.assertEqual(hf_prov.name, "huggingface-inference")
        self.assertFalse(hf_prov.is_production)

    def test_generator_non_production(self):
        gen = VideoGenerator("non-production")
        output_file = os.path.join(self.temp_dir, "test_out.mp4")
        job = gen.generate_from_prompt("A futuristic city at sunset", output_path=output_file)

        self.assertEqual(job.status, "completed")
        self.assertTrue(os.path.exists(output_file))
        self.assertEqual(job.provider, "non-production-ai")

    def test_generator_local_mock(self):
        gen = VideoGenerator("local-mock")
        output_file = os.path.join(self.temp_dir, "mock_out.mp4")
        config = GenerationConfig(prompt="A sleeping cat", output_path=output_file, duration=2)
        job = gen.generate(config)

        self.assertEqual(job.status, "completed")
        self.assertTrue(os.path.exists(output_file))
        self.assertEqual(job.provider, "local-mock")

    def test_generator_empty_prompt_raises(self):
        gen = VideoGenerator("non-production")
        with self.assertRaises(ValueError):
            gen.generate_from_prompt("   ")

    def test_invalid_provider_raises(self):
        with self.assertRaises(ValueError):
            VideoGenerator("non-existent-provider")

    def test_utils(self):
        w, h = validate_dimensions(319, 239)
        self.assertEqual(w, 320)
        self.assertEqual(h, 240)

        cleaned = sanitize_prompt("  hello video world  ")
        self.assertEqual(cleaned, "hello video world")


if __name__ == "__main__":
    unittest.main()
