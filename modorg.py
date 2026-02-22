import argparse
import sys
import os
from core.config_manager import ConfigManager
from core.i18n import initialize_i18n, _
from core.plugin_engine import PluginLoader

VERSION = "0.1.0"

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
        add_help=False
    )

    parser.add_argument(
        '-v', '--version',
        action='version',
        version=f"modorg {VERSION}",
        help=_("VERSION_DESC")
    )

    parser.add_argument(
        '-h', '--help',
        action='help',
        help=_("HELP_DESC")
    )

    # Subparsers for modules
    subparsers = parser.add_subparsers(dest="command")

    # Plugin Loading
    loader = PluginLoader()
    plugins = loader.load_plugins()

    # Register arguments for each active plugin
    for plugin in plugins:
        plugin.register_arguments(subparsers)

    # Parse arguments
    args = parser.parse_args()

    # Startup Message
    print(_("STARTUP_MSG"))

    # Execute plugins
    plugin_executed = False
    for plugin in plugins:
        if plugin.execute(args):
            plugin_executed = True
            break

    # Starting GUI (Placeholder) if no plugin was executed
    if not plugin_executed:
        print(_("GUI_STARTING"))

if __name__ == "__main__":
    main()
