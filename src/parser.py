import logging
from typing import Dict, Hashable, Any, Union, List

from discord.message import Message
from discord.channel import TextChannel
from discord.guild import Guild

from src.constants import HELP_MENU
from src.models.command import Command, ProtectionLevel


class SimpleCommandParser:

    prefix: str
    message: Message
    commands: List[Command]

    def __init__(
            self,
            prefix: str,
            message: Message,
            commands: List[Command]
    ) -> None:
        self.prefix = prefix
        self.message = message
        self.commands = commands

    async def parse_command(self) -> Union[Message, None]:
        content: str = self.message.content
        channel: TextChannel = self.message.channel
        guild: Guild = channel.guild

        # Make sure command starts with the prefix
        if content[:len(self.prefix)] == self.prefix:
            logging.info(f"Command received from {guild} {channel} {self.message.author}! Message: {content}")
            content_msg = content[len(self.prefix):]
            if not self.__is_valid_command(content_msg.lower()):
                error = ValueError(
                    f"Did not understand command from {guild} {channel} {self.message.author}! Message: {content}"
                )
                await channel.send(
                    content=str(error)
                )
                logging.exception(error)
                raise error
            elif content_msg.lower() == 'help':
                return await self.message.author.send(
                    content=self.help()
                )
        else:
            return None

    @staticmethod
    def help() -> str:
        return HELP_MENU
