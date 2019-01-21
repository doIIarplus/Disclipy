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
import os.path
import configparser

from prompt_toolkit import prompt
from src import DiscordClient
from src import CLI
from src.Config import *
from getpass import getpass

if __name__ == '__main__':
    # Load config
    config = configparser.ConfigParser(allow_no_value=True)
    if not os.path.isfile(CONFIG_FILE):
        config['Credentials'] = {
            "Token": DEFAULT_TOKEN,
            "AutoLogin": '',
        }
        with open(CONFIG_FILE, 'w+') as file:
            config.write(file)
    else:
        config.read(CONFIG_FILE)

    cli = CLI(config)
    cli.login()

    # while True:
    #user_input = prompt('>')
    # print(user_input)

    # Select Server

    # Select Channel
