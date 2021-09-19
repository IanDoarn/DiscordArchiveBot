from typing import Dict, Hashable, Any

HELP_MENU = f"""
Help menu not yet complete!
Head over to https://github.com/IanDoarn/DiscordArchiveBot/blob/development/README.md for more details!
"""


AVAILABLE_COMMANDS: Dict[str, Dict[Hashable, Any]] = {
    "help": {"protected": False},
    "test": {"protected": True},
}
