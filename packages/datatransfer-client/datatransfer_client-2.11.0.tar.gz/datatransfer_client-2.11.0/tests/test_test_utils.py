# coding: utf-8

u"""Тесты функции, тестирующей пакеты."""

import six

from django.test import TestCase

from datatransfer.common.utils.test import (
    CheckFailure,
    check_packet_tuples_equal,
)


class BaseTuplesCheckerTest(TestCase):

    u"""Базовый тест-кейс для тестирования функции проверки."""

    def _test_exception(self, a, b, message):
        u"""Проверяет что при вызове функции будет исключение.

        Если исключение не вызвано, либо сообщение отличается от
        указанного в аргументе, то тест завершится с ошибкой.

        :param tuple a: Первый кортеж для сравнения.
        :param tuple b: Второй кортеж для сравнения.
        :param basestring message: Ожидаемое сообщение об ошибке.
        """
        with self.assertRaises(CheckFailure) as cm:
            check_packet_tuples_equal(a, b)

        if six.PY2:
            exc_message = cm.exception.message.decode('utf-8')
        else:
            exc_message = str(cm.exception)

        self.assertEqual(
            exc_message,
            message
        )


class StandardTestCase(BaseTuplesCheckerTest):

    u"""Тест-кейс для проверки корректности сравнения элементов."""

    def test_not_equals(self):
        u"""Проверка, неравных тегов у элементов."""
        a = ('tag', ())
        b = ('another_tag', ())

        self._test_exception(
            a, b, u'Имена тегов не равны (/): tag != another_tag'
        )

    def test_not_found(self):
        u"""Проверяет сравнение при отсутствующем теге."""
        a = ('tag', (('inner_tag', 0),))
        b = ('tag', ())

        self._test_exception(
            a, b, u'Тег отсутствует во втором xml: /tag/inner_tag'
        )
        self._test_exception(
            b, a, u'Тег отсутствует в первом xml: /tag/inner_tag'
        )

    def test_values_not_equal(self):
        u"""Проверяет сравнение значений."""
        a = ('tag', (('inner_tag', 0),))
        b = ('tag', (('inner_tag', 1),))

        self._test_exception(
            a, b, u'Значения элементов не равны (/tag/inner_tag): 0 != 1'
        )

        self._test_exception(
            b, a, u'Значения элементов не равны (/tag/inner_tag): 1 != 0'
        )


class IdTestCase(BaseTuplesCheckerTest):

    u"""Тест-кейс для проверки вложенных элементов, сопостовляемых по id."""

    def test_not_all_have_id(self):
        u"""Проверяет, что все элементы имеют ID, если хотя бы один имеет."""
        a = (
            'Blocks', (
                ('Block', (('ID', 1), ('Name', 'Element name'))),
                ('Block', (('ID', 2), ('Name', 'Element name')))
            )
        )
        b = (
            'Blocks', (
                ('Block', (('ID', 1), ('Name', 'Element name'))),
                ('Block', (('Name', 'Element name')))
            )
        )
        self._test_exception(
            a, b, u'Не у всех элементов указан тег ID: /Blocks'
        )
        self._test_exception(
            b, a, u'Не у всех элементов указан тег ID: /Blocks'
        )

    def test_duplicate_id(self):
        u"""Проверяет, что исключение выбрасывается при повторяющихся ID."""
        a = (
            'Blocks', (
                ('Block', (('ID', 1), ('Name', 'Element name'))),
                ('Block', (('ID', 2), ('Name', 'Element name'))),
                ('Block', (('ID', 2), ('Name', 'Element name'))),
            )
        )
        b = (
            'Blocks', (
                ('Block', (('ID', 1), ('Name', 'Element name'))),
                ('Block', (('ID', 1), ('Name', 'Element name'))),
                ('Block', (('ID', 2), ('Name', 'Element name')))
            )
        )
        ok_b = (
            'Blocks', (
                ('Block', (('ID', 1), ('Name', 'Element name'))),
                ('Block', (('ID', 2), ('Name', 'Element name'))),
                ('Block', (('ID', 3), ('Name', 'Element name')))
            )
        )
        self._test_exception(
            a, b, u'Обнаружены повторяющиеся id: /Blocks'
        )
        self._test_exception(
            b, a, u'Обнаружены повторяющиеся id: /Blocks'
        )
        self._test_exception(
            a, ok_b, u'Обнаружены повторяющиеся id: /Blocks'
        )
        self._test_exception(
            ok_b, a, u'Обнаружены повторяющиеся id: /Blocks'
        )

    def test_different_size(self):
        u"""Проверяет исключение при различном кол-ве элементов с ID."""
        a = (
            'Blocks', (
                ('Block', (('ID', 1), ('Name', 'Element name'))),
                ('Block', (('ID', 2), ('Name', 'Element name'))),
            )
        )
        b = (
            'Blocks', (
                ('Block', (('ID', 1), ('Name', 'Element name'))),
            )
        )
        self._test_exception(
            a, b, u'Количество вложенных элементов различно:'
                  u' /Blocks\n{}\n{}'.format(a[1], b[1])
        )
        self._test_exception(
            b, a, u'Количество вложенных элементов различно:'
                  u' /Blocks\n{}\n{}'.format(b[1], a[1])
        )

    def test_id_not_equal(self):
        u"""Проверяет, что исключение выбрасывается при различных ID."""
        a = (
            'Blocks', (
                ('Block', (('ID', 1), ('Name', 'Element name'))),
            )
        )
        b = (
            'Blocks', (
                ('Block', (('ID', 2), ('Name', 'Element name'))),
            )
        )
        self._test_exception(
            a, b, (
                u'ID вложенных элементов не совпадают (/Blocks):\n'
                u'first_id_set - second_id_set: {0}\n'
                u'second_id_set - first_id_set: {1}'.format(
                    {1}, {2}
                )
            )
        )
        self._test_exception(
            b, a, (
                u'ID вложенных элементов не совпадают (/Blocks):\n'
                u'first_id_set - second_id_set: {0}\n'
                u'second_id_set - first_id_set: {1}'.format(
                    {2}, {1}
                )
            )
        )
