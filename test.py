# -*- coding: utf-8 -*-

import pdb

import logging as mod_logging
import unittest as mod_unittest

import oneapi.object as mod_object
import oneapi.models as mod_models

class Tests(mod_unittest.TestCase):

    def test_json_deserialization(self):
        class Alias(mod_object.AbstractModel):

            name = mod_object.FieldConverter()

            def __init__(self):
                mod_object.AbstractModel.__init__(self)

        class Person(mod_object.AbstractModel):

            name = mod_object.FieldConverter('name')
            family_name = mod_object.FieldConverter('familyName')
            age = mod_object.FieldConverter()
            aliases = mod_object.ObjectsListFieldConverter(Alias)
            main_alias = mod_object.ObjectFieldConverter(Alias, json_field_name='mainAlias')

            def __init__(self):
                mod_object.AbstractModel.__init__(self)

        json = '{"familyName": "bbb", "name": "aaa", "aliases": [{"name": "qqqq"}, {"name": "wwww"}, {"name": "yyyy"}], "age": 17, "mainAlias": {"name": "gazda"}}';
        person = mod_object.Conversions.from_json(Person, json, False)
        mod_logging.debug('person={0}'.format(person))

        self.assertTrue(person)
        self.assertEquals(int, person.age.__class__)
        self.assertEquals(17, person.age)
        self.assertEquals(list, person.aliases.__class__)
        self.assertEquals(3, len(person.aliases))
        self.assertEquals('wwww', person.aliases[1].name)
        self.assertEquals('gazda', person.main_alias.name)

    def test_nonstandard_json_deserialization(self):
        class Person(mod_object.AbstractModel):

            name = mod_object.FieldConverter('name')
            family_name = mod_object.FieldConverter('familyName')
            age = mod_object.FieldConverter()

            # Nonstandard deserialization the first not-null JSON element must be used:
            main_alias = [mod_object.FieldConverter('mainAlias.name'), mod_object.FieldConverter('aliases.0.name')]

            def __init__(self):
                mod_object.AbstractModel.__init__(self)

        json = '{"familyName": "bbb", "name": "aaa", "aliases": [{"name": "qqqq"}, {"name": "wwww"}, {"name": "yyyy"}], "age": 17, "mainAlias": {"name": "gazda"}}';
        person = mod_object.Conversions.from_json(Person, json, False)
        mod_logging.debug('person={0}'.format(person))

        self.assertTrue(person)
        self.assertEquals('gazda', person.main_alias)

        json = '{"familyName": "bbb", "name": "aaa", "aliases": [{"name": "qqqq"}, {"name": "wwww"}, {"name": "yyyy"}], "age": 17, "mainAlias": {"name": null}}';
        person = mod_object.Conversions.from_json(Person, json, False)
        mod_logging.debug('person={0}'.format(person))

        self.assertTrue(person)
        self.assertEquals('qqqq', person.main_alias)

    def test_exception_serialization(self):
        json = '{"requestError":{"serviceException":{"text":"Request URI missing required component(s): ","messageId":"SVC0002","variables":["aaa"]}}}';

        error = mod_object.Conversions.from_json(mod_models.OneApiError, json, False)

        self.assertTrue(error != None)
        self.assertFalse(error.is_success())
        self.assertEquals(error.message_id, 'SVC0002')
        self.assertEquals(error.text, 'Request URI missing required component(s): ')
        self.assertEquals(len(error.variables), 1)
        self.assertEquals(error.variables[0], 'aaa')

    def test_exception_serialization(self):
        """
        Trying to deserialize an object but instead we got a error response => 
        object with filled exception and is_success == False
        """
        json = '{"requestError":{"policyException":{"text":"Request URI missing required component(s): ","messageId":"SVC0002","variables":["aaa"]}}}';

        # Deserialize when is_error == True:
        result = mod_object.Conversions.from_json(mod_models.SMSRequest, json, is_error = True)

        self.assertFalse(result.is_success())
        self.assertTrue(result.exception != None)

        self.assertTrue(result.exception != None)
        self.assertTrue(result.exception.is_success())
        self.assertEquals(result.exception.message_id, 'SVC0002')
        self.assertEquals(result.exception.text, 'Request URI missing required component(s): ')
        self.assertEquals(len(result.exception.variables), 1)
        self.assertEquals(result.exception.variables[0], 'aaa')

    def test_client_correlator(self):
        json = '{"resourceReference":{"resourceURL":"http://test.com/1/smsmessaging/outbound/38598123456/requests/hzmrjiywg5"}}'

        result = mod_object.Conversions.from_json(mod_models.ResourceReference, json, is_error=False)

        self.assertEquals(result.client_correlator, 'hzmrjiywg5')

if __name__ == '__main__':
    mod_logging.basicConfig(level=mod_logging.DEBUG, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    mod_unittest.main()
