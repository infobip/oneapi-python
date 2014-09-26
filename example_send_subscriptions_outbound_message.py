# -*- coding: utf-8 -*-

import pdb
import argparse

import sys as sys
import logging as logging
import time as time

import oneapi as oneapi
import oneapi.models as models
import oneapi.dummyserver as dummyserver

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--server", help="Address of the server (default=https://oneapi.infobip.com)")
parser.add_argument("username", help="Login")
parser.add_argument("password", help="Password")
parser.add_argument("sender", help="From address")
parser.add_argument("-p", "--port", help="local port for delivery notification")
parser.add_argument("-d", "--data_format", help="Type of data used in request, can be url or json (default=url)")
parser.add_argument("-a", "--accept", help="Type of data used for response, can be url or json (default=url)")
args = parser.parse_args()

data_format = "url"
if args.data_format:
    if (args.data_format == "json"):
        data_format = "json"

port = 7090
if args.port:
    port = int(args.port)

header = None
if 'accept' in locals():
    if args.accept:
        header = {"accept" : args.accept}

# example:initialize-sms-client
sms_client = oneapi.SmsClient(args.username, args.password, args.server)
# ----------------------------------------------------------------------------------------------------

# example:prepare-message-without-notify-url
sms = models.SMSRequest()
sms.sender_address = args.sender
sms.notify_url = 'http://{}:{}'.format(public_ip_address, port)
sms.callback_data = 'Any string'
sms.filter_criteria = "Urgent"
# ----------------------------------------------------------------------------------------------------

# example:send-message
result = sms_client.subscribe_delivery_status(sms, header, data_format)
# store client correlator because we can later query for the delivery status with it:
resource_url = result.resource_url
# ----------------------------------------------------------------------------------------------------

if not result.is_success():
    print 'Error sending message:', result.exception
    sys.exit(1)

print 'Is success = ', result.is_success()
print 'Resource URL = ', result.resource_url

# Few seconds later we can delete subscription
time.sleep(10)

# example:query-for-delivery-status
sms_client.delete_delivery_status_subscription(resource_url)
# ----------------------------------------------------------------------------------------------------
