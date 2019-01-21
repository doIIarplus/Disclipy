from .DiscordClient import DiscordClient
from .observer import Observer
from getpass import getpass

from prompt_toolkit import prompt
import click

class CLI(Observer):
	def __init__(self):
		Observer.__init__(self)
		self.client = DiscordClient(self)
		click.clear()

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
			self.display_guilds()
			print('Select a server by entering the corresponding server number')
			self.select_guild(prompt('>'))
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

	def display_guilds(self):
		for i, guild in enumerate(self.client.guilds):
			print("{0}: {1}".format(i, guild.name))

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

