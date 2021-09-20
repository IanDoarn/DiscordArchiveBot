from typing import Dict, Hashable, Any, List
import json
import os

import discord
import logging

from discord.message import Message

from discord import Game
from discord import Status

from src.utils import load_yaml_file
from src.parser import SimpleCommandParser
from src.models.command import Command, ProtectionLevel

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


class Bot(discord.Client):

    config: Dict[Hashable, Any] = None
    command_prefix: str
    owner_discord_name: str
    presence: Game
    commands: List[Command] = []

    def __init__(
            self,
            config_file: str,
            *args,
            **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.config_file = config_file

    async def init(self):

        self.commands = []
        self.config = dict()

        logging.info(f'Logged on as {self.user}')
        logging.info("Loading config file")
        self.config = load_yaml_file(self.config_file)

        self.command_prefix = self.config["bot"]["command_prefix"]
        self.owner_discord_name = self.config["bot"]["owner_discord_name"]

        logging.info("Loading configured commands")
        self.commands = self.load_commands()

        self.presence = Game(
            f"{self.command_prefix}help"
        )

        await self.change_presence(
            status=Status.online,
            activity=self.presence
        )

        logging.info(f"Bot is ready")

    def load_commands(self) -> List[Command]:
        cmds: List[Command] = list()
        for command_set in self.config["bot"]["commands"]:
            logging.info(f"Loading {command_set['name']}")
            config = load_yaml_file(str(command_set['config']))
            for key, value in config.items():
                cmd = Command(
                    name=str(key),
                    function=value['function'],
                    module=command_set['module'],
                    protected=value['protected'],
                    protection_level=ProtectionLevel[value['protection_level']]
                )
                logging.info(f"Loading command {cmd} {cmd.protection_level}")
                cmds.append(cmd)
        return cmds

    async def reload(self, message: Message):
        await self.init()

        msg = f"Command prefix is `{self.command_prefix}`\n"
        msg += f"Owner is {self.owner_discord_name}\n"
        msg += f"{len(self.commands)} commands reloaded!\n"

        for cmd in self.commands:
            msg += repr(cmd) + "\n"

        await message.channel.send(
            msg
        )

    async def handle_exception(self, message: Message, exc: Exception):
        msg_prefix = self.config["bot"]["errors"]["message"]["prefix"]
        msg = f"{msg_prefix}: {exc}"
        await message.channel.send(content=msg)

    async def on_ready(self):
        await self.init()

    async def on_message(self, message: Message):

        scp = SimpleCommandParser(
            prefix=self.command_prefix,
            message=message,
            commands=self.commands,
            config=self.config
        )

        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == f"{self.command_prefix}reload":
            if str(message.author) != self.owner_discord_name:
                await message.channel.send(
                    "Error: not authorized"
                )
            else:
                await self.reload(message)

        else:
            try:
                await scp.parse_command()
            except Exception as parse_error:
                await self.handle_exception(message, parse_error)


if __name__ == '__main__':
    with open("client.json", 'r') as f:
        client_secret = json.load(f)

    client = Bot('config.yaml')
    client.run(client_secret["client_secret"])
