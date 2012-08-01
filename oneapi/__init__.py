# -*- coding: utf-8 -*-

import pdb

import json as mod_json
import logging as mod_logging

import requests as mod_requests

import models as mod_models
import object as mod_object
import utils as mod_utils

DEFAULT_BASE_URL = 'http://api.parseco.com'

class AbstractOneApiClient:
    """
    Note that this is *not* a http session. This class is just a utility class 
    holding authorization data and a few utility methods for http requests.
    """

    def __init__(self, username, password, base_url=None):
        self.base_url = base_url if base_url else DEFAULT_BASE_URL
        self.username = username
        self.password = password

        if not self.base_url.endswith('/'):
            self.base_url += '/'

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

    def get_exception_details(self, exception_response):
        """ Returns message_id, text and variables from the standard API exception response. """
        exception = None
        try:
            exception = result['requestError']['serviceException']
        except Exception, e:
            pass
        if not exception:
            try:
                exception = result['requestError']['serviceException']
            except Exception, e:
                pass
        message_id = exception['messageId'] if exception.has_key('messageId') else None
        text = exception['text'] if exception.has_key('text') else None
        variables = exception['variables'] if exception.has_key('variables') else None

        return message_id, text, variables

    def execute_GET(self, rest_path, params=None, leave_undecoded=None):
        response = mod_requests.get(self.get_rest_url(rest_path), params=params, auth=(self.username, self.password))

        mod_logging.debug('status code:{0}'.format(response.status_code))
        mod_logging.debug('text:{0}'.format(response.text))
        mod_logging.debug('content:{0}'.format(response.content))

        is_success = 200 <= response.status_code <= 299

        if leave_undecoded:
            return is_success, response.content

        return is_success, mod_json.loads(response.content)

    def execute_POST(self, rest_path, params=None, leave_undecoded=None):
        response = mod_requests.post(self.get_rest_url(rest_path), data=params, auth=(self.username, self.password))

        mod_logging.debug('status code:{0}'.format(response.status_code))
        mod_logging.debug('params: {0}'.format(params))
        mod_logging.debug('text:{0}'.format(response.text))
        mod_logging.debug('content:{0}'.format(response.content))

        is_success = 200 <= response.status_code <= 299

        if leave_undecoded:
            return is_success, response.content

        return is_success, mod_json.loads(response.content)

    def execute_DELETE(self, rest_path, params=None, leave_undecoded=None):
        response = mod_requests.delete(self.get_rest_url(rest_path), data=params, auth=(self.username, self.password))

        mod_logging.debug('status code:{0}'.format(response.status_code))
        mod_logging.debug('text:{0}'.format(response.text))
        mod_logging.debug('content:{0}'.format(response.content))

        if leave_undecoded:
            return is_success, response.content

        return is_success, mod_json.loads(response.content)

    def create_from_json(self, classs, json, is_error):
        """ Converti API result from json to model. """
        return mod_object.Conversions.from_json(classs, json, is_error);

class SmsClient(AbstractOneApiClient):

    def __init__(self, username, password, base_url=None):
        AbstractOneApiClient.__init__(self, username, password, base_url=base_url)

    def send_sms(self, sms):
        client_correlator = sms.client_correlator
        if not client_correlator:
            client_correlator = mod_utils.get_random_alphanumeric_string()

        params = {
            'senderAddress': sms.sender_address,
            'address': sms.address,
            'message': sms.message,
            'clientCorrelator': client_correlator,
            'senderName': 'tel:{0}'.format(sms.sender_address),
        }

        if sms.notify_url:
            params['notifyURL'] = sms.notify_url
        if sms.callback_data:
            params['callbackData'] = sms.callback_data

        is_success, result = self.execute_POST(
                '/1/smsmessaging/outbound/{0}/requests'.format(sms.sender_address),
                params = params
        )

        return mod_object.Conversions.from_json(mod_models.ResourceReference, result, not is_success)

    def query_delivery_status(self, client_correlator_or_resource_reference):
        if hasattr(client_correlator_or_resource_reference, 'client_correlator'):
            client_correlator = client_correlator_or_resource_reference.client_correlator
        else:
            client_correlator = client_correlator_or_resource_reference

        client_correlator = self.get_client_correlator(client_correlator)

        params = {
            'clientCorrelator': client_correlator,
        }

        is_success, result = self.execute_GET(
                '/1/smsmessaging/outbound/TODO/requests/{0}/deliveryInfos'.format(client_correlator),
                params = params
        )

        # TODO: Simplify the resulting object
        return mod_object.Conversions.from_json(mod_models.DeliveryInfoList, result, not is_success)

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

        return self.create_from_json(mod_models.InboundSmsMessages, result, not is_success)

    @staticmethod
    def unserialize_inbound_message(json):
        return mod_object.Conversions.from_json(mod_models.InboundSmsMessages, json, False)

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
            assert json.has_key('roaming')
            return self.create_from_json(mod_models.TerminalRoamingStatus, json['roaming'], not is_success);
