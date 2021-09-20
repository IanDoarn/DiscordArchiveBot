import logging
import os

from discord.guild import Guild


class GuildMapper:

    guild_dir: str

    def __init__(self, config: dict, guild: Guild):
        self.guild = guild
        self.config = config
        self.guild_dir = self.config['bot']['guilds']['mapping']['directory']

    def create_guild_mapping(self):
        self.create_directory()

    def create_directory(self):
        path = os.path.join(self.guild_dir, self.guild.name)
        logging.info(f"Creating mapping for {self.guild.name} at {path}")
        if not os.path.exists(path):
            os.makedirs(path)
            logging.info(f"Created directory for {self.guild.name} at {path}")
        else:
            logging.info(f"Found directory for {self.guild.name} at {path}")