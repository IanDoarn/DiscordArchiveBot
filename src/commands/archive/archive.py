from typing import Dict, Hashable, Any, List

from discord.message import Message
from discord.channel import TextChannel
from discord.guild import Guild


class Archive:

    config: Dict[Hashable, Any]

    # configured setting
    limit: int

    def __init__(self, config: Dict[Hashable, Any]):
        self.config = config["archive"]
        self.limit = self.config["message"]["limit"]


        # if content.lower().startswith(self.command_prefix):
        #     x = parse_command(self.command_prefix, Message)
        #     if str(message.author) != self.owner_discord_name:
        #         bot_message = await channel.send(
        #             content="Error: not authorized"
        #         )
        #     try:
        #         _limit = 1000000
        #
        #         current_guild: Guild = self.get_guild(guild.id)
        #         all_channels = current_guild.channels
        #
        #         content = f"Found {len(all_channels)} in {str(current_guild)}.\n" \
        #                   f"Attempting to archive entire server! Downloading data from the below channels:\n\n"
        #
        #         for c in all_channels:
        #             if type(c) == TextChannel:
        #                 content += str(c) + "\n"
        #
        #         await channel.send(
        #             content=content
        #         )
        #
        #         for guild_channel in all_channels:
        #             print(guild_channel)
        #             counter = 0
        #             messages: List[dict] = []
        #
        #             bot_message = await channel.send(
        #                 content=f"Trying to gather message, limit is {_limit}, from {guild_channel}."
        #                         f"This will take some time.\nTotal: {counter}",
        #                 mention_author=True
        #             )
        #
        #             try:
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