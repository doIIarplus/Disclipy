import http.client
import getpass

conn = http.client.HTTPSConnection("discordapp.com")
email = input('Enter your email: ')
password = getpass.getpass('Enter your password: ')

payload = "{\n\t\"captcha_key\":null,\n\t\"email\":\""+email+"\",\n\t\"password\": \""+password+"\",\n\t\"undelete\": false\n}"

headers = {
    'content-type': "application/json",
    }

conn.request("POST", "/api/v6/auth/login", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
