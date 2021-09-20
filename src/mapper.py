import logging
import os

from discord.guild import Guild


class GuildMapper:

    guild_dir: str

    def __init__(self, config: dict, guild: Guild):
        self.guild = guild
        self.config = config
        self.guild_dir = self.config['bot']['guilds']['mapping']['directory']

    async def create_guild_mapping(self, guild: Guild):
        path = os.path.join(self.guild_dir, guild.name)
        logging.info(f"Creating mapping for {guild.name} at {path}")
        if not os.path.exists(path):
            logging.info(f"Creating directory for {guild.name} at {path}")
            os.mkdir(path)
        else:
            logging.info(f"Found directory for {guild.name} at {path}")
            pass
