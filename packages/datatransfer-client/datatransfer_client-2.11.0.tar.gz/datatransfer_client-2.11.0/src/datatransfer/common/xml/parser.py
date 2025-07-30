# coding: utf-8

from __future__ import absolute_import

from collections import OrderedDict
from datetime import date
from datetime import datetime

import six
from django.utils.dateparse import parse_date
from django.utils.dateparse import parse_datetime
from lxml import etree
from six.moves import zip


def type_mapping_helper(s, converter):
    if s is None:
        return None

    return converter(s)


class XMLModelParser(object):
    TYPE_MAPPING = {
        six.text_type: lambda s: s,
        int: lambda s: type_mapping_helper(s, int),
        float: lambda s: type_mapping_helper(s, float),
        datetime: lambda s: type_mapping_helper(s, parse_datetime),
        date: lambda s: type_mapping_helper(s, parse_date)}


    stack = None
    rule = None
    mapping = None

    def __init__(self, mapping):
        self.stack = []
        self.rule = []

        self.mapping = mapping

    @staticmethod
    def rules(*a):
        return OrderedDict(zip(*[iter(a)] * 2))

    @staticmethod
    def model(y=False):
        return (True, False, None, None, y)

    @staticmethod
    def record(a=True, y=True):
        return (False, a, None, None, y)

    @staticmethod
    def data(t, m=None, y=False):
        return (True, False, t, m, y)

    def parse(self, xml_file, encoding='utf-8', only_data=True):
        for (event, element) in etree.iterparse(xml_file, events=('start', 'end'), huge_tree=True, encoding=encoding):
            parent = element.getparent()

            if event == 'start':
                self.rule.append(
                    self.rule and self.rule[-1][element.tag] or self.mapping[element.tag])

                (required, multiple, data_type, data_mapping, data_yield) = self.rule[-1]['__rule__']

                data = {element.tag: None}

                if parent is not None:
                    if multiple:
                        if self.stack[-1][parent.tag] and not data_yield:
                            self.stack[-1][parent.tag].append(data)
                        else:
                            self.stack[-1][parent.tag] = [data]
                    else:
                        if self.stack[-1][parent.tag]:
                            self.stack[-1][parent.tag].update(data)
                            data = self.stack[-1][parent.tag]
                        else:
                            self.stack[-1][parent.tag] = data

                self.stack.append(data)
            else:
                (required, multiple, data_type, data_mapping, data_yield) = self.rule[-1]['__rule__']

                if data_type:
                    value = data_type and self.TYPE_MAPPING[data_type](element.text)

                    if data_mapping:
                        if isinstance(data_mapping, dict):
                            value = data_mapping[value]
                        elif callable(data_mapping):
                            value = data_mapping(value)

                    self.stack[-1][element.tag] = value

                if data_yield:
                    yield (element.getroottree().getpath(element), self.stack[only_data and -1 or 0])

                    del self.stack[-1][element.tag]

                element.clear()

                self.stack.pop()
                self.rule.pop()
