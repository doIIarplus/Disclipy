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

from .ChatCommands import ChatCommands as CMD

from .DefaultEmojis import emojis


class CLI(Observer):
    def __init__(self):
        Observer.__init__(self)
        self.client = DiscordClient(self)
        click.clear()

        # TODO add completer for emojis
        self.default_emojis = list(emojis)

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
        self.client.emit('open_channel', self.current_channel)
        asyncio.ensure_future(self.channel_prompt())
        self.channel_open = True

    def display_guilds(self):
        guilds = ''
        for i, guild in enumerate(self.client.guilds):
            guilds += '{0}: {1}\n'.format(i, guild.name)
        click.echo_via_pager(guilds)

    def select_guild(self):
        click.echo('Select a server by entering the corresponding server number')
        selection = int(
            prompt('>', validator=JoinableGuildListValidator(len(self.client.guilds))))
        self.current_guild = self.client.guilds[int(selection)]
        click.clear()
        click.secho(
            'Connected to {}'.format(
                self.current_guild.name),
            fg='black',
            bg='white')
        self.display_channels()
        self.select_channel()

    def display_channels(self):
        if self.current_guild:
            channels = ''
            text_channels = self.current_guild.text_channels

            for channel in text_channels:
                channels += '#' + channel.name + '\n'

            click.echo_via_pager(channels)

    def select_channel(self):
        if self.current_guild:
            text_channels = self.current_guild.text_channels

            click.echo('Select a channel by entering the corresponding #channel-name')

            completer = WordCompleter(
                ['#' + t.name for t in text_channels], ignore_case=True, sentence=True)

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
                if not msg.startswith(CMD.PREFIX):
                    if msg:
                        await self.current_channel.send(msg)
                else:
                    self.handleCommands(msg)

                await self.channel_prompt()
        else:
            text_channels = self.current_guild.text_channels
            completer = WordCompleter(
                ['#' + t.name for t in text_channels], ignore_case=True, sentence=True)
            selected_channel = await prompt('>',
                                            async_=True,
                                            completer=completer,
                                            validator=JoinableChannelListValidator(text_channels))
            selected_channel = selected_channel[1:]

            for channel in text_channels:
                if selected_channel == channel.name:
                    self.current_channel = channel
                    click.clear()
                    self.client.emit('open_channel', self.current_channel)

            await self.channel_prompt()

    def handleCommands(self, msg):
        if CMD.HELP.match(msg):
            cmds = CMD.get_command_list()
            CMD.print('Here is a list of commands:\n' + '\n'.join(cmds))
        elif CMD.LIST_SERVERS.match(msg):
            self.display_guilds()
        elif CMD.JOIN_SERVER.match(msg):
            try:
                guild_n = CMD.JOIN_SERVER.match(msg).group(1)
                guild_n = int(guild_n)
                self.current_guild = self.client.guilds[guild_n]
                # THIS VIOLATES DRY PRINCIPLES
                # refactor some time
                self.display_channels()
                self.current_channel = None
                print_formatted_text(
                    'Select a channel by entering the corresponding #channel-name')
            except ValueError:
                CMD.print(
                    '"%s" not found. Please select a guild by index. Find the desired guild index by using:\n%s' %
                    (guild_n, str(
                        CMD.JOIN_SERVER)))
            except IndexError:
                CMD.print('Invalid guild index, must be in range 0-%s' %
                          (str(len(self.client.guilds),)))
        elif CMD.LIST_CHANNELS.match(msg):
            self.display_channels()
        elif CMD.JOIN_CHANNEL.match(msg):
            # THIS VIOLATES DRY PRINCIPLES
            # refactor some time
            selected_channel = CMD.JOIN_CHANNEL.match(msg).group(1)
            text_channels = self.current_guild.text_channels

            channel_exists = False

            for channel in text_channels:
                if selected_channel == channel.name:
                    self.current_channel = channel
                    channel_exists = True
                    break

            if channel_exists:
                click.clear()
                self.client.emit('open_channel', self.current_channel)
            else:
                print_formatted_text(
                    HTML(
                        '<b bg="#ffffff" fg="#000000">'
                        + escape(
                            '#'
                            + selected_channel) +
                        ' does not exist.</b>'))
        else:
            CMD.print(
                '"%s" command not found. Get a list of commands with:\n%s' % (
                    msg, str(CMD.HELP)
                ))

    def __get_embed_text(self, embed_attr):
        try:
            return escape(embed_attr)
        except AttributeError:
            return ''

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
            self.select_guild()
        elif action == 'login_incorrect_email_format':
            click.secho('Not a well formed email address.', fg='red', bold=True)
            self.login()
        elif action == 'login_incorrect_password':
            click.secho('Password is incorrect.', fg='red', bold=True)
            self.login()
        elif action == 'login_captcha_required':
            click.secho(
                'Captcha required.\n'
                + 'Please login through the Discord web client first.\n'
                + 'https://discordapp.com/login', fg='red', bold=True)
            self.login()

        # message actions
        elif action == 'message':
            msg = data
            color = discord.Color.from_rgb(
                255, 255, 255) if msg.author.color == discord.Color.default() else msg.author.color
            if self.current_channel:
                if self.current_channel.id == msg.channel.id and self.channel_open:
                    message = msg.content

                    # add image urls
                    for att in msg.attachments:
                        message += '\n' + att.proxy_url

                    # add embed display
                    embeds = '\n' if msg.embeds else ''
                    for embed in msg.embeds:
                        #color_bar = '<_ bg="%s"> </_> ' % (str(embed.colour),)

                        author = self.__get_embed_text(embed.author.name)
                        if author:
                            author = '<b>%s</b>' % (author,)

                        title = self.__get_embed_text(embed.title)
                        description = self.__get_embed_text(embed.description)
                        fields = '\n'.join(['<b>%s</b>\n%s' % (
                            self.__get_embed_text(f.name),
                            self.__get_embed_text(f.value)
                        ) for f in embed.fields])
                        video = self.__get_embed_text(embed.video.url)
                        image = self.__get_embed_text(
                            embed.image.proxy_url or embed.image.url or '')
                        footer = self.__get_embed_text(embed.footer.text)

                        text = []

                        bar = '<b bg="#eeeeee" fg="#333333">' + ('=' * 32) + '</b>'
                        text.append(bar)
                        if author:
                            text.append(author)
                        if title:
                            text.append(title)
                        if description:
                            text.append(description)
                        if fields:
                            text.append(fields)
                        if video:
                            text.append(video)
                        if image:
                            text.append(image)
                        if footer:
                            text.append(footer)
                        text.append(bar + '\n\n')

                        embeds += '\n\n'.join(text)

                    print_formatted_text(HTML(
                        '<_ fg="%s">%s</_>> %s' % (
                            str(color),
                            escape(msg.author.display_name),
                            escape(message)
                            + embeds
                        )))
