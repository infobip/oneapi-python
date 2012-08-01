# -*- coding: utf-8 -*-

import sys as mod_sys
import logging as mod_logging

import oneapi as mod_oneapi
import oneapi.models as mod_models
import oneapi.dummyserver as mod_dummyserver

mod_logging.basicConfig(level=mod_logging.DEBUG, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

username = mod_sys.argv[1]
password = mod_sys.argv[2]

sms_client = mod_oneapi.SmsClient(username, password);

data_connection_client = mod_oneapi.DataConnectionProfileClient(username, 'wrongpassword');

print 'sms_client validity is ', sms_client.is_valid()
print 'data_connection_client validity is ', data_connection_client.is_valid()

assert sms_client.is_valid()
assert not data_connection_client.is_valid()
