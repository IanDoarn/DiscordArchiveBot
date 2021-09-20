import asyncio
import logging

from discord.message import Message
from discord.guild import Guild
from discord.channel import TextChannel

from src.commands.archive.archive import Archive


async def archive(message: Message, config: dict, *args):
    guild: Guild = message.guild
    await message.channel.send(f"Creating working channel for {guild.name}")

    channel: TextChannel = await guild.create_text_channel(
        name="totally-not-stealing-data",
        reason="Creating working channel for acrhive bot"
    )

    archiver = Archive(config, guild, channel)
    try:
        await archiver.create_guild_archive()

        await asyncio.sleep(10)
        await message.channel.send(f"Archiving complete for {guild.name}, deleting {str(channel)}")
        await channel.delete(reason="Archiving complete")
    except Exception as error:
        logging.exception(error)
        await message.channel.send(f"Something went wrong creating archive for {guild.name}, deleting {str(channel)}")
        await channel.delete(reason=f"Archiving failed {error}")
        raise


