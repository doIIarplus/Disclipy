from .DiscordClient import DiscordClient
from .observer import Observer
from getpass import getpass

from prompt_toolkit import prompt, print_formatted_text
from prompt_toolkit.styles import Style
from prompt_toolkit.styles.pygments import style_from_pygments_cls
from pygments.styles import get_style_by_name
from .Validators import (
    JoinableGuildListValidator,
    JoinableChannelListValidator
)
import click


class CLI(Observer):
    def __init__(self, config_file):
        Observer.__init__(self)
        self.client = DiscordClient(self, config_file)
        click.clear()

        self.current_guild = None
        self.current_channel = None


    def login(self):
        # Check config file for setup status
        if self.client.config['CREDENTIALS']['Token'] == 'placeholder_token':
            email = prompt('Email: ')
            password = prompt('Password: ', is_password=True)

            if not self.client.config['CREDENTIALS']['AutoLogin']:
                auto_login = prompt('Automatically login in the future? y/n: ')
                while auto_login not in ['y', 'n']:
                    auto_login = prompt('Invalid selection. Please select y/n')

                self.client.login_with_email_password(email, password)

                if auto_login:
                    self.client.config['CREDENTIALS']['AutoLogin'] = 'True'
                    self.client.config['CREDENTIALS']['Token'] = self.client.session_token
                else:
                    self.client.config['CREDENTIALS']['Autologin'] = 'False'

                with open(self.client.config_file, 'w') as configfile:
                    self.client.config.write(configfile)
        else:
            self.client.notify('login_in_progress')
            self.client.run(self.client.config['CREDENTIALS']['Token'], bot=False)


    def update(self, action):
        # login actions
        if action == 'login_in_progress':
            click.echo('Logging in...')
        elif action == 'login_successful':
            click.clear()
            click.secho('You are logged in.', fg='black', bg='white')
            self.display_guilds()
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
        print('Select a server by entering the corresponding server number')
        self.select_guild()

    def select_guild(self):
        selection = int(prompt('>', validator=JoinableGuildListValidator(len(self.client.guilds))))
        self.current_guild = self.client.guilds[int(selection)]
        click.clear()
        click.secho('Connected to {}'.format(self.current_guild.name), fg='black', bg='white')
        self.select_channel()


    def select_channel(self):
        if self.current_guild:
            channels = ''
            text_channels = self.current_guild.text_channels

            for channel in text_channels:
                channels += '#'+channel.name+'\n'

            click.echo_via_pager(channels)
            print('Select a channel by entering the corresponding #channel-name')
            
            selection = prompt('>', validator=JoinableChannelListValidator(text_channels))

            for channel in text_channels:
                if selection[1:] == channel.name:
                    self.current_channel = channel
            
            # open the channel