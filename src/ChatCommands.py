from prompt_toolkit import print_formatted_text, HTML
import re


class Command():
    def __init__(self, prefix, cmd_description, pattern=''):
        self.description = prefix + cmd_description
        if pattern:
            self.pattern = re.compile(pattern)
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
    LIST_GUILDS = Command(PREFIX, 'list_guilds')
    LIST_CHANNELS = Command(PREFIX, 'list_channels')

    __commands = [
        LIST_GUILDS,
        LIST_CHANNELS
    ]

    @staticmethod
    def get_command_list():
        return [str(cmd) for cmd in ChatCommands.__commands]

    @staticmethod
    def print(text):
        print_formatted_text(
            HTML('<_ fg="#000000" bg="#ffffff">%s</_>' % (
                text
            ))
        )
