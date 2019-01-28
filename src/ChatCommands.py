from prompt_toolkit import print_formatted_text, HTML
from xml.sax.saxutils import escape
import re


class Command():
    def __init__(self, prefix, cmd_description, pattern=''):
        self.description = prefix + cmd_description
        if pattern:
            self.pattern = re.compile(prefix + pattern)
        else:
            self.pattern = re.compile(self.description + '$')

    def match(self, string):
        return self.pattern.match(string)

    def __str__(self):
        return self.description

    def __repr__(self):
        return self.description


class ChatCommands:
    PREFIX = '/'
    HELP = Command(PREFIX, 'help')
    LIST_SERVERS = Command(
        PREFIX,
        'list_servers - lists your joinable servers.',
        'list_servers$')
    JOIN_SERVER = Command(
        PREFIX,
        'join_server <server index>',
        r'join_server \s*([0-9]+)\s*$')
    LIST_CHANNELS = Command(
        PREFIX,
        'list_channels - lists the joinable channels in the current joined server.',
        'list_channels$')
    JOIN_CHANNEL = Command(PREFIX, 'join_channel #<server-name>', 'join_channel #(.*)$')

    SHOW_PINS = Command(PREFIX, 'show_pins - shows pinned messages', 'show_pins$')

    __commands = [
        LIST_SERVERS,
        JOIN_SERVER,
        LIST_CHANNELS,
        JOIN_CHANNEL,
        SHOW_PINS
    ]

    @staticmethod
    def get_command_list(include_help=False):
        cmd_list = [str(cmd) for cmd in ChatCommands.__commands]
        if include_help:
            cmd_list.insert(0, str(ChatCommands.HELP))
        return cmd_list

    @staticmethod
    def print(text):
        print_formatted_text(
            HTML('<_ fg="#000000" bg="#ffffff">%s</_>' % (
                escape(text)
            ))
        )
