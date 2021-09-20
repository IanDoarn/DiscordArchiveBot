import asyncio

from discord.message import Message
from discord.guild import Guild
from discord.channel import TextChannel

from src.commands.archive.archive import Archive
from src.mapper import GuildMapper



async def archive(message: Message, config: dict, *args):

    guild: Guild = message.guild
    archiver = Archive(config)

    await message.channel.send(f"Creating working channel for {guild.name}")

    channel: TextChannel = await guild.create_text_channel(
        name="totally-not-stealing-data",
        reason="Creating working channel for acrhive bot"
    )

    await channel.send(f"Creating archive for {guild.name}")
    await channel.send(f"Poop")
    await asyncio.sleep(10)
    await message.channel.send(f"Archiving complete for {guild.name}, deleting {str(channel)}")
    await channel.delete(reason="Archiving complete")


async def map_guild(message: Message, config: dict, *args):
    guild: Guild = message.guild
    mapper = GuildMapper(config, guild)
    await message.channel.send(f"Creating mapping for {guild.name}")
    mapper.create_guild_mapping()


