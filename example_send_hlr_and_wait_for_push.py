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

notify_url = 'http://{0}:{1}'.format(public_ip_address, port)

destination_address = raw_input('Enter the destination address?')

data_connection_client = mod_oneapi.DataConnectionProfileClient(username, password)

response = data_connection_client.retrieve_roaming_status_async(destination_address, notify_url)
if not response.is_success():
    print 'Error checking for roaming status:', result.exception
    mod_sys.exit(1)

print 'Roaming status request sent, the result will be pushed to:', notify_url

# Wait for 30 seconds for push-es
server = mod_dummyserver.DummyWebServer(port)
server.start_wait_and_shutdown(10)

print server.get_requests()
