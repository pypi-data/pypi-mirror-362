# coding: utf-8
from __future__ import absolute_import

from contextlib import closing
import datetime

from django.db import connection
from educommon.contingent.contingent_plugin import models as educommon_models
from m3_django_compat import atomic

from datatransfer.common.constants import MODE_UPDATED
from datatransfer.common.helpers import get_packet
from datatransfer.source import configs as dt_settings
from datatransfer.source.etl.packet.extractor.common.mapping import rules


def create_export_packet(out_dir, session_id, mode, clear_change_list=True):
    u"""Создаёт xml с выгрузкой данных из РИС в РС.

    :param basestring out_dir: Путь к папке, в которую будет записан xml файл.
    :param int session_id: Id сессии, в которой производится выгрузка.
    :param int mode: Режим выгрузки - MODE_UPDATED или MODE_ALL.
    :param bool clear_change_list: Флаг сброса данных об измененных моделях.
           Если `True`, то следующая выгрузка обновленных данных (MODE_UPDATED)
           будет пустая.
           Если `False`, то следующая выгрузка будет такая же как текущая.

    :rtype basestring
    :return: Путь к созданному xml файлу выгрузки.
    """
    if mode == MODE_UPDATED:
        connection.close()
        if hasattr(connection, 'connect'):
            connection.connect()

    with atomic():
        if mode == MODE_UPDATED:
            # Устанавливаем в транзакции уровень изоляции 'repeatable read',
            # чтобы изменения в модели наблюдателя за обновлением данных
            # не влияли на выгрузку.
            with closing(connection.cursor()) as cursor:
                cursor.execute(
                    'set transaction isolation level repeatable read'
                )

        packet_path = get_packet(
            rules,
            out_dir,
            prefix=dt_settings.SMEV_MNEMONICS,
            session_id=session_id,
            source_system_id=dt_settings.SMEV_MNEMONICS,
            authorization_key=dt_settings.DATATRANSFER_AUTHORIZATION_KEY,
            destination_system_id=dt_settings.DATATRANSFER_MNEMONICS,
            timestamp=datetime.datetime.now(),
            mode=mode
        )
        if clear_change_list:
            with connection.cursor() as c:
                c.execute('DELETE FROM "{}"'.format(
                    educommon_models.ContingentModelChanged._meta.db_table))
                if hasattr(educommon_models, 'ContingentModelDeleted'):
                    c.execute('DELETE FROM "{}"'.format(
                        educommon_models.ContingentModelDeleted._meta.db_table))
        return packet_path
