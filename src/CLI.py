from .DiscordClient import DiscordClient
from .observer import Observer
from getpass import getpass

from prompt_toolkit import prompt
import click

class CLI(Observer):
	def __init__(self):
		Observer.__init__(self)
		self.client = DiscordClient(self)

	def login(self):
		self.client.login_with_email_password(
			prompt('Email: '),
			prompt('Password: ', is_password=True))

	def update(self, action):
		# TODO implement functionality

		print(action)

		# login actions
		if action == 'login_successful':
			click.clear()
			pass
		elif action == 'login_incorrect_email_format':
			# prompt user to enter correct email format
			pass
		elif action == 'login_incorrect_password':
			# prompt user to enter correct password
			pass
		elif action == 'login_captcha_required':
			# prompt user to log into Discord's Web client first
			pass