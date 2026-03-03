from .DiscordClient import DiscordClient
from .observer import Observer

from prompt_toolkit import prompt, PromptSession, print_formatted_text
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit.formatted_text import ANSI, FormattedText

from .Validators import (
    JoinableGuildListValidator,
    JoinableChannelListValidator
)
from .CLICompleter import CLICompleter
from discord import Color, errors

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.rule import Rule
from rich.syntax import Syntax
from rich import box

import asyncio
import re
from io import StringIO

from .Config import ConfigManager
from .ChatCommands import ChatCommands as CMD


BANNER = """
 ____  _          _ _
|  _ \\(_)___  ___| (_)_ __  _   _
| | | | / __|/ __| | | '_ \\| | | |
| |_| | \\__ \\ (__| | | |_) | |_| |
|____/|_|___/\\___|_|_| .__/ \\__, |
                      |_|    |___/"""


class CLI(Observer):
    def __init__(self):
        Observer.__init__(self)
        self.client = DiscordClient(self)
        self.console = Console()
        self._in_chat_mode = False
        self._completer = None

        self.config = ConfigManager()
        self.current_guild = None
        self.current_channel = None
        self.channel_open = False
        self.logged_in = False

        self._unread_counts = {}   # {channel_id: int}
        self._session = None       # PromptSession ref for toolbar invalidation

    def _print(self, *args, **kwargs):
        if self._in_chat_mode:
            buf = StringIO()
            tmp = Console(
                file=buf, force_terminal=True,
                width=self.console.width)
            tmp.print(*args, **kwargs)
            text = buf.getvalue()
            if text.strip():
                print_formatted_text(ANSI(text.rstrip('\n')))
        else:
            self.console.print(*args, **kwargs)

    def _bottom_toolbar(self):
        unread = {cid: count for cid, count in self._unread_counts.items()
                  if count > 0}
        if not unread or not self.current_guild:
            return FormattedText([
                ('bg:#1a1a2e #888888', ' No unread messages ')
            ])

        parts = []
        for channel in self.current_guild.text_channels:
            count = unread.get(channel.id)
            if count:
                if parts:
                    parts.append(('bg:#1a1a2e #888888', ' · '))
                parts.append(('bg:#1a1a2e #ffcc00 bold',
                              f' #{channel.name} ({count}) '))
        return FormattedText(parts) if parts else FormattedText([
            ('bg:#1a1a2e #888888', ' No unread messages ')
        ])

    def start(self):
        self.console.clear()
        self.console.print(Panel(
            Text(BANNER, style="bold cyan", justify="center"),
            subtitle="[dim]Discord in your terminal[/]",
            border_style="cyan",
        ))
        self.console.print()

        if self.config.has_token():
            token = self.config.get_token()
        else:
            self.console.print(
                "[bold yellow]Enter your bot token to get started.[/]")
            self.console.print(
                "[dim]Create a bot at https://discord.com/developers/applications[/]")
            self.console.print()
            token = prompt('Token: ', is_password=True)
            self.config.set_token(token)

        self.console.print("[dim]Connecting to Discord...[/]")
        self.client.run(token)

    def display_guilds(self):
        table = Table(
            title="Servers",
            box=box.ROUNDED,
            title_style="bold white",
            border_style="cyan",
            header_style="bold cyan",
        )
        table.add_column("#", style="bold yellow", width=4)
        table.add_column("Server", style="white")
        table.add_column("Members", style="dim", justify="right")

        for i, guild in enumerate(self.client.guilds):
            table.add_row(str(i), guild.name, str(guild.member_count))

        self._print(table)

    async def select_guild(self):
        self._print()
        self._print("[bold]Select a server by entering its number:[/]")
        session = PromptSession()
        selection = await session.prompt_async(
            '› ',
            validator=JoinableGuildListValidator(len(self.client.guilds))
        )
        self.current_guild = self.client.guilds[int(selection)]
        self._print(
            f"[bold green]Connected to[/] [bold]{self.current_guild.name}[/]")

    def display_channels(self):
        if not self.current_guild:
            return

        table = Table(
            title=f"Channels in {self.current_guild.name}",
            box=box.ROUNDED,
            title_style="bold white",
            border_style="cyan",
            header_style="bold cyan",
        )
        table.add_column("Channel", style="white")
        table.add_column("Topic", style="dim", max_width=50)

        for channel in self.current_guild.text_channels:
            perms = channel.permissions_for(self.current_guild.me)
            if perms.view_channel:
                topic = (channel.topic or "")[:50]
                table.add_row(f"#{channel.name}", topic)

        self._print(table)

    async def select_channel(self):
        if not self.current_guild:
            return

        text_channels = self.current_guild.text_channels
        self._print()
        self._print(
            "[bold]Select a channel by entering #channel-name:[/]")

        completer = WordCompleter(
            ['#' + t.name for t in text_channels],
            ignore_case=True,
            sentence=True,
        )
        session = PromptSession()
        selection = await session.prompt_async(
            '› ',
            validator=JoinableChannelListValidator(text_channels),
            completer=completer,
        )

        for channel in text_channels:
            if selection[1:] == channel.name:
                self.current_channel = channel
                break

    async def open_channel(self):
        self.console.clear()
        self._print(Rule(
            f"[bold]#{self.current_channel.name}[/] in "
            f"[cyan]{self.current_guild.name}[/]",
            style="green",
        ))
        self._print()
        self._unread_counts[self.current_channel.id] = 0
        self.client.emit('open_channel', self.current_channel)
        self.channel_open = True
        await self.channel_loop()

    async def channel_loop(self):
        if not self.current_channel:
            return

        guild_emojis = [str(e) for e in self.current_guild.emojis]
        self._completer = CLICompleter(guild_emojis, self.current_guild)
        session = PromptSession(
            completer=self._completer, erase_when_done=True,
            bottom_toolbar=self._bottom_toolbar)
        self._session = session

        with patch_stdout():
            self._in_chat_mode = True
            while True:
                try:
                    channel_name = (f'#{self.current_channel.name} '
                                    if self.current_channel else '')
                    msg = await session.prompt_async(f'{channel_name}› ')
                except (EOFError, KeyboardInterrupt):
                    self._in_chat_mode = False
                    await self.client.close()
                    return

                if not msg or re.match(r'^\s*$', msg):
                    continue

                if msg.startswith(CMD.PREFIX):
                    await self.handle_commands(msg)
                elif self.current_channel:
                    await self.send_message(msg)
                else:
                    self._print(
                        "[yellow]No channel selected. "
                        "Use /join_channel #channel-name[/]")

            self._in_chat_mode = False

    async def send_message(self, msg):
        # convert #channel-name to <#channel_id>
        channel_names = re.findall(r'#(\S+)', msg)
        for msg_c in channel_names:
            for ch in self.current_guild.channels:
                if msg_c == ch.name:
                    msg = msg.replace(
                        '#' + msg_c, '<#%s>' % str(ch.id))

        # convert @name to <@id>
        try:
            names = [n.strip()
                     for n in re.findall(r'@([^@]{2,32})', msg)]
            for m in self.current_guild.members:
                if m.display_name in names:
                    msg = msg.replace(
                        '@' + m.display_name,
                        '<@' + str(m.id) + '>')
            await self.current_channel.send(msg)
        except errors.Forbidden:
            self._print(
                "[bold red]You do not have permission to send "
                "messages in this channel.[/]")

    async def handle_commands(self, msg):
        if CMD.HELP.match(msg):
            cmds = CMD.get_command_list()
            table = Table(
                title="Commands",
                box=box.SIMPLE,
                border_style="cyan",
                header_style="bold cyan",
            )
            table.add_column("Command", style="bold yellow")
            for cmd in cmds:
                table.add_row(cmd)
            self._print(table)

        elif CMD.LIST_SERVERS.match(msg):
            self.display_guilds()

        elif CMD.JOIN_SERVER.match(msg):
            try:
                guild_n = int(CMD.JOIN_SERVER.match(msg).group(1))
                self.current_guild = self.client.guilds[guild_n]
                self._print(
                    f"[bold green]Switched to[/] "
                    f"[bold]{self.current_guild.name}[/]")
                self.display_channels()
                self.current_channel = None

                # update completer for new guild
                if self._completer:
                    self._completer.guild = self.current_guild
                    self._completer.channels = (
                        self.current_guild.text_channels)
                    self._completer.guild_emojis = [
                        str(e) for e in self.current_guild.emojis]

                self._print(
                    "[dim]Select a channel with "
                    "/join_channel #channel-name[/]")
            except (ValueError, IndexError):
                self._print(
                    "[bold red]Invalid server index.[/] "
                    "Use /list_servers to see available servers.")

        elif CMD.LIST_CHANNELS.match(msg):
            self.display_channels()

        elif CMD.JOIN_CHANNEL.match(msg):
            selected_channel = CMD.JOIN_CHANNEL.match(msg).group(1)
            text_channels = self.current_guild.text_channels

            found = False
            for channel in text_channels:
                if selected_channel == channel.name:
                    self.current_channel = channel
                    found = True
                    break

            if found:
                self._unread_counts[self.current_channel.id] = 0
                self._print()
                self._print(Rule(
                    f"[bold]#{self.current_channel.name}[/] in "
                    f"[cyan]{self.current_guild.name}[/]",
                    style="green",
                ))
                self._print()
                self.client.emit('open_channel', self.current_channel)
            else:
                self._print(
                    f"[bold red]#{selected_channel} does not exist.[/]")

        elif CMD.SHOW_PINS.match(msg):
            pins = await self.current_channel.pins()
            if pins:
                self._print(Rule("Pinned Messages", style="yellow"))
                for message in pins[::-1]:
                    self.__print_message(message)
            else:
                self._print("[dim]No pinned messages.[/]")

        else:
            self._print(
                f'[bold red]Unknown command:[/] {msg}\n'
                f'[dim]Use /help for available commands.[/]')

    def __format_timestamp(self, dt):
        if dt:
            return dt.strftime("%H:%M")
        return ""

    def __print_message(self, msg):
        color = (msg.author.color
                 if msg.author.color != Color.default()
                 else Color.from_rgb(200, 200, 200))
        hex_color = str(color)

        timestamp = self.__format_timestamp(msg.created_at)
        author = msg.author.display_name
        content = msg.clean_content

        # split on code blocks to handle them separately
        parts = re.split(r'(```[\S\s]*?```)', content)

        text = Text()
        text.append(f" {timestamp} ", style="dim")
        text.append(f"{author}", style=f"bold {hex_color}")
        text.append(" > ", style="dim")

        has_code_block = False
        for part in parts:
            if part.startswith('```') and part.endswith('```'):
                has_code_block = True
                # print any text accumulated so far
                if text.plain.strip():
                    self._print(text)
                    text = Text()

                # parse and render code block
                code = part.strip('`')
                lines = code.split('\n')
                if len(lines) > 1:
                    lang = lines[0].strip()
                    code = '\n'.join(lines[1:])
                else:
                    lang = ''
                    code = lines[0] if lines else ''

                if code.strip():
                    try:
                        syntax = Syntax(
                            code, lang or "text",
                            theme="monokai", padding=(0, 1))
                        self._print(syntax)
                    except Exception:
                        self._print(f"[dim]{code}[/]")
            else:
                text.append(part)

        # add attachment urls
        for att in msg.attachments:
            text.append(f"\n  {att.url}", style="underline blue")

        # highlight @mentions
        if msg.mention_everyone or self.client.user in msg.mentions:
            text.stylize("on dark_orange")

        if msg.edited_at:
            text.append(" (edited)", style="dim italic")

        if text.plain.strip():
            self._print(text)

        # display embeds
        for embed in msg.embeds:
            self.__print_embed(embed)

    def __print_embed(self, embed):
        parts = []

        if embed.author and embed.author.name:
            parts.append(f"[bold]{embed.author.name}[/]")
        if embed.title:
            parts.append(f"[bold]{embed.title}[/]")
        if embed.description:
            parts.append(embed.description)
        for field in embed.fields:
            parts.append(f"[bold]{field.name}[/]\n{field.value}")
        if embed.video and embed.video.url:
            parts.append(embed.video.url)
        if embed.image:
            url = embed.image.proxy_url or embed.image.url
            if url:
                parts.append(url)
        if embed.footer and embed.footer.text:
            parts.append(f"[dim]{embed.footer.text}[/]")

        if parts:
            border_color = str(embed.colour) if embed.colour else "blue"
            self._print(Panel(
                "\n".join(parts),
                border_style=border_color,
                padding=(0, 1),
            ))

    def update(self, action, data=None):
        if action == 'login_successful':
            if not self.logged_in:
                self.logged_in = True
                asyncio.ensure_future(self._main_ui())

        elif action == 'message_edit':
            if (self.current_channel
                    and data.channel.id == self.current_channel.id):
                self.client.emit('open_channel', self.current_channel)

        elif action == 'pinged':
            if (self.current_channel
                    and self.current_channel.id != data.channel.id):
                self._print(Panel(
                    f"[bold]@{data.author.display_name}[/] mentioned "
                    f"you in [cyan]{data.guild.name}[/] | "
                    f"[green]#{data.channel.name}[/]",
                    border_style="dark_orange",
                    padding=(0, 1),
                ))

        elif action == 'message':
            msg = data
            if (self.current_channel
                    and self.current_channel.id == msg.channel.id
                    and self.channel_open):
                self.__print_message(msg)
            elif (self.current_guild
                    and msg.guild
                    and msg.guild.id == self.current_guild.id
                    and msg.author != self.client.user
                    and self.channel_open):
                cid = msg.channel.id
                prev = self._unread_counts.get(cid, 0)
                self._unread_counts[cid] = prev + 1
                if prev == 0:
                    self._print(Rule(
                        f"[bold yellow]#{msg.channel.name}[/] · new activity",
                        style="dim yellow",
                    ))
                if self._session and self._session.app:
                    self._session.app.invalidate()

    async def _main_ui(self):
        self.console.clear()
        self.console.print(Panel(
            Text(BANNER, style="bold cyan", justify="center"),
            subtitle="[dim]Discord in your terminal[/]",
            border_style="cyan",
        ))
        self.console.print(
            f"[bold green]Logged in as[/] "
            f"[bold]{self.client.user.name}[/]")
        self.console.print()

        self.display_guilds()
        await self.select_guild()
        self.console.print()
        self.display_channels()
        await self.select_channel()
        await self.open_channel()
