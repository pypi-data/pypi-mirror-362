# coding: utf-8

from __future__ import absolute_import

from django.db import connections, router

from datatransfer.source.get_data.models import GetDataPerson


def _get_cursor(instance=None):
    u"""Возвращает курсор для работы с БД.
    :param instance: необязательный параметр, для более точного
        отпределения инстанса соединения.
    :return: inst CursorWrapper
    """
    return connections[router.db_for_write(
        GetDataPerson, instance=instance)].cursor()


def create_temp_table(source):
    u"""Создаёт временную таблицу, построенную по схеме исходной."""
    table = 'get_data_tmp_{}'.format(source)

    cursor = _get_cursor()
    sql = (
        'CREATE TEMP TABLE {}(LIKE {} '
        'INCLUDING INDEXES INCLUDING CONSTRAINTS) ON COMMIT DROP;'
    )
    cursor.execute(sql.format(table, source))
    # Выполняем подмену sequence для id.
    # Это позволит нам при удалении дублей по source_id и external_id
    # оставить последние добавленные записи.
    # Результат будет тот же самый, что при последовательном
    # get_or_create.
    sql = (
        'CREATE TEMP SEQUENCE {table}_seq OWNED BY {table}.id;\n'
        'ALTER TABLE {table} ALTER COLUMN id '
        'SET DEFAULT nextval(\'{table}_seq\'::regclass);'
    )
    cursor.execute(sql.format(table=table))
    cursor.close()
    return table


def clear_tables(*tables):
    u"""Очищает таблицы (TRUNCATE).

    Сбрасывает sequences для полей.
    """
    sql = 'TRUNCATE TABLE {} RESTART IDENTITY;'.format(', '.join(tables))
    cursor = _get_cursor()
    cursor.execute(sql)
    cursor.close()


class DocumentWithoutPersonException(Exception):

    u"""Исключение: документ не связан с физ лицом.

    Происходит, когда в xml указан PersonId и SourceId такого физ. лица,
    которого нет в xml.
    """

    def __init__(self, external_id, source_id):
        super(DocumentWithoutPersonException, self).__init__(
            u'Документу физ. лица переданного из КО не соответствует ни одно'
            u'физ. лицо\n ExternalId={}, SourceId={}.'.format(
                external_id, source_id
            )
        )


def update_persons_ids(document_table):
    u"""Создаёт в таблице документов ссылки на GetDataPerson.

    В person_id при загрузке документов помещается external_id физ. лица.
    После загрузки во временную документу необходимо связать документ
    с сохраненным физ. лицом по FK.
    """
    cursor = _get_cursor()
    # Проверяем, что документы можно связать с физ. лицом.
    params = dict(
        doc_table=document_table,
        person_table=GetDataPerson._meta.db_table
    )
    sql = (
        'SELECT d.person_id, d.source_id '
        'FROM {doc_table} d LEFT JOIN {person_table} p '
        'ON d.person_id = p.external_id '
        '      AND d.source_id = p.source_id '
        'WHERE p.id IS NULL '
        'LIMIT 1;'
    )
    cursor.execute(sql.format(**params))

    document_without_person = cursor.fetchone()
    if document_without_person:
        raise DocumentWithoutPersonException(*document_without_person)
    # Обновляем ссылки на GetDataPerson.
    sql = (
        'UPDATE {doc_table} SET person_id=p.id FROM {person_table} p '
        'WHERE {doc_table}.person_id=p.external_id '
        '      AND {doc_table}.source_id=p.source_id;'
    )
    cursor.execute(sql.format(**params))
    cursor.close()


class Loader(object):

    u"""Загрузчик данных в БД."""

    def __init__(self, table, fields):
        self._target_table = table
        self.temp_table = create_temp_table(table)
        self._fields = fields
        self._cursor = _get_cursor()

    def insert(self, record):
        u"""Добавляет запись."""
        sql = (
            'INSERT INTO {target} ({columns}) VALUES ({values});'
        ).format(
            target=self.temp_table,
            values=', '.join(('%s',) * len(self._fields)),
            columns=', '.join(self._fields)
        )
        self._cursor.execute(sql, record)

    def _copy(self):
        u"""Выполняет копирование из временной базы в целевую.

        Из записей с равными source_id и external_id будет загружена
        только последняя.
        """
        sql = (
            'INSERT INTO {target} ({columns}) '
            'SELECT DISTINCT ON (source_id, external_id) {columns} '
            'FROM {source} ORDER BY source_id, external_id, id DESC;'
        ).format(
            target=self._target_table,
            source=self.temp_table,
            columns=', '.join(self._fields)
        )
        self._cursor.execute(sql)

    def close(self):
        self._copy()
        self._cursor.close()
