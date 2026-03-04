from .observer import Subject
import discord
from discord.app_commands import CommandTree
import asyncio


class DiscordClient(discord.Client, Subject):
    def __init__(self, cli):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        discord.Client.__init__(self, intents=intents)
        Subject.__init__(self)
        self.tree = CommandTree(self)

        self.attach(cli)
        self.session_token = None

    async def on_ready(self):
        self.notify('login_successful')

    async def on_message(self, message):
        self.notify('message', message)
        if self.user in message.mentions:
            self.notify('pinged', message)

    async def on_message_edit(self, before, after):
        self.notify('message_edit', after)

    async def on_open_channel(self, channel):
        messages = [msg async for msg in channel.history(limit=10)]
        for message in reversed(messages):
            self.notify('message', message)

    def emit(self, event, *args):
        fn = getattr(self, 'on_' + event)
        asyncio.ensure_future(fn(*args))
