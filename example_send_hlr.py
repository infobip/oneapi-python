# -*- coding: utf-8 -*-

import pdb

import sys as mod_sys
import logging as mod_logging
import time as mod_time

import oneapi as mod_oneapi
import oneapi.models as mod_models
import oneapi.dummyserver as mod_dummyserver

mod_logging.basicConfig(level=mod_logging.DEBUG, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

if len(mod_sys.argv) < 2:
    print 'Please enter username and password'
    mod_sys.exit(1)

username = mod_sys.argv[1]
password = mod_sys.argv[2]

destination_address = raw_input('Enter the destination address?')

data_connection_client = mod_oneapi.DataConnectionProfileClient(username, password)

response = data_connection_client.retrieve_roaming_status(destination_address)

print response
