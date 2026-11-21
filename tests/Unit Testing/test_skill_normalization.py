import unittest

from ml.skills.text_processing import clean_and_normalize


class SkillNormalizationTests(unittest.TestCase):
    def test_uses_alias_table_to_normalize_variants(self):
        normalized = clean_and_normalize("I used reactjs and next.js for a dashboard")
        self.assertIn("react", normalized)
        self.assertIn("nextjs", normalized)
        self.assertNotIn("reactjs", normalized)
        self.assertNotIn("next.js", normalized)


if __name__ == "__main__":
    unittest.main()
