# -*- coding: utf-8 -*-

import pdb

import sys as sys
import logging as logging

import oneapi as oneapi
import oneapi.models as models

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

if len(sys.argv) < 2:
    print 'Please enter username and password'
    sys.exit(1)

username = sys.argv[1]
password = sys.argv[2]

customer_profile_client = oneapi.CustomerProfileClient(username, password)
customer_profile_client.login()

customer_profile = customer_profile_client.get_customer_profile()

print
print customer_profile
print
