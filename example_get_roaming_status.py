# -*- coding: utf-8 -*-

import pdb

import sys as sys
import logging as logging
import time as time

import oneapi as oneapi
import oneapi.models as models
import oneapi.dummyserver as dummyserver

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

if len(sys.argv) < 2:
    print 'Please enter username and password'
    sys.exit(1)

username = sys.argv[1]
password = sys.argv[2]

destination_address = raw_input('Enter the destination address?')

# example:data-connection-client
data_connection_client = oneapi.DataConnectionProfileClient(username, password)
data_connection_client.login()
# ----------------------------------------------------------------------------------------------------

response = data_connection_client.retrieve_roaming_status(destination_address)

print response
