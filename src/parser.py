import logging
from typing import Dict, Hashable, Any, Union, List
import importlib

from discord.message import Message
from discord.channel import TextChannel
from discord.guild import Guild

from src.constants import HELP_MENU
from src.models.command import Command, ProtectionLevel


class SimpleCommandParser:

    prefix: str
    message: Message
    commands: Dict[str, Command]

    def __init__(
            self,
            prefix: str,
            message: Message,
            commands: List[Command]
    ) -> None:
        self.prefix = prefix
        self.message = message
        self.commands = {cmd.name: cmd for cmd in commands}

    async def parse_command(self) -> Union[Message, None]:
        content: str = self.message.content
        channel: TextChannel = self.message.channel
        guild: Guild = channel.guild

        # Make sure command starts with the prefix
        if content[:len(self.prefix)] == self.prefix:
            logging.info(f"Command received from {guild} {channel} {self.message.author}! Message: {content}")

            content_base_command: str = content[len(self.prefix):].split(' ')[0]
            content_full: list = content[len(self.prefix):].split(' ')

            if not content_base_command.lower() in list(self.commands.keys()):
                error = ValueError(
                    f"Did not understand command from {guild} {channel} {self.message.author}! Message: {content}"
                )
                await channel.send(
                    content=str(error)
                )
                logging.exception(error)
                raise error
            else:
                return await self.execute_command(
                    self.commands[content_base_command],
                    content_full
                )
        else:
            return None

    async def execute_command(
            self,
            cmd: Command,
            content: list
    ) -> Union[Message, None]:
        module = importlib.import_module(cmd.module)
        function_name = cmd.function

        # execute method
        result = getattr(module, function_name)(*content[1:])
        logging.info(f"Executing {module} {function_name}")
        return await self.message.channel.send(result)

    @staticmethod
    def help() -> str:
        return HELP_MENU


