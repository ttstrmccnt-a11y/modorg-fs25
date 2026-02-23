import argparse
import sys
import json
import os
import importlib
import inspect
from core.config_manager import ConfigManager
from core.i18n import initialize_i18n, _
from core.base_plugin import BasePlugin

VERSION = "0.1.0"

def load_plugins(config_manager, parser):
    """
    Dynamically loads active modules from modules.json and registers their arguments.
    """
    modules_path = "modules.json"
    plugins = {}

    if not os.path.exists(modules_path):
        return plugins

    try:
        with open(modules_path, 'r', encoding='utf-8') as f:
            modules_data = json.load(f)
    except (json.JSONDecodeError, IOError):
        return plugins

    subparsers = parser.add_subparsers(dest="command", help=_("SUBCOMMAND_HELP"))

    modules_list = modules_data.get("modules", [])

    # Handle both dict and list structures
    if isinstance(modules_list, dict):
        modules_to_load = modules_list.items()
    else:
        modules_to_load = [(m.get("name"), m) for m in modules_list if isinstance(m, dict)]

    for mod_name, mod_info in modules_to_load:
        if mod_name and mod_info.get("active"):
            try:
                module = importlib.import_module(f"modules.{mod_name}")
                # Find the subclass of BasePlugin in the module
                for name, obj in inspect.getmembers(module):
                    if inspect.isclass(obj) and issubclass(obj, BasePlugin) and obj is not BasePlugin:
                        instance = obj(config_manager)
                        plugin_parser = subparsers.add_parser(mod_name, help=_(f"HELP_{mod_name.upper()}"))
                        instance.register_arguments(plugin_parser)
                        plugins[mod_name] = instance
                        break
            except Exception as e:
                print(f"Error loading module {mod_name}: {e}")

    return plugins

def main():
    """
    Main entry point for modorg.
    Initializes core components, handles arguments, and starts the application.
    """
    # Initialize ConfigManager
    config_manager = ConfigManager()

    # Initialize Translator
    initialize_i18n(config_manager)

    # Argument Parsing
    parser = argparse.ArgumentParser(
        prog="modorg",
        description=_("APP_DESCRIPTION"),
        add_help=True
    )

    parser.add_argument(
        '-v', '--version',
        action='version',
        version=f"modorg {VERSION}",
        help=_("VERSION_DESC")
    )

    # Load and register plugins
    plugins = load_plugins(config_manager, parser)

    # Parse arguments
    args = parser.parse_args()

    if args.command:
        # Execute the chosen plugin
        if args.command in plugins:
            plugins[args.command].execute(args)
    else:
        # Startup Message
        print(_("STARTUP_MSG"))
        # Starting GUI (Placeholder)
        print(_("GUI_STARTING"))

if __name__ == "__main__":
    main()
