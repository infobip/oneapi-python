# -*- coding: utf-8 -*-

import sys as sys
import logging as logging

import oneapi as oneapi
import oneapi.models as models
import oneapi.dummyserver as dummyserver

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

username = sys.argv[1]
password = sys.argv[2]

sms_client = oneapi.SmsClient(username, password);

data_connection_client = oneapi.DataConnectionProfileClient(username, 'wrongpassword');

print 'sms_client validity is ', sms_client.is_valid()
print 'data_connection_client validity is ', data_connection_client.is_valid()

assert sms_client.is_valid()
assert not data_connection_client.is_valid()
