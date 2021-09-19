import discord
from discord.message import Message
from discord.channel import TextChannel
from discord.file import File
from discord.guild import Guild

from typing import List
import random
import json
import datetime
import os
import zipfile


class MyClient(discord.Client):

    @staticmethod
    def create_zip_file(filename, zipfile_path):
        def zipdir(path, ziph):
            # ziph is zipfile handle
            for root, dirs, files in os.walk(path):
                for file in files:
                    ziph.write(os.path.join(root, file),
                               os.path.relpath(os.path.join(root, file),
                                               os.path.join(path, '..')))

        zipf = zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED)
        zipdir(zipfile_path, zipf)
        zipf.close()

    async def on_ready(self):
        print('Logged on as', self.user)

        print('Active Guilds')
        for guild in self.guilds:
            print(f"{guild.name}")

    async def on_message(self, message: Message):
        content: str = message.content
        channel: TextChannel = message.channel
        guild: Guild = channel.guild

        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == 'ping':
            await message.channel.send('pong')

        if content.lower().startswith("emote?"):

            print(guild.emojis)
            bot_message = await channel.send(
                content=random.choice(guild.emojis)
            )

        if content.lower().startswith("download pls"):
            if str(message.author) != "baxterthehusky#1003":
                bot_message = await channel.send(
                    content="Error: not authorized"
                )
            try:
                _limit = 1000000

                current_guild: Guild = self.get_guild(guild.id)
                all_channels = current_guild.channels

                content = f"Found {len(all_channels)} in {str(current_guild)}.\n" \
                          f"Attempting to archive entire server! Downloading data from the below channels:\n\n"

                for c in all_channels:
                    if type(c) == TextChannel:
                        content += str(c) + "\n"

                await channel.send(
                    content=content
                )

                for guild_channel in all_channels:
                    print(guild_channel)
                    counter = 0
                    messages: List[dict] = []

                    bot_message = await channel.send(
                        content=f"Trying to gather message, limit is {_limit}, from {guild_channel}."
                                f"This will take some time.\nTotal: {counter}",
                        mention_author=True
                    )

                    try:
                        async for elem in guild_channel.history(limit=_limit, oldest_first=True):
                            msg: Message = elem

                            messages.append(
                                {
                                    'guild_id': guild.id,
                                    'guild': str(guild.id),
                                    'id': msg.id,
                                    'user': str(msg.author),
                                    'content': msg.content,
                                    'channel_id': channel.id,
                                    'channel': str(msg.channel),
                                    'date_posted': msg.created_at.strftime("%m/%d/%Y, %H:%M:%S"),
                                    'message_type': str(msg.type)
                                }
                            )

                            counter += 1
                            if counter % 1000 == 0:
                                await bot_message.edit(content=f"Trying to gather message, limit is {_limit}, from {guild_channel}."
                                                               f"This will take some time.\nTotal: {counter}")

                        print(f"Collected {len(messages)}")

                        content = f"Gathered {len(messages)} from {guild_channel}!\n" \
                                  f"Total: {counter}\n" \
                                  f"Complete!\n"

                        await bot_message.edit(content=content)

                        dump_file = f"{str(guild_channel)}_{datetime.datetime.now().strftime('%m-%d-%Y_%H%M%S')}.json"
                        if not os.path.exists(os.path.join(os.getcwd(), str(guild))):
                            os.mkdir(os.path.join(os.getcwd(), str(guild)))
                        with open(os.path.join(os.getcwd(), str(guild), dump_file), 'w') as dump:
                            json.dump(messages, dump)

                        print(f"{len(messages)} dumped from {str(current_guild)} - #{guild_channel} to {dump_file}")

                    except Exception as gather_error:
                        await message.channel.send(
                            content=f"{message.author.mention} something went wrong in {str(guild)}! {str(gather_error)}",
                            mention_author=True
                        )

                _dir = os.getcwd()

                zip_file = f"{guild}__{datetime.datetime.now().strftime('%m-%d-%Y_%H_%M_%S')}.zip"
                print(f'Creating ZIP file {zip_file}')

                self.create_zip_file(zip_file, os.path.join(_dir, str(guild)))

                await channel.send(
                    content=f"Data dump complete.",
                    file=File(zip_file)
                )

            except Exception as error:
                await message.channel.send(
                    content=f"{message.author.mention} something went wrong in {str(guild)}! {str(error)}",
                    mention_author=True
                )


if __name__ == '__main__':
    with open("client.json", 'r') as f:
        client_secret = json.load(f)

    client = MyClient()
    client.run(client_secret["client_secret"])