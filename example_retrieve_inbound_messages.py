import pdb

import sys as sys
import logging as logging

import oneapi as oneapi
import oneapi.models as models
import oneapi.dummyserver as dummyserver

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

if len(sys.argv) < 2:
    print 'Please enter username and password'
    sys.exit(1)

username = sys.argv[1]
password = sys.argv[2]

sms_client = oneapi.SmsClient(username, password)

# example:retrieve-inbound-messages
result = sms_client.retrieve_inbound_messages()
# ----------------------------------------------------------------------------------------------------
