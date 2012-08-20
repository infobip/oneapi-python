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
    print 'Please enter username, password, your ip address and gsm number'
    sys.exit(1)

username = sys.argv[1]
password = sys.argv[2]
public_ip_address = sys.argv[3]
address = sys.argv[4]
port = 9000

notify_url = 'http://{0}:{1}'.format(public_ip_address, port)

data_connection_client = oneapi.DataConnectionProfileClient(username, password)
data_connection_client.login()

# example:retrieve-roaming-status-with-notify-url
response = data_connection_client.retrieve_roaming_status(address, notify_url)
# ----------------------------------------------------------------------------------------------------

# Wait for 15 seconds for push-es
server = dummyserver.DummyWebServer(port)
server.start_wait_and_shutdown(15)

requests = server.get_requests()
if not requests:
    print 'No requests received'
    sys.exit(1)

for method, path, http_body in requests:
    # example:on-roaming-status
    roaming_status = oneapi.DataConnectionProfileClient.unserialize_roaming_status(http_body)
    # ----------------------------------------------------------------------------------------------------
    print roaming_status
