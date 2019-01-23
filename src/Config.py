import os.path
import configparser


class Sections:
    CREDENTIALS = 'Credentials'


class Keys:
    # credentials
    TOKEN = 'Token'
    AUTOLOGIN = 'AutoLogin'
    FIRSTTIME = 'FirstTime'


class ConfigManager:
    def __init__(self):
        self.filename = 'config.ini'

        # Load config
        self.config = configparser.ConfigParser(allow_no_value=True)
        if not os.path.isfile(self.filename):
            self.config[Sections.CREDENTIALS] = {
                Keys.TOKEN: '',
                Keys.AUTOLOGIN: 'False',
                Keys.FIRSTTIME: 'True'
            }
            with open(self.filename, 'w') as file:
                self.config.write(file)
        else:
            self.config.read(self.filename)

    def first_time(self):
        first = self.config[Sections.CREDENTIALS][Keys.FIRSTTIME] == 'True'
        if first:
            self.config[Sections.CREDENTIALS][Keys.FIRSTTIME] = 'False'
        return first

    def enable_auto_login(self, token=''):
        c = self.config[Sections.CREDENTIALS]
        c[Keys.AUTOLOGIN] = 'True'
        c[Keys.TOKEN] = token
        self.save()

    def auto_login_enabled(self):
        c = self.config[Sections.CREDENTIALS]
        return c[Keys.AUTOLOGIN] == 'True' and c[Keys.TOKEN]

    def set_token(self, token):
        if self.config[Sections.CREDENTIALS][Keys.AUTOLOGIN] == 'True':
            self.config[Sections.CREDENTIALS][Keys.TOKEN] = token
        self.save()

    def get_token(self):
        return self.config[Sections.CREDENTIALS][Keys.TOKEN]

    def save(self):
        with open(self.filename, 'w') as f:
            self.config.write(f)
