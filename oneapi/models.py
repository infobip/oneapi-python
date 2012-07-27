# -*- coding: utf-8 -*-

import object as mod_object
import utils as mod_utils

# ----------------------------------------------------------------------------------------------------
# SMS message models:
# ----------------------------------------------------------------------------------------------------

class OneApiError(mod_object.AbstractModel):

    message_id = [ mod_object.FieldConverter('requestError.serviceException.messageId'), mod_object.FieldConverter('requestError.policyException.messageId') ]
    text = [ mod_object.FieldConverter('requestError.serviceException.text'), mod_object.FieldConverter('requestError.policyException.text') ]
    variables = [ mod_object.FieldConverter('requestError.serviceException.variables'), mod_object.FieldConverter('requestError.policyException.variables') ]

    def __init__(self):
        mod_object.AbstractModel.__init__(self)

# ----------------------------------------------------------------------------------------------------
# SMS message models:
# ----------------------------------------------------------------------------------------------------

class SMSRequest(mod_object.AbstractModel):

    sender_address = mod_object.FieldConverter('senderAddress')
    sender_name = mod_object.FieldConverter('senderName')
    message = mod_object.FieldConverter()
    address = mod_object.FieldConverter()

    # Used later for querying about the message status.
    client_correlator = mod_object.FieldConverter('clientCorrelator')

    # If not empty -- this is the url where the delivery notification will be pushed. 
    # 
    # If empty -- the delivery notification may be queried using the 
    # clientCorrelator string.
    notify_url = mod_object.FieldConverter('notifyURL')

    # Artibtrary string that will be pushed if notifyURL is set.
    callback_data = mod_object.FieldConverter('callbackData')

    def __init__(self, sender_address=None, message=None, address=None, client_correlator=None,
                 notify_url=None, sender_name=None, callback_data=None):
        mod_object.AbstractModel.__init__(self)

        self.sender_address = sender_address
        self.message = message
        self.address = address
        self.client_correlator = client_correlator
        self.notify_url = notify_url
        self.sender_name = sender_name
        self.callback_data = callback_data

# ----------------------------------------------------------------------------------------------------

class ResourceReference(mod_object.AbstractModel):

    # The client correlator for this message. This value may be used to query 
    # for message status later.
    client_correlator = mod_object.LastPartOfUrlFieldConverter('resourceReference.resourceURL')

    def __init__(self, client_correlator=None):
        mod_object.AbstractModel.__init__(self)

        self.client_correlator = client_correlator

# ----------------------------------------------------------------------------------------------------

class DeliveryInfo(mod_object.AbstractModel):

    delivery_status = mod_object.FieldConverter('deliveryStatus')

    def __init__(self):
        mod_object.AbstractModel.__init__(self)

# ----------------------------------------------------------------------------------------------------

class DeliveryInfoList(mod_object.AbstractModel):

    delivery_info = mod_object.ObjectsListFieldConverter(DeliveryInfo, json_field_name='deliveryInfoList.deliveryInfo')

    def __init__(self):
        mod_object.AbstractModel.__init__(self)

# ----------------------------------------------------------------------------------------------------

