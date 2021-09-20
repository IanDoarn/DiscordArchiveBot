from discord.message import Message
from discord.emoji import Emoji


def _help(*args):
    return f"""
Help menu not yet complete!
Head over to https://github.com/IanDoarn/DiscordArchiveBot/blob/development/README.md for more details!
"""


async def hello(message: Message, *args):
    return await message.channel.send(
        content=f"Hello, {message.author.mention} :wave:"
    )
