from discord.message import Message
from src.commands.archive.archive import Archive
from src.mapper import GuildMapper


def archive(message: Message, config: dict, *args):
    archiver = Archive(config)


async def map_guild(message: Message, config: dict, *args):
    mapper = GuildMapper(config, message.guild)
    await message.channel.send(f"Creating mapping for {message.guild.name}")

