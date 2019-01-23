from .DiscordClient import DiscordClient
from .observer import Observer
from .Config import *
from getpass import getpass

from prompt_toolkit import prompt, print_formatted_text, HTML
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style
from prompt_toolkit.styles.pygments import style_from_pygments_cls
from pygments.styles import get_style_by_name
from .Validators import (
    JoinableGuildListValidator,
    JoinableChannelListValidator
)
from xml.sax.saxutils import escape
import click

import asyncio
import discord

from prompt_toolkit.eventloop.defaults import use_asyncio_event_loop
from prompt_toolkit.patch_stdout import patch_stdout

from .Config import ConfigManager


class CLI(Observer):
    def __init__(self):
        Observer.__init__(self)
        self.client = DiscordClient(self)
        # click.clear()

        self.config = ConfigManager()
        self.current_guild = None
        self.current_channel = None
        self.channel_open = False

    def login(self):
        if self.config.auto_login_enabled():
            self.update('login_in_progress')
            self.client.run(self.config.get_token(), bot=False)
        else:
            email = prompt('Email: ')
            password = prompt('Password: ', is_password=True)

            if self.config.first_time():
                auto_login = prompt('Automatically login in the future? y/n: ')
                while auto_login not in ['y', 'n']:
                    auto_login = prompt('Invalid selection. Please select y/n')

                if auto_login == 'y':
                    self.config.enable_auto_login()

            self.client.login_with_email_password(email, password)

    def open_channel(self):
        click.clear()
        self.channel_open = True
        self.client.emit('open_channel', self.current_channel)
        asyncio.ensure_future(self.channel_prompt())

    def display_guilds(self):
        guilds = ''
        for i, guild in enumerate(self.client.guilds):
            guilds += '{0}: {1}\n'.format(i, guild.name)
        click.echo_via_pager(guilds)
        click.echo('Select a server by entering the corresponding server number')
        self.select_guild()

    def select_guild(self):
        selection = int(
            prompt('>', validator=JoinableGuildListValidator(len(self.client.guilds))))
        self.current_guild = self.client.guilds[int(selection)]
        click.clear()
        click.secho(
            'Connected to {}'.format(
                self.current_guild.name),
            fg='black',
            bg='white')
        self.select_channel()

    def select_channel(self):
        if self.current_guild:
            channels = ''
            text_channels = self.current_guild.text_channels

            for channel in text_channels:
                channels += '#' + channel.name + '\n'

            click.echo_via_pager(channels)
            click.echo('Select a channel by entering the corresponding #channel-name')

            completer = WordCompleter(['#' + t.name for t in text_channels])

            selection = prompt('>',
                               validator=JoinableChannelListValidator(text_channels),
                               completer=completer)

            for channel in text_channels:
                if selection[1:] == channel.name:
                    self.current_channel = channel

            self.open_channel()

    async def channel_prompt(self):
        if self.current_channel:
            use_asyncio_event_loop()

            with patch_stdout():
                msg = await prompt('>', async_=True)
                await self.current_channel.send(msg)
                await self.channel_prompt()

    def update(self, action: str, data=None):
        """Prints information passed by DiscordClient
        """
        # login actions
        if action == 'login_in_progress':
            click.echo('Logging in...')
        elif action == 'login_successful':
            click.clear()
            click.secho('You are logged in as %s.' %
                        (self.client.user.name,), fg='black', bg='white')
            if self.client.session_token:
                self.config.set_token(self.client.session_token)
            self.display_guilds()
        elif action == 'login_incorrect_email_format':
            click.secho('Not a well formed email address.', fg='red', bold=True)
            self.login()
        elif action == 'login_incorrect_password':
            click.secho('Password is incorrect.', fg='red', bold=True)
            self.login()
        elif action == 'login_captcha_required':
            click.secho(
                'Captcha required.\n' +
                'Please login through the Discord web client first.\n' +
                'https://discordapp.com/login', fg='red', bold=True)
            self.login()

        # message actions
        elif action == 'message':
            msg = data
            color = discord.Color.from_rgb(
                255, 255, 255) if msg.author.color == discord.Color.default() else msg.author.color
            if self.current_channel:
                if self.current_channel.id == msg.channel.id and self.channel_open:
                    print_formatted_text(HTML(
                        '<_ fg="%s">%s</_>> %s' % (
                            str(color),
                            msg.author.display_name,
                            escape(msg.content)
                        )))
