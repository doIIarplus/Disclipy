from prompt_toolkit.validation import Validator, ValidationError


class JoinableGuildListValidator(Validator):
    def __init__(self, guild_length):
        Validator.__init__(self)
        self.guild_length = guild_length

    def validate(self, document):
        text = document.text

        if not text.isdigit() or not int(text) in range(self.guild_length):
            raise ValidationError(
                message='Selection invalid. Please enter a valid number ranging from 0 to {0}'.format(
                    self.guild_length - 1))


class JoinableChannelListValidator(Validator):
    def __init__(self, text_channels):
        Validator.__init__(self)
        self.text_channels = text_channels

    def validate(self, document):
        text = document.text
        text_channels = ['#' + t.name for t in self.text_channels]
        if text not in text_channels:
            raise ValidationError(
                message='Invalid channel. Please enter a valid channel name')
