from .DiscordClient import DiscordClient
from .observer import Observer
from getpass import getpass

from prompt_toolkit import prompt, print_formatted_text
from prompt_toolkit.styles import Style
from prompt_toolkit.styles.pygments import style_from_pygments_cls
from pygments.styles import get_style_by_name
import click


class CLI(Observer):
    def __init__(self, config):
        Observer.__init__(self)
        self.client = DiscordClient(self, config)
        click.clear()

    def login(self):
        # Check config file for setup status
        email = prompt('Email: ')
        password = prompt('Password: ', is_password=True)
        self.client.login_with_email_password(email, password)

    def update(self, action):
        # login actions
        if action == 'login_in_progress':
            click.echo('Logging in...')
        elif action == 'login_successful':
            click.clear()
            click.secho('You are logged in.', fg='black', bg='white');
            self.display_guilds()
            print('Select a server by entering the corresponding server number')
            self.select_guild(prompt('>'))
        elif action == 'login_incorrect_email_format':
            click.secho('Not a well formed email address.', fg='red', bold=True)
            self.login()
        elif action == 'login_incorrect_password':
            click.secho('Password is incorrect.', fg='red', bold=True)
            self.login()
        elif action == 'login_captcha_required':
            click.secho(
                'Captcha required.\n'+
                'Please login through the Discord web client first.\n'+
                'https://discordapp.com/login', fg='red', bold=True)
            self.login()

    def display_guilds(self):
        guilds = ''
        for i, guild in enumerate(self.client.guilds):
            guilds += '{0}: {1}\n'.format(i, guild.name)
        click.echo_via_pager(guilds)

    def select_guild(self, selection):
        while(
            not str.isdigit(selection) or 
            not int(selection) in range(0, len(self.client.guilds))
        ):
            print('Selection invalid. Please enter a valid number ranging from 0 to {0}'.format(len(self.client.guilds)))
            selection = prompt('>')

        self.current_guild = self.client.guilds[int(selection)]
        click.clear()
        print('Connected to {}'.format(self.current_guild.name))
