import os.path
import configparser


class Sections:
    CREDENTIALS = 'Credentials'


class Keys:
    TOKEN = 'Token'
    ACCOUNT_TYPE = 'AccountType'


class ConfigManager:
    def __init__(self):
        self.filename = 'config.ini'

        self.config = configparser.ConfigParser(allow_no_value=True)
        if not os.path.isfile(self.filename):
            self.config[Sections.CREDENTIALS] = {
                Keys.TOKEN: '',
                Keys.ACCOUNT_TYPE: 'bot',
            }
            with open(self.filename, 'w') as file:
                self.config.write(file)
        else:
            self.config.read(self.filename)

    def has_token(self):
        token = self.config[Sections.CREDENTIALS][Keys.TOKEN]
        return bool(token and token.strip())

    def set_token(self, token):
        self.config[Sections.CREDENTIALS][Keys.TOKEN] = token
        self.save()

    def get_token(self):
        return self.config[Sections.CREDENTIALS][Keys.TOKEN]

    def get_account_type(self):
        try:
            return self.config[Sections.CREDENTIALS][Keys.ACCOUNT_TYPE]
        except KeyError:
            return 'bot'

    def set_account_type(self, account_type):
        self.config[Sections.CREDENTIALS][Keys.ACCOUNT_TYPE] = account_type
        self.save()

    def is_bot(self):
        return self.get_account_type() == 'bot'

    def save(self):
        with open(self.filename, 'w') as f:
            self.config.write(f)
