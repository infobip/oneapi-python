"""
Example basic authorization WITHOUT the library.
"""
import json
import urllib2
import requests
import base64

username = 'your_username_here'
password = 'your_password_here'

# Base64 encode username:password:
basic_authorization_string = base64.encodestring(username + ':' + password)

# Some base64 algorithms leave a newline at the end of the string, you need to remove it:
basic_authorization_string = basic_authorization_string.strip()

# Send any API request:
req = urllib2.Request(
        'http://api.parseco.com/1/customerProfile',
        headers={'Authorization': 'Basic ' + basic_authorization_string})

# Read and process the response:
result_json = urllib2.urlopen(req).read()

print result_json
