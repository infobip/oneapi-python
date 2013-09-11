# -*- coding: utf-8 -*-

import pdb

import sys as sys
import logging as logging
import time as time

import oneapi as oneapi
import oneapi.models as models
import oneapi.dummyserver as dummyserver

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

if len(sys.argv) < 5:
    print 'Please enter username, password, dest, source, content-type (url|json) [accept-type]'
    sys.exit(1)

username = sys.argv[1]
password = sys.argv[2]
address = sys.argv[3]
data_format = sys.argv[4]

if len(sys.argv) == 6:
   accept = sys.argv[5]

if data_format != "json":
   data_format = "url"

# example:initialize-sms-client
sms_client = oneapi.SmsClient(username, password)
# ----------------------------------------------------------------------------------------------------

# example:prepare-message-without-notify-url
sms = models.SMSRequest()
sms.address = address
sms.notify_url = 'Any URL'
sms.callback_data = 'Any string'
sms.filter_criteria = "Urgent"
# ----------------------------------------------------------------------------------------------------

header=None
if 'accept' in locals():
   header = {"accept" : accept}

# example:send-message
result = sms_client.subscribe_messages_sent_notification(sms, header, data_format)
# store client correlator because we can later query for the delivery status with it:
resource_url = result.resource_url
# ----------------------------------------------------------------------------------------------------

if not result.is_success():
    print 'Error sending message:', result.exception
    sys.exit(1)

print 'Is success = ', result.is_success()
print 'Resource URL = ', result.resource_url

#Few seconds later we can delete the subscription
time.sleep(10)

sms_client.delete_messages_sent_subscription(resource_url, header, data_format)
# ----------------------------------------------------------------------------------------------------
