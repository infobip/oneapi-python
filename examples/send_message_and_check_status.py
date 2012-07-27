# -*- coding: utf-8 -*-

import pdb

import oneapi as mod_oneapi
import oneapi.object as mod_object
import oneapi.models as mod_models

json = '{"requestError":{"serviceException":{"text":"Request URI missing required component(s): ","messageId":"SVC0002","variables":[""]},"policyException":null}}';

sms_exception = mod_object.Conversions.from_json(mod_models.OneApiError, json, False)

print sms_exception
