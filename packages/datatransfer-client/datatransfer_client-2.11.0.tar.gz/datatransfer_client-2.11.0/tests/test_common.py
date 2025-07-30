# coding: utf-8

from unittest import skip
import os

from django.test import TestCase

from datatransfer.common.helpers import (
    VirtualQuerySetWrapper,
    get_packet,
)
from test_project.system.models import Example
from utils import (
    packet_to_tuples,
    temp_dir,
)


class GetPacketTestCase(TestCase):

    u"""Тест функции, преобразующей маппинг в xml."""

    _stub_rules = (
        ('Examples', None, [(
            VirtualQuerySetWrapper([(1,)]), (
                ('NameTag', '', None, None),
            )
        )]),
    )

    def test_qs_wrapper(self):
        u"""Проверяет корректность работы с VirtualQuerySetWrapper."""
        rules = (
            ('Packet', None, [(
                VirtualQuerySetWrapper([(1, 2)]), (
                    ('Tag1', 'foo', None, None),
                    ('Tag2', 'bar', None, None),
                ),
            )]),
        )

        with temp_dir() as out_dir:
            xml_file_name = get_packet(rules, out_dir)
            result = packet_to_tuples(xml_file_name)
            expected = ('Packet', (('Tag1', '1'), ('Tag2', '2')))
            self.assertEquals(result, expected)

    def test_model(self):
        u"""Проверяет корректноcть работы с моделями."""
        rules = (
            ('Examples', 'Example', [(
                Example.objects.all(), (
                    ('NameTag', 'name', None, None),
                    ('NumberTag', 'number', None, None)
                )
            )]),
        )

        Example.objects.create(name='First', number=111)
        Example.objects.create(name='Second', number=222)

        with temp_dir() as out_dir:
            xml_file_name = get_packet(rules, out_dir)
            result = packet_to_tuples(xml_file_name)

            expected = ('Examples', (
                ('Example', (('NameTag', 'First'), ('NumberTag', '111'))),
                ('Example', (('NameTag', 'Second'), ('NumberTag', '222')))
            ))
            self.assertEquals(result, expected)

    def test_filename_args(self):
        u"""Проверяет аргументы, влияющие на имя файла.

            - prefix - определяет префикс имени файла
            - file_name - определяет имя файла
        """
        rules = self._stub_rules

        with temp_dir() as out_dir:
            prefix = 'xyz345'
            xml_file_name = get_packet(rules, out_dir, prefix=prefix)
            self.assertTrue(prefix in os.path.basename(xml_file_name))

            target_filename = 'result678.xml'
            xml_file_name = get_packet(rules, out_dir, target_filename)
            self.assertEquals(
                xml_file_name, os.path.join(out_dir, target_filename)
            )

    @skip('Incorrect implementation')
    def test_rules_kwargs(self):
        u"""Проверяет правильность передачи аргументов в маппинг."""
        def rules(**kwargs):
            self.assertIn('a', kwargs)
            self.assertEquals(kwargs['a'], 'text')
            self.assertIn('b_id', kwargs)
            self.assertEquals(kwargs['b_id'], 78)
            return self._stub_rules

        with temp_dir() as out_dir:
            get_packet(rules, out_dir, a='text', b_id=78)
