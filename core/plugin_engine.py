import json
import os
import importlib
import inspect
from abc import ABC, abstractmethod

class BasePlugin(ABC):
    """
    Abstract base class for all modules/plugins.
    """
    @abstractmethod
    def register_arguments(self, parser):
        """
        Allows the plugin to register its own CLI arguments.
        """
        pass

    @abstractmethod
    def execute(self, args):
        """
        Executes the plugin's main logic based on parsed arguments.
        """
        pass

class PluginLoader:
    """
    Handles discovery and dynamic loading of plugins from the modules directory.
    """
    def __init__(self, modules_json_path="modules.json", modules_dir="modules"):
        self.modules_json_path = modules_json_path
        self.modules_dir = modules_dir
        self.plugins = []

    def load_plugins(self):
        """
        Reads modules.json and imports active plugins.
        """
        if not os.path.exists(self.modules_json_path):
            return []

        try:
            with open(self.modules_json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (json.JSONDecodeError, IOError):
            return []

        loaded_plugins = []
        for mod_info in data.get("modules", []):
            if mod_info.get("active"):
                module_name = mod_info.get("name")
                try:
                    # Construct module path (e.g., modules.my_module)
                    full_module_name = f"{self.modules_dir}.{module_name}"
                    module = importlib.import_module(full_module_name)

                    # Find classes that inherit from BasePlugin
                    for name, obj in inspect.getmembers(module):
                        if (inspect.isclass(obj) and
                            issubclass(obj, BasePlugin) and
                            obj is not BasePlugin):
                            loaded_plugins.append(obj())
                except (ImportError, Exception) as e:
                    print(f"Error loading module {module_name}: {e}")

        self.plugins = loaded_plugins
        return self.plugins
