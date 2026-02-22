import json
import os
import copy

class ConfigManager:
    """
    Manages the application configuration, supporting a 'global' section
    and 'modules' sections.
    """
    DEFAULT_CONFIG = {
        "global": {
            "language": "en",
            "version": "0.1.0"
        },
        "modules": {}
    }

    def __init__(self, config_path="config.json"):
        self.config_path = config_path
        self.config = copy.deepcopy(self.DEFAULT_CONFIG)
        self.load()

    def load(self):
        """Loads configuration from the JSON file."""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    # Simple merge
                    if "global" in loaded_config:
                        self.config["global"].update(loaded_config["global"])
                    if "modules" in loaded_config:
                        self.config["modules"].update(loaded_config["modules"])
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading config: {e}")
        else:
            self.save()

    def save(self):
        """Saves current configuration to the JSON file."""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4)
        except IOError as e:
            print(f"Error saving config: {e}")

    def get_global(self, key, default=None):
        """Returns a value from the global configuration section."""
        return self.config.get("global", {}).get(key, default)

    def set_global(self, key, value):
        """Sets a value in the global configuration section and saves."""
        self.config["global"][key] = value
        self.save()

    def get_module_config(self, module_name):
        """Returns the configuration for a specific module."""
        return self.config.get("modules", {}).get(module_name, {})

    def set_module_config(self, module_name, config_data):
        """Sets the configuration for a specific module and saves."""
        self.config["modules"][module_name] = config_data
        self.save()
