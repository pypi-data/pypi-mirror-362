# coding: utf-8

from __future__ import absolute_import

from collections import OrderedDict
from contextlib import contextmanager
from datetime import datetime
import os

from django.db import connection
from lxml import etree
from lxml import objectify
from petl.io.sources import ZipSource
from petl.transform.maps import fieldmap
from six.moves import range
from six.moves import zip
import six

from .utils import xml_escape
from datatransfer.source.configs import XSD_FILE_PATH


EMPTY = (None, '')
UNBIND = ('-1', -1)
FALSE = (0, '0', False)


def get_error(exc):
    """Хелпер, возвращающий описание Exception в
    python2 и python3"""
    if hasattr(exc, 'message'):
        try:
            error = six.text_type(exc.message)
        except UnicodeDecodeError:
            error = exc.message.decode('UTF-8')
    else:
        error = str(exc)
    return error


def SKIP(_):
    return True


def row(value):
    return value


def just(value):
    return lambda _: value


def maybe(mapping, value=None):
    return lambda v: mapping.get(v, value)


def first(mapping, value=None):
    return lambda arr: mapping.get(min(arr), value) if arr else None


def ns(namespace, element):
    return "{{{0}}}{1}".format(
            namespace, element)


def d(value):
    return value and value.date().isoformat() or None


def dt(value):
    return value and datetime.combine(value, datetime.min.time()).isoformat() or None


class Hidden(object):

    def __len__(self):
        return 0


def simple_serializer(obj):
    return objectify.DataElement(xml_escape(obj)).text or ''


class VirtualQuerySetWrapper(object):
    """Обертка для RawQuerySet.
    Имитирует поведение методов values_list и iterator.
    Позволяет использовать RawQuerySet в функции fromorm."""

    def __init__(self, rows):
        self.rows = rows

    def values_list(self, *fields):
        return self

    def iterator(self):
        for row in self.rows:
            yield row


class RawQuerySetWrapper(object):
    """Обертка для RawQuerySet.
    Имитирует поведение методов values_list и iterator.
    Позволяет использовать RawQuerySet в функции fromorm."""

    def __init__(self, model, options):
        self.model = model
        self.options = options
        self.fields = []

    def values_list(self, *fields):
        self.fields = fields

        return self

    def iterator(self):
        for row in self.model.objects.raw(*self.options):
            yield tuple([getattr(row, column) for column in self.fields])


def fromorm(qs, *fields):
    """Обертка для Django ORM QuerySet"""

    yield fields

    for row in qs.values_list(*fields).iterator():
        yield row


@contextmanager
def xfelement(xf, obj):
    if obj:
        if isinstance(obj, tuple):
            obj, opts = obj
        else:
            obj, opts = obj, {}

        with xf.element(obj, **opts):
            yield
    else:
        yield


def process_mapping(mapping, **kwargs):
    u"""Процессинг маппинга"""

    if callable(mapping):
        mapping = mapping(**kwargs)

    for (model, record, variants) in mapping:
        skip_header = False

        for (qs, rules) in variants:
            _rules = OrderedDict()
            options = []
            for rule_item in rules:
                k = rule_item[0]
                v = rule_item[1]

                if not k:
                    k = Hidden()

                _rules[k or Hidden()] = v

                options.append(rule_item[2:])

            fields = []

            for v in six.itervalues(_rules):
                if isinstance(v, str):
                    fields.append(v)
                elif isinstance(v, tuple) and len(v) == 2:
                    fields.append(v[0])

            header = True

            for row in fieldmap(fromorm(qs, *fields), _rules, True):
                if not (header and skip_header):
                    yield (model, record, row, options)

                header = False

            skip_header = True

        yield None


def fields_writer(xf, serializer, header, row, options, **kwargs):
    for (field, data, options) in zip(header, row, options):
        try:
            optionality_config = options[0]
        except IndexError:
            pass
        else:
            if isinstance(optionality_config, tuple):
                if data in optionality_config:
                    continue

            if callable(optionality_config):
                if optionality_config(data):
                    continue

        try:
            nested = options[1]
        except IndexError:
            nested = None

        if nested:
            with xfelement(xf, field):
                model_writer(xf, serializer, process_mapping(
                    nested(data, **kwargs), **kwargs), **kwargs)
        else:
            with xfelement(xf, field):
                xf.write(serializer(data))


def record_writer(xf, serializer, header, data, options, **kwargs):
    (model, record, row, options) = data

    with xfelement(xf, record):
        fields_writer(xf, serializer, header, row, options, **kwargs)


def model_writer(xf, serializer, iterator, **kwargs):
    for (model, record, header, options) in iterator:
        with xfelement(xf, model):
            for data in iterator:
                if data is None:
                    break
                record_writer(xf, serializer, header, data, options, **kwargs)


def validate_xml_by_xsd(xsd_name, xml_name):
    """Валидация XML файла по XSD шаблону.

    Если валидация неуспешна - функция выкинет exception

    :param xsd_name: имя XSD шаблона для валидации
    :param xml_name: имя валидируемового XML файла
    """
    xmlschema_xsd = etree.parse(xsd_name)
    xmlschema = etree.XMLSchema(xmlschema_xsd)
    doc = etree.parse(xml_name)
    xmlschema.assertValid(doc)


