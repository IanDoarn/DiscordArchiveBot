from discord.message import Message
from src.commands.archive.archive import Archive


def archive(message: Message, config: dict, *args):
    archiver = Archive(config)



