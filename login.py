import http.client
import getpass
import json


def get_token(email, password):
    conn = http.client.HTTPSConnection('discordapp.com')

    payload = '{"captcha_key":null, "email": "%s", "password": "%s", "undelete": false}' % (
        email, password)

    headers = {'content-type': 'application/json'}

    conn.request('POST', '/api/v6/auth/login', payload, headers)

    res = conn.getresponse()
    data = res.read()

    return json.loads(data)


print(get_token(input('Enter your email: '), getpass.getpass('Enter your password: ')))
