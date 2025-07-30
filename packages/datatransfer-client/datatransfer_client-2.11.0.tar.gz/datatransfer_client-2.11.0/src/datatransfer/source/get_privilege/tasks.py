# coding: utf-8

from __future__ import absolute_import

import datetime
import os
from collections import OrderedDict
from functools import partial

from celery.states import FAILURE
from celery.states import SUCCESS
from datatransfer.common import constants
from datatransfer.common.helpers import get_error
from datatransfer.common.helpers import get_packet
from datatransfer.common.helpers import write_data
from datatransfer.common.utils import archive_xml
from datatransfer.common.utils import encode_archive
from datatransfer.common.utils import register_task
from datatransfer.source import configs as dt_settings
from datatransfer.source.common.configuration import get_object
from django.contrib.contenttypes.models import ContentType
from django.db import connection
from m3_django_compat import atomic

from .etl.packet.extractor.common.mapping import privilege_mapping
from .etl.packet.extractor.common.mapping import rules
from .models import GetPrivilegeSession
from .models import GetPrivilegeStatistic
from .service.client import GetPrivilegeClient
from .utils import move_declarationprivilege_data
from .utils import move_personprivilege_data
from .utils import row_count


# Класс асинхронной задачи
AsyncTask = get_object("task_class")


class GetPrivilegeTask(AsyncTask):
    """Задача - формирующая xml"""

    description = u"Контингент. Запрос данных"
    stop_executing = False
    routing_key = dt_settings.CELERY_ROUTING_KEY

    LOG_TIME_FORMAT = "%d.%m.%Y %H:%M"

    def run(self, *args, **kwargs):
        super(GetPrivilegeTask, self).run(*args, **kwargs)

        packet_mapping = rules

        session_id = kwargs.get('session_id', None) or self.request.id

        today = datetime.date.today()
        now = datetime.datetime.now()

        session = GetPrivilegeSession()
        session.timestamp = now
        session.session = session_id
        session.processed = False
        session.message = ''
        session.save()

        try:
            archive_path = os.path.join(
                dt_settings.STORAGE_MAILBOX_PATH,
                constants.CONFIGURATION_ARCHIVE_OUT,
                str(today.year), str(today.month), str(today.day))

            if not os.path.exists(archive_path):
                os.makedirs(archive_path)

            self.set_progress(
                progress=u"Процесс формирования XML с данными ...",
                values={
                    u"Время начала формирования "
                    u"XML c данными": datetime.datetime.now(
                    ).strftime(self.LOG_TIME_FORMAT)
                }
            )

            filename = get_packet(
                packet_mapping,
                archive_path,
                prefix=dt_settings.SMEV_MNEMONICS,
                session_id=session_id,
                source_system_id=dt_settings.SMEV_MNEMONICS,
                authorization_key=dt_settings.DATATRANSFER_AUTHORIZATION_KEY,
                destination_system_id=dt_settings.DATATRANSFER_MNEMONICS,
                timestamp=now)

            self.set_progress(
                progress=u"Процесс формирования XML c данными окончен",
                values={
                    u"Время окончания процесса "
                    u"формирования XML c данными": datetime.datetime.now(
                    ).strftime(self.LOG_TIME_FORMAT)})

            self.set_progress(
                progress=u"Процесса архивирования XML ...",
                values={
                    u"Время начала процесса "
                    u"архивирования XML": datetime.datetime.now(
                    ).strftime(self.LOG_TIME_FORMAT)
                }
            )
            archive_filename = archive_xml(filename)
            self.set_progress(
                progress=u"Процесс архивирования XML завершен",
                values={
                    u"Время окончания процесса "
                    u"архивирования XML": datetime.datetime.now(
                    ).strftime(self.LOG_TIME_FORMAT)
                }
            )

            try:
                os.remove(filename)
            except OSError as e:
                msg = get_error(e)
                self.set_progress(
                    values={
                        u"Ошибка в процессе "
                        u"удаления файла {0}".format(filename): msg
                    }
                )
            else:
                self.set_progress(
                    values={
                        u"Выполнено удаление XML": u""
                    }
                )

            self.set_progress(
                progress=u"Начало процесса кодирования архива",
                values={
                    u"Время начала процесса "
                    u"кодирования архива": datetime.datetime.now(
                    ).strftime(self.LOG_TIME_FORMAT)
                }
            )
            encoded_file_name = encode_archive(archive_filename)
            self.set_progress(
                progress=u"Конец процесса кодирования архива",
                values={
                    u"Время окончания процесса "
                    u"кодирования архива": datetime.datetime.now(
                    ).strftime(self.LOG_TIME_FORMAT)
                }
            )

            client = GetPrivilegeClient()

            client.GetPrivilege(session_id, encoded_file_name, filename)

            try:
                os.remove(encoded_file_name)
            except OSError as e:
                msg = get_error(e)
                self.set_progress(
                    values={
                        u"Ошибка в процессе "
                        u"удаления временного файла {0}".format(
                            encoded_file_name): msg
                    }
                )
            else:
                self.set_progress(
                    values={
                        u"Выполнено удаление XML": u""
                    }
                )

            self.set_progress(
                progress=u"Формирование прошло успешно",
                task_state=SUCCESS)
        except Exception as e:
            msg = get_error(e)
            session.message = msg
            session.save()
            raise
        return self.state


