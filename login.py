import http.client
import getpass
import json


def get_token(email: str, password: str):
    """Returns a Discord user token.

    Args:
        email: your Discord email used to login
        password: the password associated with your Discord email

    Returns:
        dict containing:
            {
                'token': str,
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
