# -*- coding: utf-8 -*-

import random as mod_random

def get_random_string(length, chars):
    if not length:
        raise Exception('Invalid random string length: {0}'.format(length))
    if not chars:
        raise Exception('Invalid random chars: {0}'.format(chars))

    result = ''

    for i in range(length):
        result += chars[mod_random.randint(0, len(chars) - 1)]

    return result

def get_random_alphanumeric_string(length=10):
    return get_random_string(length, 'qwertzuiopasdfghjklyxcvbnm123456789')

def get(json_data, path):
    result = json_data
    parts = path.split('.')

    if '|' in path:
        parts = path.split('|')
        for part in parts:
            result = get(json_data, part.strip())
            if result:
                return result
        return None

    for part in parts:
        try:
            part = int(part)
        except:
            pass
        try:
            result = result[part]
        except Exception, e:
            return None

    return result
