# -*- coding: utf-8 -*-

import pdb

import oneapi as oneapi

# This files contain examples on how to handle inbound http push events. Your 
# scripts should be able to retrieve the http body of the request and call one 
# of the following lines:

# example:on-mo
inbound_message = oneapi.SmsClient.unserialize_inbound_messages(http_body)
# ----------------------------------------------------------------------------------------------------
