import logging
from typing import Dict, Union, List
import importlib
import inspect

from discord.message import Message
from discord.channel import TextChannel
from discord.guild import Guild

from src.models.command import Command, ProtectionLevel


class SimpleCommandParser:

    prefix: str
    message: Message
    commands: Dict[str, Command]
    config: dict

    def __init__(
            self,
            prefix: str,
            message: Message,
            commands: List[Command],
            config: dict
    ) -> None:
        self.prefix = prefix
        self.message = message
        self.config = config
        self.commands = {cmd.name: cmd for cmd in commands}

    async def parse_command(self) -> Union[Message, None]:
        content: str = self.message.content
        channel: TextChannel = self.message.channel
        guild: Guild = channel.guild

        # Make sure command starts with the prefix
        if content[:len(self.prefix)] == self.prefix:
            logging.info(f"Command received from {guild} {channel} {self.message.author}! Message: {content}")

            content_base_command: str = content[len(self.prefix):].split(' ')[0]

            if not content_base_command.lower() in list(self.commands.keys()):
                error = ValueError(
                    f"Did not understand command from {guild} {channel} {self.message.author}! Message: {content}"
                )
                logging.exception(error)
                raise error
            else:
                cmd: Command = self.commands[content_base_command]
                if self.can_user_execute_command(cmd, self.message):
                    return await self.execute_command(cmd)
                else:
                    raise PermissionError(f"Not authorized to execute command: {cmd}")
        else:
            return None

    def can_user_execute_command(self, command: Command, message: Message) -> bool:
        owner_discord_name = self.config["bot"]["owner_discord_name"]
        if not command.protected:
            return True
        else:
            if command.protection_level == ProtectionLevel.OWNER and str(message.author) != owner_discord_name:
                return False
            else:
                return True
            # TODO: implement a way to map roles in a server to permission level

    async def execute_command(self, cmd: Command) -> Union[Message, None]:
        content: str = self.message.content
        full_command: list = content[len(self.prefix):].split(' ')
        module = importlib.import_module(cmd.module)
        function_name = cmd.function

        # execute method
        logging.info(f"Executing {module} {function_name}")
        _inputs = (
            self.message,
            self.config,
            *full_command[1:]
        )
        if inspect.iscoroutinefunction(getattr(module, function_name)):
            result = await getattr(module, function_name)(*_inputs)
        else:
            result = getattr(module, function_name)(*_inputs)



