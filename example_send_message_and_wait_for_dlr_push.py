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
parser.add_argument("address", help="Destination address")
parser.add_argument("sender", help="Sender address")
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

sms_client = oneapi.SmsClient(args.username, args.password, args.server)

# example:prepare-message-with-notify-url
sms = models.SMSRequest()
sms.sender_address = args.sender
sms.address = args.address
sms.message = 'Test message'
# The url where the delivery notification will be pushed:
sms.notify_url = 'http://{}:{}'.format('localhost', port)
sms.callback_data = 'any+string'
# ----------------------------------------------------------------------------------------------------

result = sms_client.send_sms(sms, header, data_format)

if not result.is_success():
    print 'Error sending message:', result.exception
    sys.exit(1)

print result
print 'Is success = ', result.is_success()
print 'Client correlator = ', result.client_correlator

# Wait for 15 seconds for push-es
server = dummyserver.DummyWebServer(port)
server.start_wait_and_shutdown(15)

requests = server.get_requests()
if not requests:
    print 'No requests received'
    sys.exit(1)

for method, path, http_body in requests:
    # example:on-delivery-notification
    delivery_status = oneapi.SmsClient.unserialize_delivery_status(http_body)
    # ----------------------------------------------------------------------------------------------------
    print delivery_status
