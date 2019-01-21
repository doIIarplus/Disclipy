"""
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter

if __name__ == '__main__':
    AutoCompleter = WordCompleter(['abcde', 'bcdef', 'cdefg', 'defgh'],
                                  ignore_case=True)

    while True:
        user_input = prompt('Discord>',
                            history=FileHistory('history.txt'),
                            auto_suggest=AutoSuggestFromHistory(),
                            completer=AutoCompleter,
                            )
        print(user_input)
"""
from prompt_toolkit import prompt
from src import DiscordClient
from src import CLI

from getpass import getpass

if __name__ == '__main__':
    cli = CLI()
    cli.login()

    # while True:
    #user_input = prompt('>')
    # print(user_input)

    # Select Server

    # Select Channel
