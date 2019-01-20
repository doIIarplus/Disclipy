from .DiscordClient import DiscordClient
from .observer import Observer

class CLI(Observer):
	def __init__(self):
		Observer.__init__(self)
		self.client = DiscordClient(self)

	def update(self, action):
		# TODO implement functionality

		print(action)

		# login actions
		if action == 'login_successful':
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