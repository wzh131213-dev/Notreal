import unittest
from video_generator.ai_coder import AICodeGenerator

class TestAICodeGenerator(unittest.TestCase):

    def setUp(self):
        self.generator = AICodeGenerator()

    def test_synthesize_code_structure(self):
        code = self.generator.synthesize_code(
            prompt="Cyberpunk city with glowing neon rain",
            width=640,
            height=360,
            duration=2.0,
            fps=15
        )
        self.assertIn("def render_video(", code)
        self.assertIn("Cyberpunk city with glowing neon rain", code)
        self.assertIn("output_path", code)

    def test_different_prompt_themes(self):
        prompts = [
            "Cosmic galaxy nebula",
            "Ocean sunset waves",
            "Energy portal magic sparks",
            "3D morphing sphere geometry"
        ]
        for prompt in prompts:
            code = self.generator.synthesize_code(prompt=prompt, width=320, height=180, duration=1.0, fps=10)
            self.assertIsInstance(code, str)
            self.assertTrue(len(code) > 100)

if __name__ == '__main__':
    unittest.main()
