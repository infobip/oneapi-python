# -*- coding: utf-8 -*-

import pdb

import sys as mod_sys
import logging as mod_logging
import time as mod_time

import oneapi as mod_oneapi
import oneapi.models as mod_models

mod_logging.basicConfig(level=mod_logging.DEBUG, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

if len(mod_sys.argv) < 2:
    print 'Please enter username and password'
    mod_sys.exit(1)

username = mod_sys.argv[1]
password = mod_sys.argv[2]

sms_client = mod_oneapi.SmsClient(username, password)

sms = mod_models.SMSRequest()
sms.sender_address = '38598854702'
sms.address = '38598854702'
sms.message = 'Test message'
#sms.notify_url = 
#sms.callback_data = 

result = sms_client.send_sms(sms)

if not result.is_success():
    print 'Error sending message:', result.exception
    mod_sys.exit(1)

print result
print 'Is success = ', result.is_success()
print 'Client correlator = ', result.client_correlator

# Wait few seconds for the message to be delivered:
mod_time.sleep(5)

result = sms_client.query_delivery_status(result)

if not result.is_success():
    print 'Error checking message status';
    mod_sys.exit(1)

for delivery_info in result.delivery_info:
    print delivery_info.delivery_status