get_privilege_task = register_task(GetPrivilegeTask())


class GetPrivilegePushTask(AsyncTask):
    u"""Парсинг и сохранение результатов запроса."""

    description = u"Загрузка данных"
    stop_executing = False
    routing_key = dt_settings.CELERY_ROUTING_KEY

    LOG_TIME_FORMAT = "%d.%m.%Y %H:%M"

    # Сопоставление столбцов таблицы с наименованиями тегов, которые парсим.
    # Формат значений словаря:
    #   (column, (tag_name, is_required, default_value))
    PRIVILEGE_COLUMNS_TAGS = OrderedDict((
        ('risid', ('RISID', True, None)),
        ('person_type', (None, False, None)),
        ('exemption', ('Code', True, None)),
        ('expiration_date', ('ExpirationDate', True, None)),
        ('deleted', ('Deleted', False, False)),
        ('deleted_date', ('DeletedDate', False, None)),
    ))

    @property
    def table_columns(self):
        """Перечень наименований столбцов в таблице БД для сохранения данных."""
        return self.PRIVILEGE_COLUMNS_TAGS.keys()

    @property
    def xml_tags(self):
        """Перечень кортежей с тегами, которые парсим."""
        return self.PRIVILEGE_COLUMNS_TAGS.values()

    @atomic
    def run(self, xml_filename, archive_filename, session, *args, **kwargs):
        super(GetPrivilegePushTask, self).run(*args, **kwargs)

        session = GetPrivilegeSession.objects.get(session=session)

        def modify_info(info, risid_idx, exemption_idx, person_type_idx):
            """Функция преобразования данных.

            :param info: Список с данными
            :param risid_idx: Индекс значения risid в данных
            :param exemption_idx: Индекс значения exemption в данных
            :param person_type_idx: Индекс значения person_type в данных
            """
            # ищем пришедшую льготу в локальном справочнике:
            privilege_id = privilege_mapping.get(info[exemption_idx])
            if not privilege_id:
                del info[:]
                return
            info[exemption_idx] = privilege_id
            # В принимаемом значении risid первая цифра содержит
            # тип принадлежности льготы: 1 - персона, 2 - заявление.
            # Последующие - id ученика/заявления в РИС:
            info[person_type_idx] = info[risid_idx][0]
            info[risid_idx] = info[risid_idx][1:]

        # odict_keys to list
        columns = list(self.table_columns)

        modify_info = partial(
            modify_info,
            risid_idx=columns.index('risid'),
            exemption_idx=columns.index('exemption'),
            person_type_idx=columns.index('person_type'),
        )

        self.set_progress(
            progress=u"Процесс распаковки данных ...",
            values={
                u"Время начала распаковки "
                u"данных": datetime.datetime.now(
                ).strftime(self.LOG_TIME_FORMAT)
            }
        )

        write_data(
            archive_filename,
            xml_filename,
            'PersonPrivilege',
            self.xml_tags,
            'get_privilege_getprivilegedata',
            modify_data=modify_info,
            columns=columns,
            with_truncate=True,
        )

        move_personprivilege_data()
        move_declarationprivilege_data()

        models = ['privilege', 'personprivilege', 'declarationprivilege']
        with connection.cursor() as cursor:
            GetPrivilegeStatistic.objects.bulk_create([
                GetPrivilegeStatistic(
                    session=session,
                    model=ContentType.objects.get(
                        app_label='privilege', model=m),
                    count=row_count(cursor, m))
                for m in models])

        self.set_progress(
            progress=u"Конец процесса распаковки данных",
            values={
                u"Время окончания процесса "
                u"распаковки данных": datetime.datetime.now(
                ).strftime(self.LOG_TIME_FORMAT)
            }
        )

        session.processed = True
        session.save()

        self.set_progress(
            progress=u"Загрузка прошла успешно",
            task_state=SUCCESS)

        return self.state

    def on_failure(self, exc, task_id, args, kwargs, einfo):

        msg = get_error(exc)
        self.set_progress(msg, task_state=FAILURE)


get_privilege_push_task = register_task(GetPrivilegePushTask())
