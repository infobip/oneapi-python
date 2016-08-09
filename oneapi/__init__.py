# -*- coding: utf-8 -*-

import pdb

from . import exceptions as mod_exceptions
import json as mod_json
import logging as mod_logging
import base64 as mod_base64

from . import http as mod_http
from . import models as mod_models
from . import object as mod_object
from . import utils as mod_utils

DEFAULT_BASE_URL = 'https://oneapi.infobip.com'


class AbstractOneApiClient:
    VERSION = '0.03'

    """
    Note that this is *not* a http session. This class is just a utility class 
    holding authorization data and a few utility methods for http requests.
    """

    def __init__(self, username, password, base_url=None):
        self.base_url = base_url if base_url else DEFAULT_BASE_URL
        self.username = username
        self.password = password
        self.oneapi_authentication = None

        if not self.base_url.endswith('/'):
            self.base_url += '/'

        # If true -- an exception will be thrown on error, otherwise, you have 
        # to check the is_success and exception methods on resulting objects.
        self.raise_exception = True

    def login(self):
        params = {
            'username': self.username,
            'password': self.password,
        }

        is_success, result = self.execute_POST('/1/customerProfile/login', params)

        return self.fill_oneapi_authentication(result, is_success)

    def fill_oneapi_authentication(self, content, is_success):
        self.oneapi_authentication = self.create_from_json(mod_models.OneApiAuthentication,
                                                           content, not is_success)
        self.oneapi_authentication.username = self.username
        self.oneapi_authentication.password = self.password
        self.oneapi_authentication.authenticated = len(self.oneapi_authentication.ibsso_token) > 0
        return self.oneapi_authentication

    def get_client_correlator(self, client_correlator=None):
        if client_correlator:
            return client_correlator;

        return mod_utils.get_random_alphanumeric_string()

    def get_rest_url(self, rest_path):
        if not rest_path:
            return self.base_url

        if rest_path.startswith('/'):
            return self.base_url + rest_path[1:]

        return self.base_url + rest_path

    def is_valid(self):
        """ Check if the authorization (username/password) is valid. """
        is_success, result = self.execute_GET('/1/customerProfile')

        return is_success

    def get_headers(self, headers=None):
        assert headers is None or isinstance(headers, dict)

        result = headers
        if result is None:
            result = {}

        result["User-Agent"] = "OneApi-python-{0}".format(self.VERSION)

        if self.oneapi_authentication and self.oneapi_authentication.ibsso_token:
            result['Authorization'] = 'IBSSO {0}'.format(self.oneapi_authentication.ibsso_token)
        else:
            auth_string = '%s:%s' % (self.username, self.password)
            auth_string = mod_base64.encodestring(auth_string.encode('utf-8'))
            result['Authorization'] = 'Basic {0}'.format(auth_string.decode('utf-8')).strip()
        return result

    def execute_GET(self, rest_path, params=None, leave_undecoded=False, headers=None):
        response = mod_http.execute_GET(self.get_rest_url(rest_path), data=params,
                                        headers=self.get_headers(headers))

        mod_logging.debug('status code:{0}'.format(response.status_code))
        mod_logging.debug('content:{0}'.format(response.content))

        is_success = 200 <= response.status_code <= 299

        if leave_undecoded or not is_success:
            return is_success, response.content

        return is_success, mod_json.loads(response.content)

    def execute_POST(self, rest_path, params=None, leave_undecoded=False, headers=None, data_format=None):
        response = mod_http.execute_POST(self.get_rest_url(rest_path), data=params,
                                         headers=self.get_headers(headers), data_format=data_format)

        mod_logging.debug('status code:{0}'.format(response.status_code))
        mod_logging.debug('params: {0}'.format(params))
        mod_logging.debug('content:{0}'.format(response.content))

        is_success = 200 <= response.status_code <= 299

        if leave_undecoded or not is_success:
            return is_success, response.content

        return is_success, mod_json.loads(response.content.decode('utf-8'))

    def execute_PUT(self, rest_path, params=None, leave_undecoded=False, headers=None):
        response = mod_http.execute_PUT(self.get_rest_url(rest_path), data=params,
                                        headers=self.get_headers(headers))

        mod_logging.debug('status code:{0}'.format(response.status_code))
        mod_logging.debug('params: {0}'.format(params))
        mod_logging.debug('content:{0}'.format(response.content))

        is_success = 200 <= response.status_code <= 299

        if leave_undecoded or not is_success:
            return is_success, response.content

        return is_success, mod_json.loads(response.content)

    def execute_DELETE(self, rest_path, params=None, leave_undecoded=False, headers=None, use_absolute_path=None):
        if use_absolute_path:
            response = mod_http.execute_DELETE(rest_path, data=params,
                                               headers=self.get_headers(headers))
        else:
            response = mod_http.execute_DELETE(self.get_rest_url(rest_path), data=params,
                                               headers=self.get_headers(headers))

        mod_logging.debug('status code:{0}'.format(response.status_code))
        mod_logging.debug('content:{0}'.format(response.content))

        is_success = 200 <= response.status_code <= 299

        if leave_undecoded or not is_success or response.status_code == 204:
            return is_success, response.content

        return is_success, mod_json.loads(response.content)

    def create_from_json(self, classs, json, is_error):
        """ Converti API result from json to model. """
        result = mod_object.Conversions.from_json(classs, json, is_error);

        if self.raise_exception and not result.is_success():
            message = "{0}: {1} [{2}]".format(result.exception.message_id, result.exception.text,
                                              result.exception.variables)
            raise mod_exceptions.OneApiError(message)

        return result

    def create_to_json(self, json):
        result = mod_object.Conversions.to_json(json);

        return result


