# -*- coding: utf-8 -*-

import pdb

import sys as mod_sys
import logging as mod_logging
import time as mod_time

import oneapi as mod_oneapi
import oneapi.models as mod_models
import oneapi.dummyserver as mod_dummyserver

mod_logging.basicConfig(level=mod_logging.DEBUG, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

if len(mod_sys.argv) < 3:
    print 'Please enter username, password and your ip address'
    mod_sys.exit(1)

username = mod_sys.argv[1]
password = mod_sys.argv[2]
public_ip_address = mod_sys.argv[3]
port = 9000

sms_client = mod_oneapi.SmsClient(username, password)

sms = mod_models.SMSRequest()
sms.sender_address = '38598854702'
sms.address = '38598854702'
sms.message = 'Test message'
sms.notify_url = 'http://{0}:{1}'.format(public_ip_address, port)
#sms.callback_data = 

result = sms_client.send_sms(sms)

if not result.is_success():
    print 'Error sending message:', result.exception
    mod_sys.exit(1)

print result
print 'Is success = ', result.is_success()
print 'Client correlator = ', result.client_correlator

# Wait for 30 seconds for push-es
server = mod_dummyserver.DummyWebServer(port)
server.start_wait_and_shutdown(30)

print server.get_requests()
