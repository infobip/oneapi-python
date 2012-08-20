# -*- coding: utf-8 -*-

import pdb

import oneapi as oneapi

# This files contain examples on how to handle inbound http push events. Your 
# scripts should be able to retrieve the http body of the request and call one 
# of the following lines:

# example:on-mo
oneapi.SmsClient.unserialize_inbound_messages(http_body)
# ----------------------------------------------------------------------------------------------------

# example:on-delivery-notification
oneapi.SmsClient.unserialize_delivery_status(http_body)
# ----------------------------------------------------------------------------------------------------

# example:on-roaming-status
oneapi.SmsClient.unserialize_roaming_status(http_body)
# ----------------------------------------------------------------------------------------------------
