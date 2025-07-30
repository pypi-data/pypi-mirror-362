# coding: utf-8

from django.test import TransactionTestCase

from datatransfer.common.constants import (
    MODE_ALL,
    MODE_UPDATED,
)
from datatransfer.source.utils import create_export_packet
from test_project.system.models import Example
from utils import (
    packet_to_tuples,
    temp_dir,
)


class ToRSTestCase(TransactionTestCase):

    u"""Тесты выгрузки данных в РС КО.

    SimpleTestCase выбран из-за того, что ``create_export_packet`` пересоздает
    подключение к БД и транзация откатывается с ошибкой в  ``TestCase`` и
    ``TransactionTestCase``.
    """

    allow_database_queries = True

    def tearDown(self):
        u"""Очищает БД явно."""
        Example.objects.all().delete()
        super(ToRSTestCase, self).tearDown()

    @staticmethod
    def process_mapping(updated=True, clear=True):
        with temp_dir() as out_dir:
            xml_file_name = create_export_packet(
                out_dir, 1,
                MODE_UPDATED if updated else MODE_ALL,
                clear
            )
            result = packet_to_tuples(xml_file_name)
            return result

    def test_full(self):
        Example.objects.create(name='First', number=111)
        Example.objects.create(name='Second', number=222)
        self.assertEquals(
            self.process_mapping(False),
            ('Examples', (
                ('Example', (('NameTag', 'First'), ('NumberTag', '111'))),
                ('Example', (('NameTag', 'Second'), ('NumberTag', '222')))
            ))
        )

    def test_updated(self):
        # Первичная выгрузка
        Example.objects.create(name='First', number=111)
        Example.objects.create(name='Second', number=222)
        self.assertEquals(
            self.process_mapping(),
            ('Examples', (
                ('Example', (('NameTag', 'First'), ('NumberTag', '111'))),
                ('Example', (('NameTag', 'Second'), ('NumberTag', '222')))
            ))
        )

        # Выгрузка только обновленных данных
        Example.objects.create(name='Third', number=333)
        self.assertEquals(
            self.process_mapping(),
            ('Examples', (
                ('Example', (('NameTag', 'Third'), ('NumberTag', '333'))),
            ))
        )

    def test_updated_no_clean(self):
        # Выгрузка только обновленных данных
        Example.objects.create(name='Any', number=19)
        expected = ('Examples', (
            ('Example', (('NameTag', 'Any'), ('NumberTag', '19'))),
        ))
        self.assertEquals(self.process_mapping(clear=False), expected)

        # Повторная выгрузка только обновленных данных должна соответствовать
        # предыдущей
        self.assertEquals(self.process_mapping(clear=False), expected)