class OneApiClient(AbstractOneApiClient):
    """ Generic OneApi client. May be used for direct rest requests. """

    def __init__(self, username, password, base_url=None):
        AbstractOneApiClient.__init__(self, username, password, base_url=base_url)


class SmsClient(AbstractOneApiClient):
    def __init__(self, username, password, base_url=None):
        AbstractOneApiClient.__init__(self, username, password, base_url=base_url)

    def send_sms(self, sms, header=None, data_format=None):
        if not data_format: data_format = 'json'

        client_correlator = sms.client_correlator
        if not client_correlator:
            client_correlator = mod_utils.get_random_alphanumeric_string()

        if data_format == "json":
            params = {
                'address': [
                    'tel:{0}'.format(sms.address)
                ],
                'clientCorrelator': client_correlator,
                'senderAddress': sms.sender_address,
                'message': sms.message,
                'senderName': 'tel:{0}'.format(sms.sender_address),
                'callbackData': sms.callback_data,
                'notifyURL': sms.notify_url
            }
        elif data_format == "url":
            params = {
                'senderAddress': sms.sender_address,
                'address': sms.address,
                'message': sms.message,
                'clientCorrelator': client_correlator,
                'senderName': 'tel:{0}'.format(sms.sender_address),
            }

            if sms.mo_response_key:
                params['moResponseKey'] = sms.mo_response_key

            if sms.notify_url:
                params['notifyURL'] = sms.notify_url
            if sms.callback_data:
                params['callbackData'] = sms.callback_data
        else:
            raise ValueError("invalid asked data format (supported url or json")

        is_success, result = self.execute_POST(
            '/1/smsmessaging/outbound/{0}/requests'.format(sms.sender_address),
            params=params,
            headers=header,
            data_format=data_format
        )

        if not is_success:
            return is_success

        return self.create_from_json(mod_models.ResourceReference, result, not is_success)

    def query_delivery_status(self, client_correlator_or_resource_reference, sender):
        if hasattr(client_correlator_or_resource_reference, 'client_correlator'):
            client_correlator = client_correlator_or_resource_reference.client_correlator
        else:
            client_correlator = client_correlator_or_resource_reference

        client_correlator = self.get_client_correlator(client_correlator)

        params = {
            'clientCorrelator': client_correlator,
        }

        is_success, result = self.execute_GET(
            '/1/smsmessaging/outbound/{0}/requests/{1}/deliveryInfos'.format(sender, client_correlator),
            params=params
        )

        if not is_success:
            return is_success

        # TODO: Simplify the resulting object
        return self.create_from_json(mod_models.DeliveryInfoList, result, not is_success)

    def retrieve_inbound_messages(self, max_number=None):
        if not max_number or max_number < 0:
            max_number = 100

        params = {
            'maxBatchSize': max_number,
        }

        is_success, result = self.execute_GET(
            '/1/smsmessaging/inbound/registrations/INBOUND/messages',
            params
        )

        if not is_success:
            return is_success

        return self.create_from_json(mod_models.InboundSmsMessages, result, not is_success)

    def subscribe_delivery_status(self, sms, header=None, data_format=None):
        if not data_format: data_format = 'json'

        if data_format == "json":
            params = {
                'callbackData': sms.callback_data,
                'notifyURL': sms.notify_url,
                'criteria': sms.filter_criteria
            }
        elif data_format == "url":
            params = {
                'callbackData': sms.callback_data,
                'notifyURL': sms.notify_url,
                'criteria': sms.filter_criteria
            }
        else:
            raise ValueError("invalid asked data format (supported url or json")

        is_success, result = self.execute_POST(
            '/1/smsmessaging/outbound/'
            '{0}/subscriptions'.format(sms.sender_address),
            params=params,
            headers=header,
            data_format=data_format
        )

        if not is_success:
            return is_success

        return self.create_from_json(mod_models.DeliveryReceiptSubscription, result, not is_success)

    # TODO (pd) only subscriptionID should be passed into this method
    def delete_delivery_status_subscription(self, resource_url):

        is_success = self.execute_DELETE(
            resource_url, use_absolute_path=True
        )

        return is_success

    def subscribe_messages_sent_notification(self, sms, header=None, data_format=None):
        if not data_format: data_format = 'json'

        if data_format == "json":
            params = {
                'callbackData': sms.callback_data,
                'notifyURL': sms.notify_url,
                'criteria': sms.filter_criteria,
                'destinationAddress': sms.address,
                'clientCorrelator': sms.client_correlator
            }
        elif data_format == "url":
            params = {
                'callbackData': sms.callback_data,
                'notifyURL': sms.notify_url,
                'destinationAddress': sms.address
            }
            if sms.filter_criteria:
                params['criteria'] = sms.filter_criteria
            if sms.client_correlator:
                params['client_correlator'] = sms.client_correlator
                # resourceURL
        else:
            raise ValueError("invalid asked data format (supported url or json")

        is_success, result = self.execute_POST(
            '/1/smsmessaging/inbound/subscriptions',
            params=params,
            headers=header,
            data_format=data_format
        )

        if not is_success:
            return is_success

        return self.create_from_json(mod_models.InboundSMSMessageReceiptSubscription, result, not is_success)

    # TODO (pd) only subscriptionID should be passed into this method
    def delete_messages_sent_subscription(self, resource_url):

        is_success = self.execute_DELETE(
            resource_url, use_absolute_path=True
        )

        return is_success

    # ----------------------------------------------------------------------------------------------------
    # Static methods used for http push events from the server:
    # ----------------------------------------------------------------------------------------------------    

    @staticmethod
    def unserialize_inbound_messages(json):
        return mod_object.Conversions.from_json(mod_models.InboundSmsMessages, json, False)

    @staticmethod
    def unserialize_delivery_status(json):
        return mod_object.Conversions.from_json(mod_models.DeliveryInfoNotification, json, False)


