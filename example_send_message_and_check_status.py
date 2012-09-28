# -*- coding: utf-8 -*-

import pdb

import sys as sys
import logging as logging
import time as time

import oneapi as oneapi
import oneapi.models as models
import oneapi.dummyserver as dummyserver

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

if len(sys.argv) < 4:
    print 'Please enter username, password and address'
    sys.exit(1)

username = sys.argv[1]
password = sys.argv[2]
address = sys.argv[3]

# example:initialize-sms-client
sms_client = oneapi.SmsClient(username, password)
# ----------------------------------------------------------------------------------------------------

# example:prepare-message-without-notify-url
sms = models.SMSRequest()
sms.sender_address = address
sms.address = address
sms.message = 'Test message'
sms.callback_data = 'Any string'
# ----------------------------------------------------------------------------------------------------

# example:send-message
result = sms_client.send_sms(sms)
# store client correlator because we can later query for the delivery status with it:
client_correlator = result.client_correlator
# ----------------------------------------------------------------------------------------------------

if not result.is_success():
    print 'Error sending message:', result.exception
    sys.exit(1)

print result
print 'Is success = ', result.is_success()
print 'Client correlator = ', result.client_correlator

# Few seconds later we can check for the sending status
time.sleep(10)

# example:query-for-delivery-status
query_status = sms_client.query_delivery_status(client_correlator)
delivery_status = query_status.delivery_info[0].delivery_status
# ----------------------------------------------------------------------------------------------------
