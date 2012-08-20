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

Same as with the standard messaging example, but when preparing your message:

    sms = models.SMSRequest()
    sms.sender_address = address
    sms.address = address
    sms.message = 'Test message'
    # The url where the delivery notification will be pushed:
    sms.notify_url = notify_url


When the delivery notification is pushed to your server as a HTTP POST request, you must process the body of the message with the following code:

    delivery_status = oneapi.SmsClient.unserialize_delivery_status(http_body)


HLR example
-----------------------

Initialize and login the data connection client:

    data_connection_client = oneapi.DataConnectionProfileClient(username, password)
    data_connection_client.login()


Retrieve the roaming status (HLR):

    TODO

HLR with notification push example
-----------------------

Similar to the previous example, but this time you must set the notification url where the result will be pushed:

    response = data_connection_client.retrieve_roaming_status(destination_address, notify_url)


When the roaming status notification is pushed to your server as a HTTP POST request, you must process the body of the message with the following code:

    TODO

Retrieve inbound messages example
-----------------------

With the existing sms client (see the basic messaging example to see how to start it):

    result = sms_client.retrieve_inbound_messages()


Inbound message push example
-----------------------

The subscription to recive inbound messages can be set up on our site.
When the inbound message notification is pushed to your server as a HTTP POST request, you must process the body of the message with the following code:

    inbound_message = oneapi.SmsClient.unserialize_inbound_messages(http_body)


License
-------

This library is licensed under the [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0)
