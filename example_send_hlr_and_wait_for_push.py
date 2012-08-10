# -*- coding: utf-8 -*-

import pdb

import sys as sys
import logging as logging
import time as time

import oneapi as oneapi
import oneapi.models as models
import oneapi.dummyserver as dummyserver

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

if len(sys.argv) < 3:
    print 'Please enter username, password and notification url'
    sys.exit(1)

username = sys.argv[1]
password = sys.argv[2]
notify_url = sys.argv[3]

destination_address = raw_input('Enter the destination address?')
#destination_address = raw_input('Enter the destination address?')

data_connection_client = oneapi.DataConnectionProfileClient(username, password)
data_connection_client.login()

# example:retrieve-roaming-status-with-notify-url
response = data_connection_client.retrieve_roaming_status(destination_address, notify_url)
# ----------------------------------------------------------------------------------------------------

print response
