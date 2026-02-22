import unittest
import os
import json
import shutil
from core.plugin_engine import BasePlugin, PluginLoader

class MockPlugin(BasePlugin):
    def register_arguments(self, parser):
        parser.add_parser('mock')

    def execute(self, args):
        return args.command == 'mock'

class TestPluginEngine(unittest.TestCase):
    def setUp(self):
        self.modules_dir = "test_modules"
        os.makedirs(self.modules_dir, exist_ok=True)
        # Create an __init__.py for the test modules directory
        with open(os.path.join(self.modules_dir, "__init__.py"), "w") as f:
            pass

        self.modules_json = "test_modules.json"

    def tearDown(self):
        if os.path.exists(self.modules_dir):
            shutil.rmtree(self.modules_dir)
        if os.path.exists(self.modules_json):
            os.remove(self.modules_json)

    def test_plugin_loader_no_file(self):
        loader = PluginLoader(modules_json_path="non_existent.json")
        plugins = loader.load_plugins()
        self.assertEqual(len(plugins), 0)

    def test_plugin_loader_empty_modules(self):
        with open(self.modules_json, "w") as f:
            json.dump({"modules": []}, f)

        loader = PluginLoader(modules_json_path=self.modules_json)
        plugins = loader.load_plugins()
        self.assertEqual(len(plugins), 0)

    def test_plugin_loader_active_module(self):
        # Create a mock module file
        module_content = """
from core.plugin_engine import BasePlugin

class MyTestPlugin(BasePlugin):
    def register_arguments(self, parser):
        pass
    def execute(self, args):
        return True
"""
        with open(os.path.join(self.modules_dir, "my_mod.py"), "w") as f:
            f.write(module_content)

        with open(self.modules_json, "w") as f:
            json.dump({"modules": [{"name": "my_mod", "active": True}]}, f)

        loader = PluginLoader(modules_json_path=self.modules_json, modules_dir=self.modules_dir)
        plugins = loader.load_plugins()

        self.assertEqual(len(plugins), 1)
        self.assertEqual(plugins[0].__class__.__name__, "MyTestPlugin")

    def test_plugin_loader_inactive_module(self):
        # Create a mock module file
        module_content = "class MyTestPlugin: pass"
        with open(os.path.join(self.modules_dir, "my_mod_inactive.py"), "w") as f:
            f.write(module_content)

        with open(self.modules_json, "w") as f:
            json.dump({"modules": [{"name": "my_mod_inactive", "active": False}]}, f)

        loader = PluginLoader(modules_json_path=self.modules_json, modules_dir=self.modules_dir)
        plugins = loader.load_plugins()

        self.assertEqual(len(plugins), 0)

if __name__ == '__main__':
    unittest.main()
