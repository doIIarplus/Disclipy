from .observer import Subject
import http.client
import json
import discord
import configparser


class DiscordClient(discord.Client, Subject):
    def __init__(self, cli, config_file):
        discord.Client.__init__(self)
        Subject.__init__(self)

        self.config_file = config_file
        self.config = configparser.ConfigParser(allow_no_value=True)
        self.config.read(config_file)
        print(self.config)

        self.attach(cli)

    async def on_ready(self):
        self.notify('login_successful')
        self.logged_in = True

    async def on_message(self, message):
        self.notify(message)

    def __get_token(self, email: str, password: str):
        """Returns a Discord user token.

        Args:
            email: your Discord email used to login
            password: the password associated with your Discord email

        Returns:
            dict containing:
                {
                    'token': str,
                    'incorrect_email_format': bool,
                    'incorrect_password': bool,
                    'captcha_required': bool
                }
        """
        conn = http.client.HTTPSConnection('discordapp.com')

        payload = json.dumps({
            "captcha_key": None,
            "email": email,
            "password": password,
            "undelete": False
        })

        headers = {'content-type': 'application/json'}

        conn.request('POST', '/api/v6/auth/login', payload, headers)

        res = conn.getresponse()
        data = json.loads(res.read())

        ret = {
            'token': '',
            'incorrect_email_format': False,
            'incorrect_password': False,
            'captcha_required': False
        }

        # Possible responses:
        #    1 - {'token': 'thetokenstring'}
        #    2 - {'password': ['Password does not match.']}
        #    3 - {'captcha_key': ['captcha-required']}
        #    4 - {'email': ['Not a well formed email address.']}
        # 1 & 2 only return if the user has bypassed the captcha
        # 3 returns if the user has not bypassed the captcha or if the user does not exist
        # 4 returns if an incorrect email format is passed
        if 'token' in data:
            ret['token'] = data['token']
        elif 'email' in data:
            ret['incorrect_email_format'] = True
        elif 'password' in data:
            ret['incorrect_password'] = True
        elif 'captcha_key' in data:
            ret['captcha_required'] = True

        return ret

    def login_with_email_password(self, email, password):
        res = self.__get_token(email, password)

        if res['token']:
            self.notify('login_in_progress')
            self.session_token = res['token']
            self.run(res['token'], bot=False)
        elif res['incorrect_email_format']:
            self.notify('login_incorrect_email_format')
        elif res['incorrect_password']:
            self.notify('login_incorrect_password')
        elif res['captcha_required']:
            self.notify('login_captcha_required')
