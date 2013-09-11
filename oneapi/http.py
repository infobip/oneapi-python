# -*- coding: utf-8 -*-

import pdb

"""
Note, requests are much better than this
"""
import json as mod_json
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

def add_params(url, urlencoded_params):
    if '?' in url:
        return url + '&' + urlencoded_params
    else:
        return url + '?' + urlencoded_params

def parse_headers(headers):
    result = {}
    if not headers:
        return result
    for header in headers:
        pos = header.find(':')
        if pos > 0:
            result[header[:pos]] = header[pos + 1:].strip()

    return result

def urlencode_params(params):
    if hasattr(params, 'items') or isinstance(params, tuple):
        return mod_urllib.urlencode(params)

    return params

def execute_request(method, url, data=None, headers=None, data_format=None):
    if not method in VALID_METHODS:
        raise Exception('Invalid method %s' % method)

    mod_logging.debug('%s to %s with %s', method, url, data)

    body = None
    opener = mod_urllib2.build_opener(mod_urllib2.HTTPHandler)
    if data:
        if method in PARAMS_IN_BODY_METHODS:
            if data_format == "json":
                body = mod_json.JSONEncoder().encode(data)
            else:
                body = urlencode_params(data)
        else:
            url = add_params(url, urlencode_params(data))

    request = CustomRequest(method, url)

    if data_format == "json":
        headers["content-type"] = "application/json"

    if headers:
        mod_logging.debug('Headers: %s', headers)
        for key, value in headers.items():
            request.add_header(key, value)

    try:
        url = opener.open(request, data=body)

        http_code = url.getcode()
        headers = headers
        body = url.read()
    except Exception, e:
        if hasattr(e, 'code'):
            http_code = e.code
        else:
            # Withoud http code => non-http exception:
            raise e

        if hasattr(e, 'headers'):
            headers = {}
            for key, value in e.headers.items():
                headers[key] = value

        if hasattr(e, 'read'):
            body = e.read()
    finally:
        try:
            url.close()
        except Exception, ignore:
            pass

    mod_logging.debug('http response code:%s', http_code)
    mod_logging.debug('http response headers:%s', headers)
    mod_logging.debug('http response body:%s', body)

    return CustomHttpResponse(http_code, headers, body)

def execute_GET(url, data=None, headers=None):
    return execute_request('GET', url, data=data, headers=headers)

def execute_POST(url, data=None, headers=None, data_format=None):
    return execute_request('POST', url, data=data, headers=headers, data_format=data_format)

def execute_PUT(url, data=None, headers=None):
    return execute_request('PUT', url, data=data, headers=headers)

def execute_DELETE(url, data=None, headers=None):
    return execute_request('DELETE', url, data=data, headers=headers)

if __name__ == '__main__':
    #print execute_GET('http://localhost', {'a': 'šđčćž/(/(/('})
    print execute_GET('https://oneapi.infobip.com/status', {'a': 'šđčćž/(/(/('})
