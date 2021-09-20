from discord.message import Message
from discord.guild import Guild

from src.commands.archive.archive import Archive
from src.mapper import GuildMapper


async def archive(message: Message, config: dict, *args):
    guild: Guild = message.guild
    archiver = Archive(config)
    await message.channel.send(f"Creating archive for {guild.name}")


async def map_guild(message: Message, config: dict, *args):
    guild: Guild = message.guild
    mapper = GuildMapper(config, guild)
    await message.channel.send(f"Creating mapping for {guild.name}")
    mapper.create_guild_mapping()


