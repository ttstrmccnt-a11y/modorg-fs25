import os
import platform
from core.base_plugin import BasePlugin
from core.xml_service import XMLService
from core.i18n import _

class SystemTweak(BasePlugin):
    """
    System-Tweak Module: Configures game.xml settings for Farming Simulator 25.
    """
    def register_arguments(self, parser):
        """Adds CLI arguments for the system_tweak module."""
        parser.add_argument(
            '--console',
            choices=['true', 'false'],
            help=_("HELP_CONSOLE")
        )

    def execute(self, args):
        """Executes the system-tweak logic."""
        if args.console is not None:
            game_xml_path = self._find_game_xml()
            if game_xml_path and os.path.exists(game_xml_path):
                # The XPath for FS25 is /game/development/controls.
                # Older versions sometimes used different paths, but FS25
                # strictly follows this structure in game.xml.
                xpath = "/game/development/controls"

                success = XMLService.smart_patch(
                    game_xml_path,
                    xpath,
                    args.console
                )

                if success:
                    print(_("CONSOLE_UPDATED").format(value=args.console))
                else:
                    # XMLService returns False if XPath is not found
                    print(_("XPATH_NOT_FOUND").format(xpath=xpath))
            else:
                print(_("GAME_XML_NOT_FOUND"))

    def _find_game_xml(self):
        """
        Attempts to locate game.xml specifically in the FarmingSimulator2025 directory
         to avoid confusion with older game versions.
        """
        paths = []
        if platform.system() == "Windows":
            # Standard path on Windows
            paths.append(os.path.expandvars(r"%USERPROFILE%\Documents\My Games\FarmingSimulator2025\game.xml"))
        else:
            # Standard path on Linux (Proton) or macOS
            paths.append(os.path.expanduser("~/Documents/My Games/FarmingSimulator2025/game.xml"))

        # Fallback for testing or non-standard installations
        paths.append("game.xml")

        for p in paths:
            if os.path.exists(p):
                return p
        return None
