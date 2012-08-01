import pdb

import sys as mod_sys
import logging as mod_logging

import oneapi as mod_oneapi
import oneapi.models as mod_models
import oneapi.dummyserver as mod_dummyserver

mod_logging.basicConfig(level=mod_logging.DEBUG, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

if len(mod_sys.argv) < 2:
    print 'Please enter username and password'
    mod_sys.exit(1)

username = mod_sys.argv[1]
password = mod_sys.argv[2]

sms_client = mod_oneapi.SmsClient(username, password)

result = sms_client.retrieve_inbound_messages()
