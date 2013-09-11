# -*- coding: utf-8 -*-

import pdb

import sys as sys
import logging as logging
import time as time

import oneapi as oneapi
import oneapi.models as models
import oneapi.dummyserver as dummyserver

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

if len(sys.argv) < 6:
    print 'Please enter username, password, address, sender, content-type (json|url), [accept-type]'
    sys.exit(1)

username = sys.argv[1]
password = sys.argv[2]
address = sys.argv[3]
sender = sys.argv[4]
data_format = sys.argv[5]

if len(sys.argv) == 7:
    accept = sys.argv[6]

if (data_format != "json"):
    data_format = "url"

# example:initialize-sms-client
sms_client = oneapi.SmsClient(username, password)
# ----------------------------------------------------------------------------------------------------

# example:prepare-message-without-notify-url
sms = models.SMSRequest()
sms.sender_address = sender
sms.address = address
sms.message = 'Test message'
sms.callback_data = 'Any string'
sms.notify_url = 'Any URL'
# ----------------------------------------------------------------------------------------------------

header = None
if 'accept' in locals():
    header = {"accept" : accept}

# example:send-message
result = sms_client.send_sms(sms, header, data_format)
# store client correlator because we can later query for the delivery status with it:
client_correlator = result.client_correlator
# ----------------------------------------------------------------------------------------------------

if not result.is_success():
    print 'Error sending message:', result.exception
    sys.exit(1)

print result
print 'Is success = ', result.is_success()
print 'Sender = ', result.sender
print 'Client correlator = ', result.client_correlator

# Few seconds later we can check for the sending status
time.sleep(10)

# example:query-for-delivery-status
query_status = sms_client.query_delivery_status(client_correlator, sender)
delivery_status = query_status.delivery_info[0].delivery_status
# ----------------------------------------------------------------------------------------------------
