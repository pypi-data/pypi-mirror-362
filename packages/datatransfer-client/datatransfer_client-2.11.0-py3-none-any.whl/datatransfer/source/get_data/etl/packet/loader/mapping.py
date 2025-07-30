# coding: utf-8

from __future__ import absolute_import

from datetime import date
from datetime import datetime

import six

from datatransfer.common.xml.parser import XMLModelParser
from datatransfer.source.get_data.etl.packet.extractor.common.mapping import (
    rules as extractor_rules
)


RULES = XMLModelParser.rules
MODEL = XMLModelParser.model
RECORD = XMLModelParser.record
DATA = XMLModelParser.data


def unbinded2none(value):
    if value in (-1, '-1'):
        return None

    return value


rules = RULES(
    '__rule__', MODEL(),
    'Packet', RULES(
        '__rule__', MODEL(),
        'Header', RULES(
            '__rule__', RECORD(a=False),
            'SourceSystemID', RULES(
                '__rule__', DATA(six.text_type)),
            'AuthorizationKey', RULES(
                '__rule__', DATA(six.text_type)),
            'DestinationSystemID', RULES(
                '__rule__', DATA(six.text_type)),
            'Timestamp', RULES(
                '__rule__', DATA(datetime)),
            'SessionID', RULES(
                '__rule__', DATA(six.text_type))),
        'Data', RULES(
            '__rule__', MODEL(),
            'Persons', RULES(
                '__rule__', MODEL(),
                'Person', RULES(
                    '__rule__', RECORD(),
                    'ID', RULES(
                        '__rule__', DATA(int, m=extractor_rules.extract_person_id)),
                    'RegionalID', RULES(
                        '__rule__', DATA(int)),
                    'FederalID', RULES(
                        '__rule__', DATA(six.text_type)),
                    'SourceID', RULES(
                        '__rule__', DATA(int)),
                    'ExternalID', RULES(
                        '__rule__', DATA(int)),
                    'FirstName', RULES(
                        '__rule__', DATA(six.text_type)),
                    'MiddleName', RULES(
                        '__rule__', DATA(six.text_type)),
                    'LastName', RULES(
                        '__rule__', DATA(six.text_type)),
                    'Gender', RULES(
                        '__rule__', DATA(six.text_type, m=unbinded2none)),
                    'BirthDate', RULES(
                        '__rule__', DATA(date)),
                    'BirthPlace', RULES(
                        '__rule__', DATA(six.text_type)),
                    'SNILS', RULES(
                        '__rule__', DATA(six.text_type)),
                    'HealthGroup', RULES(
                        '__rule__', DATA(six.text_type, m=unbinded2none)),
                    'LongTermTreatment', RULES(
                        '__rule__', DATA(six.text_type, m=unbinded2none)),
                    'DisabilityGroup', RULES(
                        '__rule__', DATA(six.text_type, m=unbinded2none)),
                    'DisabilityExpirationDate', RULES(
                        '__rule__', DATA(date)),
                    'DisabilityReason', RULES(
                        '__rule__', DATA(six.text_type, m=unbinded2none)),
                    'AdaptationProgram', RULES(
                        '__rule__', DATA(six.text_type, m=unbinded2none)),
                    'PhysicalCultureGroup', RULES(
                        '__rule__', DATA(six.text_type, m=unbinded2none)),
                    'DifficultSituation', RULES(
                        '__rule__', DATA(six.text_type, m=unbinded2none)),
                    'DocumentRegistryNumber', RULES(
                        '__rule__', DATA(six.text_type)),
                    'DocumentRegistryIssuer', RULES(
                        '__rule__', DATA(six.text_type)),
                    'DocumentRegistryIssueDate', RULES(
                        '__rule__', DATA(date)),
                    'Citizenship', RULES(
                        '__rule__', DATA(six.text_type, m=unbinded2none)),
                    'RegistrationAddressPlace', RULES(
                        '__rule__', DATA(six.text_type)),
                    'RegistrationAddressStreet', RULES(
                        '__rule__', DATA(six.text_type)),
                    'RegistrationAddressHouse', RULES(
                        '__rule__', DATA(six.text_type)),
                    'RegistrationAddressFlat', RULES(
                        '__rule__', DATA(six.text_type)),
                    'RegistrationAddress', RULES(
                        '__rule__', DATA(six.text_type)),
                    'ResidenceAddressPlace', RULES(
                        '__rule__', DATA(six.text_type)),
                    'ResidenceAddressStreet', RULES(
                        '__rule__', DATA(six.text_type)),
                    'ResidenceAddressHouse', RULES(
                        '__rule__', DATA(six.text_type)),
                    'ResidenceAddressFlat', RULES(
                        '__rule__', DATA(six.text_type)),
                    'ResidenceAddress', RULES(
                        '__rule__', DATA(six.text_type)),
                    'ActualAddressPlace', RULES(
                        '__rule__', DATA(six.text_type)),
                    'ActualAddressStreet', RULES(
                        '__rule__', DATA(six.text_type)),
                    'ActualAddressHouse', RULES(
                        '__rule__', DATA(six.text_type)),
                    'ActualAddressFlat', RULES(
                        '__rule__', DATA(six.text_type)),
                    'ActualAddress', RULES(
                        '__rule__', DATA(six.text_type)))),
            'PersonDocuments', RULES(
                '__rule__', MODEL(),
                'Document', RULES(
                    '__rule__', RECORD(),
                    'ID', RULES(
                        '__rule__', DATA(int, m=extractor_rules.extract_document_id)),
                    'PersonRegionalID', RULES(
                        '__rule__', DATA(int)),
                    'PersonLocalID', RULES(
                        '__rule__', DATA(int)),
                    'Person', RULES(
                        '__rule__', DATA(int)),
                    'SourceID', RULES(
                        '__rule__', DATA(int)),
                    'ExternalID', RULES(
                        '__rule__', DATA(int)),
                    'Type', RULES(
                        '__rule__', DATA(six.text_type, m=unbinded2none)),
                    'Series', RULES(
                        '__rule__', DATA(six.text_type)),
                    'Number', RULES(
                        '__rule__', DATA(six.text_type)),
                    'Issuer', RULES(
                        '__rule__', DATA(six.text_type)),
                    'IssueDate', RULES(
                        '__rule__', DATA(date)))))))