class UssdClient(AbstractOneApiClient):
    """
    Warning, this is an experimental feature. The API may change!
    """

    def __init__(self, username, password, base_url=None):
        AbstractOneApiClient.__init__(self, username, password, base_url=base_url)

    def send_message(self, address, message):
        params = {
            'address': address,
            'message': message,
        }

        is_success, json = self.execute_POST(
            '/1/ussd/outbound',
            params=params
        )

        return self.create_from_json(mod_models.InboundSmsMessage, json, not is_success)

    def close_session(self, address, message):
        params = {
            'address': address,
            'message': message,
            'stopSession': 'true',
        }

        is_success, json = self.execute_POST(
            '/1/ussd/outbound',
            params=params,
            leave_undecoded=True
        )

        return True


class DataConnectionProfileClient(AbstractOneApiClient):
    def __init__(self, username, password, base_url=None):
        AbstractOneApiClient.__init__(self, username, password, base_url=base_url)

    def retrieve_roaming_status(self, destination_address, notify_url=None):
        """
        Retrieve asynchronously the customer’s roaming status for a single network-connected mobile device  (HLR)
        """
        params = {
            'address': destination_address,
        }

        if notify_url:
            params['notifyURL'] = notify_url

        # TODO(TK) Add these includeExtendedData, clientCorrelator, callbackData

        is_success, result = self.execute_GET('/1/terminalstatus/queries/roamingStatus', params,
                                              leave_undecoded=True)

        if notify_url:
            return self.create_from_json(mod_models.GenericObject, {}, not is_success);
        else:
            assert result
            json = mod_json.loads(result)
            assert 'roaming' in json
            return self.create_from_json(mod_models.TerminalRoamingStatus, json['roaming'], not is_success);

    # ----------------------------------------------------------------------------------------------------
    # Static methods used for http push events from the server:
    # ----------------------------------------------------------------------------------------------------    

    @staticmethod
    def unserialize_roaming_status(json):
        return mod_object.Conversions.from_json(mod_models.TerminalRoamingStatusNotification, json, False)


class CustomerProfileClient(AbstractOneApiClient):
    def __init__(self, username, password, base_url=None):
        AbstractOneApiClient.__init__(self, username, password, base_url=base_url)

    def get_account_balance(self):
        is_success, result = self.execute_GET('/1/customerProfile/balance')

        return self.create_from_json(mod_models.AccountBalance, result, not is_success)

    def get_customer_profile(self):
        is_success, result = self.execute_GET('/1/customerProfile')

        return self.create_from_json(mod_models.CustomerProfile, result, not is_success)
