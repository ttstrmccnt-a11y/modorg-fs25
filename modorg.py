import argparse
import sys
import json
import os
from core.config_manager import ConfigManager
from core.i18n import initialize_i18n, _

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

    # Parse arguments (handles --version and --help automatically)
    args = parser.parse_args()

    # Load modules.json (Skeleton)
    modules_path = "modules.json"
    if os.path.exists(modules_path):
        try:
            with open(modules_path, 'r', encoding='utf-8') as f:
                modules_data = json.load(f)
                # Skeleton: Register modules here in the future
        except (json.JSONDecodeError, IOError) as e:
            # Fallback or error handling
            pass

    # Startup Message
    print(_("STARTUP_MSG"))

    # Starting GUI (Placeholder)
    print(_("GUI_STARTING"))

if __name__ == "__main__":
    main()
