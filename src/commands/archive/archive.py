from typing import Dict, Hashable, Any, List

from discord.message import Message
from discord.channel import TextChannel
from discord.guild import Guild


class Archive:

    config: Dict[Hashable, Any]

    # configured setting
    limit: int

    def __init__(self, config: Dict[Hashable, Any]):
        self.config = config["archive"]
        self.limit = self.config["message"]["limit"]


