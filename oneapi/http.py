# -*- coding: utf-8 -*-

import pdb

"""
Note, requests are much better than this
"""

import logging as mod_logging
import urllib2 as mod_urllib2
import urllib as mod_urllib
import collections as mod_collections

mod_logging.basicConfig(level=mod_logging.DEBUG, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

VALID_METHODS = ['GET', 'DELETE', 'PUT', 'POST']

# For those methods params will be urlencoded and put in request body:
PARAMS_IN_BODY_METHODS = ['PUT', 'POST']

CustomHttpResponse = mod_collections.namedtuple(
        'CustomHttpResponse',
        ('status_code', 'headers', 'content'))

class CustomRequest(mod_urllib2.Request):

    def __init__(self, method, url, *args1, **args2):
        mod_urllib2.Request.__init__(self, url, *args1, **args2)
        self.method = method

    def get_method(self):
        return self.method

def add_params(url, params):
    if '?' in url:
        return url + '&' + mod_urllib.urlencode(params)
    else:
        return url + '?' + mod_urllib.urlencode(params)

def parse_headers(headers):
    result = {}
    if not headers:
        return result
    for header in headers:
        pos = header.find(':')
        if pos > 0:
            result[header[:pos]] = header[pos + 1:].strip()

    return result

def execute_request(method, url, params=None, body=None, headers=None):
    if not method in VALID_METHODS:
        raise Exception('Invalid method %s' % method)

    mod_logging.debug('%s request to %s', method, url)

    opener = mod_urllib2.build_opener(mod_urllib2.HTTPHandler)
    if params:
        if method in PARAMS_IN_BODY_METHODS:
            if body:
                raise Exception('No http body possible for %s with params (%s)' % (methods, params))
            body = mod_urllib.urlencode(params)
        else:
            url = add_params(url, params)

    request = CustomRequest(method, url)

    if headers:
        for key, value in headers.items():
            request.add_header(key, value)

    url = opener.open(request, data=body)

    http_code = url.getcode()
    headers = parse_headers(url.headers.headers)
    body = url.read()

    mod_logging.debug('http response code:%s', http_code)
    mod_logging.debug('http response headers:%s', headers)
    mod_logging.debug('http response body:%s', body)

    return CustomHttpResponse(http_code, headers, body)

def execute_GET(url, params=None, body=None, headers=None):
    return execute_request('GET', url, params=params, body=body, headers=headers)

def execute_POST(url, params=None, body=None, headers=None):
    return execute_request('POST', url, params=params, body=body, headers=headers)

def execute_PUT(url, params=None, body=None, headers=None):
    return execute_request('PUT', url, params=params, body=body, headers=headers)

def execute_DELETE(url, params=None, body=None):
    return execute_request('DELETE', url, params=params, body=body, headers=headers)

if __name__ == '__main__':
    #print execute_GET('http://localhost', {'a': 'šđčćž/(/(/('})
    print execute_GET('https://api.parseco.com/status', {'a': 'šđčćž/(/(/('})
