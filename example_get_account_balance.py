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

account_balance = customer_profile_client.get_account_balance()

print
print account_balance.balance, account_balance.currency.symbol
print