def toxml(iterator, destination, encoding='utf-8', serializer=None, **kwargs):
    """Потоковая генерация XML"""

    if serializer is None:
        serializer = simple_serializer

    try:
        with etree.xmlfile(destination, encoding=encoding) as xf:
            xf.write_declaration()
            model_writer(xf, serializer, iterator, **kwargs)

    # FIXME: lxml падает при закрытии большого файла
    except etree.SerialisationError:
        pass


def get_packet(rules, files_destination, file_name=None, prefix=None, **kwargs):
    u"""Формирует XML с данными и возвращает путь до неё.

    :param rules: Маппинг или callable, возвращающий маппинг.
    :param file_name: Имя создаваемого xml-файла.
    :param prefix: Если file
    :param files_destination: путь по кторому хранятся файлы
    :return: /full/path/to/xml,
    """

    if file_name is None:
        file_name = "{MNEMONIC}_{DATETIME}.xml".format(
            MNEMONIC=prefix,
            DATETIME=datetime.now().strftime("%Y%m%d_%H%M%S"))

    xml_filename = os.path.join(files_destination, file_name)

    serializer = None

    if callable(rules):
        rules_config = rules(**kwargs)
    else:
        rules_config = rules

    if isinstance(rules_config, dict):
        packet_mapping = rules_config['packet_mapping']
        serializer = rules_config.get('serializer')
    else:
        packet_mapping = rules

    toxml(process_mapping(packet_mapping), xml_filename,
          serializer=serializer, **kwargs)

    if XSD_FILE_PATH:
        validate_xml_by_xsd(XSD_FILE_PATH, xml_filename)

    return xml_filename


# TODO переписать на классы - Reader, Modifier, Writer

def get_record(element, tags, modify_data=None, session_id=None):
    u"""Возвращает данные записи, извлеченные из XML-элемента.

    :param element: XML-элемент
    :type element: lxml.etree._Element
    :param tags: Перечень тегов с наименованием и признаком обязательности
    :type tags: list[tuple]
    :param modify_data: Функция изменяющая данные
    :type modify_data: function
    :param session_id: ID сессии
    :type session_id: int
    :return: Запись с данными
    :rtype: None or list
    """
    data = []
    for tag in tags:
        tag_name, is_required, default_value = tag
        el = element.xpath(tag_name) if tag_name else None
        if (not el or len(el) != 1) and is_required:
            return None
        value = el[0].text if el else default_value
        data.append(value)
    if session_id:
        data += [session_id]
    if modify_data:
        modify_data(data)
    return data


def get_records(archive_filename, xml_filename, tag_name, tags,
                modify_data=None, session_id=None):
    u"""Возвращает записи исходного файла в виде строк.

    :param archive_filename:    Имя файла-архива.
    :param xml_filename:        Имя XML-файла.
    :param tag_name:            Название тега.
    :param tags: Перечень тегов с наименованием и признаком обязательности
    :param modify_data:         Функция изменяющая данные.
    :param session_id:          ID сессии.

    :rtype: generator of unicode
    """
    with ZipSource(archive_filename, xml_filename).open('r') as xml_file:
        for event, element in etree.iterparse(xml_file, tag=tag_name):
            record = get_record(element, tags, modify_data, session_id)
            if not record:
                continue
            yield record


class RecordsAdapter(object):
    u"""Адаптор для использования функции-генератора строк в качестве file-like object"""

    def __init__(self, data):
        self._data = data

    def convert_data_to_string(self, data):
        modified_data = ['\\N' if i is None else six.text_type(i) for i in data]
        return '\t'.join(modified_data)

    def readline(self, size):
        return self.convert_data_to_string(next(self._data)) + '\n'

    def read(self, size):
        return '\n'.join(self.convert_data_to_string(data) for data in self._data)


def write_data(archive_filename, xml_filename, tag_name, tags,
               table_name, modify_data=None, session_id=None, columns=None,
               with_truncate=False):
    u"""Записывает в таблицу данные, считанные из XML-файла по заданному тегу.

    :param archive_filename:    Имя файла-архива.
    :param xml_filename:        Имя XML-файла.
    :param tag_name:            Название тега.
    :param tags:                Перечень тегов с наименованием и признаком обязательности.
    :param table_name:          Наименование таблицы для сохранения данных.
    :param modify_data:         Функция изменяющая данные.
    :param session_id:          ID сессии.
    :param columns:             Названия колонок таблицы.
    :param with_truncate:       Необходимость очистки таблицы перед записью туда данных.
    """
    records = get_records(
        archive_filename, xml_filename, tag_name, tags, modify_data, session_id
    )
    with connection.cursor() as cursor:
        if with_truncate:
            cursor.execute('TRUNCATE {};'.format(table_name))
        cursor.copy_from(RecordsAdapter(records), table_name, columns=columns)


def make_fullname(surname=None, firstname=None, patronymic=None):
    """
    Склеивание фамилии, имени и отчества.

    Капитализируем только первую букву каждой части
    """
    vals = (
        (surname or '').capitalize(),
        (firstname or '').capitalize(),
        (patronymic or '').capitalize()
    )
    return ' '.join(x for x in vals if x)
