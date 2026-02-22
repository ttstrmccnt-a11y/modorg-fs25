import unittest
import os
import json
from core.config_manager import ConfigManager

class TestConfigManager(unittest.TestCase):
    def setUp(self):
        self.test_config = "test_config.json"
        if os.path.exists(self.test_config):
            os.remove(self.test_config)
        self.cm = ConfigManager(self.test_config)

    def tearDown(self):
        if os.path.exists(self.test_config):
            os.remove(self.test_config)

    def test_default_config(self):
        self.assertEqual(self.cm.get_global("language"), "en")

    def test_set_get_global(self):
        self.cm.set_global("test_key", "test_value")
        self.assertEqual(self.cm.get_global("test_key"), "test_value")

        # Verify it was saved
        with open(self.test_config, 'r') as f:
            data = json.load(f)
            self.assertEqual(data["global"]["test_key"], "test_value")

    def test_module_config(self):
        module_data = {"key": "value"}
        self.cm.set_module_config("test_module", module_data)
        self.assertEqual(self.cm.get_module_config("test_module"), module_data)

if __name__ == "__main__":
    unittest.main()
