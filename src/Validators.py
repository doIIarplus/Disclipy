from prompt_toolkit.validation import Validator, ValidationError

class JoinableGuildListValidator(Validator):
	def __init__(self, guildLength):
		pass