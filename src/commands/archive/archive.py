import logging
from typing import Dict, Hashable, Any, List

from discord.channel import (
    ChannelType,
    TextChannel
)
from discord.message import Message
from discord.guild import Guild


class Archive:

    config: Dict[Hashable, Any]
    guild: Guild
    working_channel: TextChannel

    # configured setting
    limit: int

    def __init__(
            self,
            config: Dict[Hashable, Any],
            guild: Guild,
            working_channel: TextChannel
    ):
        self.config = config["archive"]
        self.limit = self.config["message"]["limit"]

        self.guild = guild
        self.working_channel = working_channel

    async def create_guild_archive(self):
        message = await self.working_channel.send(f"Creating archive for {self.guild.name}")

        channels: List[TextChannel] = [x for x in self.guild.channels if x.type == ChannelType.text]

        logging.info(f"Found {len(channels)} in guild {self.guild.name}")
        await message.edit(content=f"{message.content}\nFound {len(channels)} in guild {self.guild.name}")

        for channel in channels:
            await self.download_messages_from_channel(channel)

    async def download_messages_from_channel(self, channel: TextChannel):
        message_base = f"Attempting to archive {channel.name}! Limit set to {self.limit}." \
                       f"\nThis operation will take some time.\n\n"
        messages: List[Message] = list()
        counter = 0
        logging.info(message_base)
        bot_message = await self.working_channel.send(message_base)

        async for message in channel.history(limit=self.limit, oldest_first=True):
            msg: Message = message
            counter += 1
            if counter % 1000 == 0:
                await bot_message.edit(content=f"{message_base}Total: {counter}")

        logging.info(f"Collected {len(messages)}")
        content = f"{message_base}\n"\
                  f"Gathered {len(messages)} from {channel.name}!\n"\
                  f"Total: {counter}\n"\
                  f"Complete!\n"



        #                 async for elem in guild_channel.history(limit=_limit, oldest_first=True):
        #                     msg: Message = elem
        #
        #                     messages.append(
        #                         {
        #                             'guild_id': guild.id,
        #                             'guild': str(guild.id),
        #                             'id': msg.id,
        #                             'user': str(msg.author),
        #                             'content': msg.content,
        #                             'channel_id': channel.id,
        #                             'channel': str(msg.channel),
        #                             'date_posted': msg.created_at.strftime("%m/%d/%Y, %H:%M:%S"),
        #                             'message_type': str(msg.type)
        #                         }
        #                     )
        #
        #                     counter += 1
        #                     if counter % 1000 == 0:
        #                         await bot_message.edit(content=f"Trying to gather message, limit is {_limit}, from {guild_channel}."
        #                                                        f"This will take some time.\nTotal: {counter}")
        #
        #                 print(f"Collected {len(messages)}")
        #
        #                 content = f"Gathered {len(messages)} from {guild_channel}!\n" \
        #                           f"Total: {counter}\n" \
        #                           f"Complete!\n"
        #
        #                 await bot_message.edit(content=content)
        #
        #                 dump_file = f"{str(guild_channel)}_{datetime.datetime.now().strftime('%m-%d-%Y_%H%M%S')}.json"
        #                 if not os.path.exists(os.path.join(os.getcwd(), str(guild))):
        #                     os.mkdir(os.path.join(os.getcwd(), str(guild)))
        #                 with open(os.path.join(os.getcwd(), str(guild), dump_file), 'w') as dump:
        #                     json.dump(messages, dump)
        #
        #                 print(f"{len(messages)} dumped from {str(current_guild)} - #{guild_channel} to {dump_file}")
        #
        #             except Exception as gather_error:
        #                 await message.channel.send(
        #                     content=f"{message.author.mention} something went wrong in {str(guild)}! {str(gather_error)}",
        #                     mention_author=True
        #                 )
        #
        #         _dir = os.getcwd()
        #
        #         zip_file = f"{guild}__{datetime.datetime.now().strftime('%m-%d-%Y_%H_%M_%S')}.zip"
        #         print(f'Creating ZIP file {zip_file}')
        #
        #         self.create_zip_file(zip_file, os.path.join(_dir, str(guild)))
        #
        #         await channel.send(
        #             content=f"Data dump complete.",
        #             file=File(zip_file)
        #         )
        #
        #     except Exception as error:
        #         await message.channel.send(
        #             content=f"{message.author.mention} something went wrong in {str(guild)}! {str(error)}",
        #             mention_author=True
        #         )