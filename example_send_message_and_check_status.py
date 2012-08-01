# -*- coding: utf-8 -*-

import pdb

import sys as mod_sys
import logging as mod_logging
import time as mod_time

import oneapi as mod_oneapi
import oneapi.models as mod_models
import oneapi.dummyserver as mod_dummyserver

mod_logging.basicConfig(level=mod_logging.DEBUG, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

if len(mod_sys.argv) < 2:
    print 'Please enter username, password and your public ip address'
    mod_sys.exit(1)

username = mod_sys.argv[1]
password = mod_sys.argv[2]

sms_client = mod_oneapi.SmsClient(username, password)

sms = mod_models.SMSRequest()
sms.sender_address = '38598854702'
sms.address = '38598854702'
sms.message = 'Test message'
sms.callback_data = 'Any string'

result = sms_client.send_sms(sms)

if not result.is_success():
    print 'Error sending message:', result.exception
    mod_sys.exit(1)

print result
print 'Is success = ', result.is_success()
print 'Client correlator = ', result.client_correlator

# Few seconds later we can check for the sending status
mod_time.sleep(10)

query_status = sms_client.query_delivery_status(result.client_correlator)
print query_status.delivery_info[0].delivery_status
