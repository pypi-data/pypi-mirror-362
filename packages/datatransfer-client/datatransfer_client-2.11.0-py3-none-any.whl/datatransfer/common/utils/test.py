# coding: utf-8

u"""Базовый функционал тестирования пакетов в системах."""

from __future__ import absolute_import

from collections import Iterable
from traceback import format_exc
import contextlib
import functools
import os
import shutil
import tempfile

from django.test import TestCase
from lxml import etree
from six.moves import zip_longest

from datatransfer.common.helpers import get_error


class PacketTestCase(TestCase):

    u"""Доработанный TestCase Django.

    - Позволяет сравнивать xml-пакеты datatransfer между собой.
    """

    def assertXMLFilesEqual(self, a, b):
        u"""Сравнивает 2 xml файла.

        Данная реализация опирается на то, что у элементов с одинаковыми
        тегами, встречающимися несколько раз, есть тег ID.

        Вывод ошибки сделан насколько возможно подробно.

        Для xml, сгенерированной по маппингу не подходит стандартный метод
        сравнения xml, т.к. он:
         - Не выдаёт внятных результатов сравнения.
         - Не учитывает, что порядок элементов может различаться.
        """
        try:
            check_packet_tuples_equal(packet_to_tuples(a), packet_to_tuples(b))
        except CheckFailure as e:
            msg = get_error(e)
            self.fail(msg)

    def assertOnlyElementsNotEmpty(self, xml_filename, tags, msg):
        u"""Проверяет, что в xml-пакете только элементы `tags` не пусты.

        :param xml_filename: имя файла
        :param tags: список тегов ожидаемых элементов.
        :param msg: сообщение об ошибке.
        """
        with open(xml_filename) as f:
            tree = etree.parse(f)
        root = tree.getroot()
        data = root.find('Data')
        for i, block in enumerate(list(data)):
            if block.tag in tags:
                self.assertNotEqual(
                    len(list(block)), 0,
                    msg + u"{} is empty".format(block.tag)
                )
            else:
                self.assertEqual(
                    len(list(block)), 0,
                    msg + u"{} is not empty".format(block.tag)
                )


def xml_to_tuples(element):
    u"""Возвращает представление xml в виде кортежей."""
    children = list(element)

    if not children:
        return element.tag, element.text

    return element.tag, tuple(xml_to_tuples(child) for child in children)


def packet_to_tuples(filename):
    u"""Возвращает представление xml-файла в виде кортежей."""
    with open(filename) as f:
        tree = etree.parse(f, parser=etree.XMLParser(remove_comments=True))
    return xml_to_tuples(tree.getroot())


@contextlib.contextmanager
def temp_dir():
    u"""Контекстный менеджер для временной директории."""
    dirname = tempfile.mkdtemp()
    dirname = os.path.realpath(dirname)
    try:
        yield dirname
    finally:
        shutil.rmtree(dirname)


class CheckFailure(AssertionError):

    u"""Исключение, выбрасываемое при проваленной проверке xml пакета."""


def check_packet_tuples_equal(a, b, path=''):
    u"""Проверяет на равенство кортежные представления xml a и b.

    :param a: Первое сравниваемое представление.
    :param b: Второе сравниваемое представление.
    :param path: путь к элементу xml. При рекурсивной обработке к каждому
                 вложенному вызову добавляется через слэш имя текущего тега.
    :return: Возвращает None, если представления равны, иначе описание ошибки.
    :rtype: unicode or None
    """
    def nested_elements(a, b):
        u"""Вызывается, когда элементы содержат вложенные теги."""
        a_tag, a_children = a
        b_tag, b_children = b
        if a_tag != b_tag:
            raise CheckFailure(
                u'Имена тегов не равны ({path}/): {0} != {1}'.format(
                    a[0], b[0], path=path
                )
            )

        def get_id(element_tuple):
            u"""Возвращает значение тега id или None."""
            if isinstance(element_tuple[1], Iterable):
                for child in element_tuple[1]:
                    if child and child[0] == 'ID':
                        return child[1]

        a_ids = tuple(get_id(x) for x in a_children)
        b_ids = tuple(get_id(x) for x in b_children)
        if any(a_ids) or any(b_ids):
            if (
                len(set(a_children)) != len(a_children) or
                len(set(b_children)) != len(b_children)
            ):
                raise CheckFailure(
                    u'Обнаружены повторяющиеся id: '
                    u'{0}/{1}'.format(path, a[0])
                )
            # Проверяем, что количество дочерних элементов равно
            if len(a_children) != len(b_children):
                raise CheckFailure(
                    u'Количество вложенных элементов различно: '
                    u'{0}/{1}\n{2}\n{3}'.format(
                        path, a[0], a_children, b_children
                    )
                )
            if all(a_ids) and all(b_ids):
                a_child_id_map = {get_id(x): x for x in a_children}
                b_child_id_map = {get_id(x): x for x in b_children}

                a_ids = set(a_child_id_map.keys())
                b_ids = set(b_child_id_map.keys())

                if a_ids - b_ids:
                    raise CheckFailure(
                        u'ID вложенных элементов не совпадают '
                        u'({path}):\n{0}\n{1}'.format(
                            u'first_id_set - second_id_set: {0}'.format(
                                a_ids - b_ids),
                            u'second_id_set - first_id_set: {0}'.format(
                                b_ids - a_ids),
                            path=u'{}/{}'.format(path, a_tag)
                        )
                    )
                child_keys = sorted(a_child_id_map.keys())
                a_ordered_children = tuple(
                    a_child_id_map[k] for k in child_keys
                )
                b_ordered_children = tuple(
                    b_child_id_map[k] for k in child_keys
                )
            else:
                raise CheckFailure(
                    u'Не у всех элементов указан тег ID: {}/{}'.format(
                        path, a_tag
                    )
                )
        else:
            a_ordered_children = sorted(a_children)
            b_ordered_children = sorted(b_children)

        for child_a, child_b in zip_longest(a_ordered_children,
                                             b_ordered_children):
            check_packet_tuples_equal(
                child_a, child_b, path + u'/' + a_tag
            )

    if a and b and isinstance(a[1], tuple) and isinstance(b[1], tuple):
        nested_elements(a, b)
    else:
        # Случай, когда один из вложенных тегов не кортеж.
        if not a and b:
            raise CheckFailure(
                u'Тег отсутствует в первом xml: {}/{}'.format(
                    path, b[0]
                )
            )
        if not b and a:
            raise CheckFailure(
                u'Тег отсутствует во втором xml: {}/{}'.format(
                    path, a[0]
                )
            )
        if a[0] != b[0]:
            raise CheckFailure(
                u'Названия элементов не равны ({}): {} != {}'.format(
                    path, a[0], b[0]
                )
            )
        if a[1] != b[1]:
            raise CheckFailure(
                u'Значения элементов не равны ({}/{}): {} != {}'.format(
                    path, a[0], a[1], b[1]
                )
            )


def fail_on(exc):
    u"""Декоратор, перенаправляющий в тесте исключение в ошибку."""

    def create_wrapper(method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            try:
                result = method(self, *args, **kwargs)
            except exc:
                self.fail(format_exc().decode('unicode-escape'))
            return result

        return wrapper

    return create_wrapper
