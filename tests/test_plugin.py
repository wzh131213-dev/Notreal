import json
import os
import unittest

class TestPluginAndSkillStructure(unittest.TestCase):

    def test_plugin_json_files_exist_and_valid(self):
        plugin_paths = [
            ".claude-plugin/plugin.json",
            ".codex-plugin/plugin.json",
            ".agent-plugin/plugin.json",
        ]
        for path in plugin_paths:
            self.assertTrue(os.path.exists(path), f"Missing plugin file: {path}")
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.assertIn("name", data)
                self.assertIn("version", data)
                self.assertIn("description", data)

    def test_skill_files_parity(self):
        skill_paths = [
            "skills/token-saver/SKILL.md",
            "SKILL.md",
            "SKILLS/token-saver.md",
        ]
        contents = []
        for path in skill_paths:
            self.assertTrue(os.path.exists(path), f"Missing skill file: {path}")
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                self.assertTrue(content.startswith("---"), f"{path} missing YAML frontmatter start")
                contents.append(content)

        # Check content parity across all copies
        for content in contents[1:]:
            self.assertEqual(contents[0], content)

if __name__ == "__main__":
    unittest.main()
