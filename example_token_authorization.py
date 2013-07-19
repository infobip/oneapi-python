"""
Example token-based authorization WITHOUT the library.
"""
import json
import urllib2
import requests
import base64

username = 'your_username_here'
password = 'your_password_here'

# Request a API token by sending a /login POST request:
authentication_request_json_body = '{"username":"%s", "password":"%s"}' % (username, password)
req = urllib2.Request(
        'https://oneapi.infobip.com/1/customerProfile/login',
        data = authentication_request_json_body)

result_json = urllib2.urlopen(req).read()

# The result comes in the following format:
# {"login":{"verified":true,"ibAuthCookie":"<your_secret_token>"}}

# Retrieve the token:
result_json = json.loads(result_json)
token = result_json['login']['ibAuthCookie']

# Now use this token when calling the API for all other methods:
req = urllib2.Request(
        'http://oneapi.infobip.com/1/customerProfile',
        headers={'Authorization': 'IBSSO ' + token})

result_json = urllib2.urlopen(req).read()

print result_json
