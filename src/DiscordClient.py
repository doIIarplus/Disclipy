from .observer import Subject
import discord
import discord.client
from discord.app_commands import CommandTree
from discord.user import ClientUser
import asyncio


class _UserToken(str):
    """String subclass where 'Bot ' + token returns just the token.

    discord.py hardcodes 'Bot ' + self.token in the Authorization header.
    Python tries __radd__ first when the right operand is a subclass of the
    left operand's type, so 'Bot ' + UserToken('x') returns 'x'.
    """

    def __radd__(self, other):
        return str(self)


class DiscordClient(discord.Client, Subject):
    def __init__(self, cli, bot=True):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        discord.Client.__init__(self, intents=intents)
        Subject.__init__(self)
        self._is_bot = bot
        self.tree = CommandTree(self) if bot else None

        self.attach(cli)
        self.session_token = None

        if not bot:
            self._patch_http_auth()

    def _patch_http_auth(self):
        """Patch HTTP client to send user token without 'Bot ' prefix.

        Makes http.token a property that wraps any assigned value in
        _UserToken, so the hardcoded 'Bot ' + self.token in request()
        returns just the raw token via __radd__.
        """
        http = self.http
        original_token = http.token

        OriginalClass = type(http)

        class _PatchedHTTPClient(OriginalClass):
            @property
            def token(self):
                return self._user_token

            @token.setter
            def token(self, value):
                self._user_token = _UserToken(value) if value is not None else None

        http._user_token = _UserToken(original_token) if original_token else None
        http.__class__ = _PatchedHTTPClient

    async def login(self, token):
        if self._is_bot:
            return await super().login(token)

        # User-token login: replicate the bot login flow but skip
        # application_info() which is a bot-only endpoint.
        if not isinstance(token, str):
            raise TypeError(
                f'expected token to be a str, received {token.__class__.__name__} instead'
            )
        token = token.strip()

        if self.loop is discord.client._loop:
            await self._async_setup_hook()

        data = await self.http.static_login(token)
        self._connection.user = ClientUser(state=self._connection, data=data)
        await self.setup_hook()

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
