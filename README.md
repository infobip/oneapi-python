OneApi python client
============================

Basic messaging example
-----------------------

First initialize the messaging client using your username and password:

    sms_client = oneapi.SmsClient(username, password)


Then login with the client:

    sms_client.login()


An exception will be thrown if your username and/or password are incorrect.

Prepare the message:

    sms = models.SMSRequest()
    sms.sender_address = address
    sms.address = address
    sms.message = 'Test message'
    sms.callback_data = 'Any string'


Send the message:

    result = sms_client.send_sms(sms)
    # store client correlator because we can later query for the delivery status with it:
    client_correlator = result.client_correlator


Later you can query for the delivery status of the message:

    query_status = sms_client.query_delivery_status(client_correlator)
    delivery_status = query_status.delivery_info[0].delivery_status


Possible statuses are: **DeliveredToTerminal**, **DeliveryUncertain**, **DeliveryImpossible**, **MessageWaiting** and **DeliveredToNetwork**.

Messaging with notification push example
-----------------------

HLR example
-----------------------

HLR with notification push example
-----------------------

Retrieve inbound messages example
-----------------------

Inbound message push example
-----------------------

License
-------

This library is licensed under the [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0)
