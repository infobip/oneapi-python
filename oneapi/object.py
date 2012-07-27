# -*- coding: utf-8 -*-

import pdb

import logging as mod_logging
import json as mod_json

import oneapi.utils as mod_utils

class FieldConverter:

    def __init__(self, json_field_name=None):
        self.json_field_name = json_field_name

        # Filled later while registering the model:
        self.object_field_name = None

    def from_json(self, value):
        return value

    def to_json(self, value):
        return value

class LastPartOfUrlFieldConverter(FieldConverter):

    def __init__(self, json_field_name=None):
        FieldConverter.__init__(self, json_field_name=json_field_name)

    def from_json(self, value):
        if not value:
            return value

        parts = value.split('/')

        return parts[-1]

    def to_json(self, value):
        return value

class ObjectFieldConverter(FieldConverter):

    def __init__(self, classs, json_field_name=None):
        FieldConverter.__init__(self, json_field_name=json_field_name)
        self.classs = classs

    def from_json(self, value):
        return Conversions.from_json(self.classs, value, is_error=False)

    def to_json(self, value):
        return Conversions.to_json(value)

class ObjectsListFieldConverter(FieldConverter):

    def __init__(self, classs, json_field_name=None):
        FieldConverter.__init__(self, json_field_name=json_field_name)
        self.classs = classs

    def from_json(self, values):
        if not values:
            return []

        result = []

        for value in values:
            result.append(Conversions.from_json(self.classs, value, is_error=False))

        return result

    def to_json(self, value):
        # TODO
        pass

# ----------------------------------------------------------------------------------------------------

class Models:

    models = []

    @staticmethod
    def register(model_class):
        """ Registers metadata for object<->JSON conversion """
        assert model_class

        Models.models.append(model_class)
        for attribute_name in dir(model_class):
            if '_' != attribute_name[0]:
                attribute_values = getattr(model_class, attribute_name)
                if not isinstance(attribute_values, list):
                    attribute_values = [attribute_values]

                for attribute_value in attribute_values:
                    if isinstance(attribute_value, FieldConverter):
                        if not attribute_value.json_field_name:
                            attribute_value.json_field_name = attribute_name
                        if not attribute_value.object_field_name:
                            attribute_value.object_field_name = attribute_name
                        attribute_value.object_field_name = attribute_name

    @staticmethod
    def is_registered(model_class):
        return model_class in Models.models

# ----------------------------------------------------------------------------------------------------

class Conversions:

    @staticmethod
    def fill_from_json(obj, json, is_error=False):
        """ Fill existing objects with JSON data. """
        assert obj
        assert json

        import oneapi.models as mod_models

        if isinstance(json, str) or isinstance(json, unicode):
            json = mod_json.loads(json)

        if is_error:
            obj.exception = Conversions.from_json(mod_models.OneApiError, json, False)
            assert not obj.is_success()
        else:
            for attribute_name in dir(obj.__class__):
                attribute_values = getattr(obj.__class__, attribute_name)
                if not isinstance(attribute_values, list):
                    attribute_values = [attribute_values]
                converted = None
                object_field_name = None
                for attribute_value in attribute_values:
                    if not converted:
                        if isinstance(attribute_value, FieldConverter):
                            object_field_name = attribute_value.object_field_name
                            json_field_name = attribute_value.json_field_name
                            json_value = mod_utils.get(json, json_field_name)
                            converted = attribute_value.from_json(json_value)
                if object_field_name:
                    setattr(obj, object_field_name, converted)

        return obj

    @staticmethod
    def from_json(classs, json, is_error=False):
        """ Create a new object converted from JSON data. """
        assert classs
        assert json

        result = classs()

        Conversions.fill_from_json(result, json, is_error)

        return result

    @staticmethod
    def to_json(obj):
        assert obj

        pass

# ----------------------------------------------------------------------------------------------------

class AbstractModel:

    exception = None

    def __init__(self):
        if not Models.is_registered(self.__class__):
            Models.register(self.__class__)

        # reset class attributes for this instance:
        for class_attribute in dir(self.__class__):
            class_attribute_value = getattr(self.__class__, class_attribute)
            if isinstance(class_attribute_value, ObjectFieldConverter):
                setattr(self, class_attribute, None)

    def is_success(self):
        return self.exception == None

    def __str__(self):
        result = '[{0}:'.format(self.__class__.__name__)

        for attr in dir(self):
            value = getattr(self, attr)
            if '_' != attr[0] and not callable(value):
                result += ':{0}={1}'.format(attr, value)

        return result + ']'

