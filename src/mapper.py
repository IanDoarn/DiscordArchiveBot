from discord.guild import Guild


class GuildMapper:

    def __init__(self, guild: Guild, directory: str):
        self.guild = guild
        self.guild_dir = directory

    def create_guild_map(self):
        ...
