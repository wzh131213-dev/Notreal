import unittest
import os
import re
import zipfile

class TestTokenOptimizationSkill(unittest.TestCase):

    def setUp(self):
        self.root_skill = "SKILL.md"
        self.skills_dir_skill = "SKILLS/token-optimization.md"
        self.pkg_dir_skill = "skills/token-optimization/SKILL.md"
        self.zip_file = "token-optimization.zip"
        self.skill_file = "token-optimization.skill"

    def test_skill_files_exist(self):
        self.assertTrue(os.path.exists(self.root_skill), f"Missing {self.root_skill}")
        self.assertTrue(os.path.exists(self.skills_dir_skill), f"Missing {self.skills_dir_skill}")
        self.assertTrue(os.path.exists(self.pkg_dir_skill), f"Missing {self.pkg_dir_skill}")

    def test_yaml_frontmatter(self):
        for path in [self.root_skill, self.skills_dir_skill, self.pkg_dir_skill]:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()

            match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
            self.assertIsNotNone(match, f"File {path} missing '---' YAML frontmatter block.")

            yaml_block = match.group(1)
            keys = {}
            for line in yaml_block.splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    keys[k.strip()] = v.strip()

            self.assertIn("name", keys, f"Missing 'name' in YAML frontmatter for {path}")
            self.assertIn("description", keys, f"Missing 'description' in YAML frontmatter for {path}")
            self.assertEqual(keys["name"], "token-optimization")
            self.assertTrue(len(keys["description"]) > 10)

    def test_skills_synchronized(self):
        with open(self.root_skill, "r", encoding="utf-8") as f1:
            c1 = f1.read()
        with open(self.skills_dir_skill, "r", encoding="utf-8") as f2:
            c2 = f2.read()
        with open(self.pkg_dir_skill, "r", encoding="utf-8") as f3:
            c3 = f3.read()

        self.assertEqual(c1, c2, "SKILL.md and SKILLS/token-optimization.md are not synchronized.")
        self.assertEqual(c1, c3, "SKILL.md and skills/token-optimization/SKILL.md are not synchronized.")

    def test_packages_contain_skill_md_and_no_nested_zips(self):
        for pkg_path in [self.zip_file, self.skill_file]:
            self.assertTrue(os.path.exists(pkg_path), f"Package file {pkg_path} does not exist.")
            with zipfile.ZipFile(pkg_path, "r") as zf:
                namelist = zf.namelist()
                self.assertIn("SKILL.md", namelist, f"{pkg_path} must contain SKILL.md")
                for name in namelist:
                    self.assertFalse(name.endswith(".zip"), f"Package {pkg_path} must not contain nested zip archive: {name}")
                    self.assertFalse(name.endswith(".skill"), f"Package {pkg_path} must not contain nested skill archive: {name}")

    def test_token_optimization_content_coverage(self):
        with open(self.root_skill, "r", encoding="utf-8") as f:
            content = f.read()

        keywords = [
            "Token",
            "Prompt",
            "Context",
            "Diff",
            "JSON",
            "精简"
        ]
        for kw in keywords:
            self.assertIn(kw, content, f"Skill content missing keyword: {kw}")

if __name__ == '__main__':
    unittest.main()
