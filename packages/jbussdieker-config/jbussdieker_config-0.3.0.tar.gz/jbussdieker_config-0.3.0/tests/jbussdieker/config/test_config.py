import os
import unittest
import tempfile
import json
from unittest.mock import patch

from jbussdieker.config.config import Config


class TestConfig(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.config_path = os.path.join(self.tmpdir.name, "config.json")
        os.environ["JBUSSDIEKER_CONFIG"] = self.config_path

    def tearDown(self):
        self.tmpdir.cleanup()
        os.environ.pop("JBUSSDIEKER_CONFIG", None)

    def test_with_no_existing_config(self):
        config = Config.load()
        self.assertIsInstance(config, Config)

    def test_save_creates_file(self):
        config = Config(log_level="TRACE")
        config.save()
        self.assertTrue(os.path.exists(self.config_path))
        with open(self.config_path) as f:
            data = json.load(f)
        self.assertEqual(data["log_level"], "TRACE")

    def test_load_with_existing_file(self):
        data = {"log_level": "INFO", "custom_settings": {"customkey": "baz"}}
        with open(self.config_path, "w") as f:
            json.dump(data, f)
        config = Config.load()
        self.assertEqual(config.log_level, "INFO")
        self.assertIn("customkey", config.custom_settings)
        self.assertEqual(config.custom_settings["customkey"], "baz")

    def test_new_config_fields_defaults(self):
        config = Config.load()
        self.assertEqual(config.user_name, "Joshua B. Bussdieker")
        self.assertEqual(config.user_email, "jbussdieker@gmail.com")
        self.assertEqual(config.github_org, "jbussdieker")
        self.assertTrue(config.private)

    def test_new_config_fields_custom_values(self):
        config = Config(
            user_name="Test User",
            user_email="test@example.com",
            github_org="testorg",
            private=False,
        )
        self.assertEqual(config.user_name, "Test User")
        self.assertEqual(config.user_email, "test@example.com")
        self.assertEqual(config.github_org, "testorg")
        self.assertFalse(config.private)

    def test_load_with_new_config_fields(self):
        data = {
            "user_name": "Custom User",
            "user_email": "custom@example.com",
            "github_org": "customorg",
            "private": False,
            "log_level": "DEBUG",
        }
        with open(self.config_path, "w") as f:
            json.dump(data, f)
        config = Config.load()
        self.assertEqual(config.user_name, "Custom User")
        self.assertEqual(config.user_email, "custom@example.com")
        self.assertEqual(config.github_org, "customorg")
        self.assertFalse(config.private)
        self.assertEqual(config.log_level, "DEBUG")

    def test_asdict_includes_new_fields(self):
        config = Config(
            user_name="Test User",
            user_email="test@example.com",
            github_org="testorg",
            private=False,
            custom_settings={"test": "value"},
        )
        data = config.asdict()
        self.assertEqual(data["user_name"], "Test User")
        self.assertEqual(data["user_email"], "test@example.com")
        self.assertEqual(data["github_org"], "testorg")
        self.assertFalse(data["private"])
        self.assertEqual(data["custom_settings"]["test"], "value")


if __name__ == "__main__":
    unittest.main()
