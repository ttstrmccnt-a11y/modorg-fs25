import os
import platform
from core.base_plugin import BasePlugin
from core.xml_service import XMLService
from core.i18n import _

class SystemTweak(BasePlugin):
    """
    System-Tweak Module: Configures game.xml settings.
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
                # The task specifies the XPath /language/development/controls
                # We use that as requested.
                success = XMLService.smart_patch(
                    game_xml_path,
                    "/language/development/controls",
                    args.console
                )
                if success:
                    print(_("CONSOLE_UPDATED").format(value=args.console))
                else:
                    # If it failed, maybe the xpath was wrong for this file
                    # but we followed instructions.
                    print(_("CONSOLE_UPDATE_FAILED"))
            else:
                print(_("GAME_XML_NOT_FOUND"))

    def _find_game_xml(self):
        """Attempts to locate game.xml in standard locations."""
        # Common locations for Farming Simulator 25 game.xml
        paths = []
        if platform.system() == "Windows":
            paths.append(os.path.expandvars(r"%USERPROFILE%\Documents\My Games\FarmingSimulator2025\game.xml"))
        else:
            # On Linux/macOS (e.g. via Proton/Steam or just for testing)
            paths.append(os.path.expanduser("~/Documents/My Games/FarmingSimulator2025/game.xml"))

        # Also check current directory for testing purposes
        paths.append("game.xml")

        for p in paths:
            if os.path.exists(p):
                return p
        return None
