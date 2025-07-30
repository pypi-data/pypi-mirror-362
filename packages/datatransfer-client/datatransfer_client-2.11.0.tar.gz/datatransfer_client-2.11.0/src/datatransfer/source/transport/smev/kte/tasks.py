# coding: utf-8
from __future__ import absolute_import

import datetime
import json
import os
import uuid
import zipfile

from datatransfer.common import constants
from datatransfer.common.helpers import get_error
from datatransfer.common.constants import MODE_UPDATED
from datatransfer.common.helpers import process_mapping
from datatransfer.common.helpers import toxml
from datatransfer.common.utils import encode_archive
from datatransfer.common.utils import register_task
from datatransfer.source import configs as dt_settings
from datatransfer.source.common.configuration import get_object
from datatransfer.source.common.helpers import set_isolation_level
from datatransfer.source.etl.packet.extractor.common.mapping import \
    rules as kte_rules

from celery.states import FAILURE
from celery.states import SUCCESS
from django.core.exceptions import ValidationError
from django.db import connection
from django.db.models import QuerySet
from django.template import Context
from django.template import Template
from educommon.contingent.contingent_plugin.models import \
    ContingentModelChanged
from educommon.utils.system import is_in_migration_command
from m3_django_compat import atomic
from six import PY2

from .client import KteLabsClient


# Класс асинхронной задачи
AsyncTask = get_object("task_class")


APPLIED_DOCUMENTS_TEMPLATE = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<ns1:AppliedDocuments xmlns:ns1="http://smev.gosuslugi.ru/request/rev111111">
    {% for name in names %}
    <ns1:AppliedDocument>
        <ns1:Name>{{ name }}</ns1:Name>
        <ns1:Number>0</ns1:Number>
        <ns1:URL>{{ name }}</ns1:URL>
    </ns1:AppliedDocument>
    {% endfor %}
</ns1:AppliedDocuments>
"""


class KteLabsSendDataTask(AsyncTask):
    """Задача формирующая xml"""

    description = u"Контингент КТЕ Лабс. Выгрузка данных"
    stop_executing = False
    routing_key = dt_settings.CELERY_ROUTING_KEY
    queue = dt_settings.CELERY_QUEUE

    LOG_TIME_FORMAT = "%d.%m.%Y %H:%M"

    def run(self, mode=MODE_UPDATED, *args, **kwargs):
        super(KteLabsSendDataTask, self).run(*args, **kwargs)

        def remove_file(fn):
            try:
                os.remove(fn)
            except OSError as e:
                msg = get_error(e)
                self.set_progress(
                    values={
                        u"Ошибка в процессе "
                        u"удаления файла {0}".format(fn): msg
                    }
                )
            else:
                self.set_progress(
                    values={
                        u"Выполнено удаление файла": fn
                    }
                )

        today = datetime.date.today()

        archive_path = os.path.join(
            dt_settings.STORAGE_MAILBOX_PATH,
            constants.CONFIGURATION_ARCHIVE_OUT,
            str(today.year), str(today.month), str(today.day))

        if not os.path.exists(archive_path):
            os.makedirs(archive_path)

        self.set_progress(
            progress=u"Процесс формирования пакета данных ...",
            values={
                u"Время начала формирования "
                u"XML c данными": datetime.datetime.now(
                ).strftime(self.LOG_TIME_FORMAT)
            }
        )

        package_name = os.path.join(
            archive_path,
            'package_{0}_{1}.zip'.format(
                dt_settings.SMEV_MNEMONICS,
                datetime.datetime.now().strftime('%s')
            ))

        zf = zipfile.ZipFile(
            package_name,
            mode="w",
            compression=zipfile.ZIP_DEFLATED,
            allowZip64=True)

        rules = kte_rules()
        blocks = list(rules['packet_mapping'].__self__._mapping.keys())

        if mode == MODE_UPDATED:
            connection.close()
            if hasattr(connection, 'connect'):
                connection.connect()

        with atomic(savepoint=False):
            if mode == MODE_UPDATED:
                set_isolation_level('repeatable read')

            for block in blocks:
                conf = {
                    'partition': False,
                    'block': block,
                    'mode': mode,
                    'organization_id': kwargs.get('organization_id')
                }

                xml_name = '{0}_{1}_{2}.xml'.format(
                    dt_settings.SMEV_MNEMONICS,
                    datetime.datetime.now().strftime('%s'),
                    block)

                filename = os.path.join(
                    archive_path, xml_name)

                pm = process_mapping(rules['packet_mapping'], **conf)
                toxml(pm, filename, serializer=rules['serializer'], **conf)

                zf.write(filename, filename.split('_')[-1])
                remove_file(filename)

            self.set_progress(
                progress=u"Процесс формирования пакета завершен",
                values={
                    u"Время окончания процесса "
                    u"архивирования XML": datetime.datetime.now(
                    ).strftime(self.LOG_TIME_FORMAT)
                }
            )

            request_code = uuid.uuid4()
            app_docs_name = "req_%s.xml" % request_code
            applied_documents = os.path.join(archive_path, app_docs_name)

            app_docs = Template(APPLIED_DOCUMENTS_TEMPLATE).render(
                Context({'names': [b + '.zip' for b in blocks]})
            )
            with open(applied_documents, 'w+') as f:
                f.write(app_docs)

            zf.write(applied_documents, app_docs_name)
            remove_file(applied_documents)

            # Удаляем данные об измененных моделях
            if kwargs.get('organization_id') is None:
                ContingentModelChanged.objects.all().delete()

        self.set_progress(
            progress=u"Начало процесса кодирования архива",
            values={
                u"Время начала процесса "
                u"кодирования архива": datetime.datetime.now(
                ).strftime(self.LOG_TIME_FORMAT)
            }
        )

        encoded_file_name = encode_archive(package_name)

        self.set_progress(
            progress=u"Конец процесса кодирования архива",
            values={
                u"Время окончания процесса "
                u"кодирования архива": datetime.datetime.now(
                ).strftime(self.LOG_TIME_FORMAT)
            }
        )

        client = KteLabsClient()
        ticket_guid = client.SendPacket(encoded_file_name, request_code)

        remove_file(encoded_file_name)

        if ticket_guid:
            kte_labs_get_result_task.apply_async(
                kwargs={
                    'ticket_guid': ticket_guid,
                }
            )

        self.set_progress(
            progress=u"Формирование прошло успешно",
            task_state=SUCCESS)
        return self.state


kte_labs_send_data_task = register_task(KteLabsSendDataTask())


class KteLabsGetResultTask(AsyncTask):
    """Задача проверяющая ответ Контингента КТЕ Лабс"""

    description = u"Контингент КТЕ Лабс. Получение результата"
    stop_executing = False
    routing_key = dt_settings.CELERY_ROUTING_KEY
    queue = dt_settings.CELERY_QUEUE

    LOG_TIME_FORMAT = "%d.%m.%Y %H:%M"

    def run(self, *args, **kwargs):
        super(KteLabsGetResultTask, self).run(*args, **kwargs)

        ticket_guid = kwargs.get('ticket_guid', None)
        if ticket_guid is None:
            return

        client = KteLabsClient()
        (message_text, errors, retry_after, status) = client.GetResult(ticket_guid)
        retry_after = retry_after or 0

        if status == 'FAIL':
            self.set_progress(
                progress=u"Ошибка обработки запроса с тикетом %s."
                         u"%s" % (ticket_guid, message_text),
                task_state=FAILURE)
        elif status == 'NOTFOUND':
            self.set_progress(
                progress=u"Запроса с тикетом %s нет в системе" % ticket_guid,
                task_state=FAILURE)
        elif status == 'INQUEUE':
            self.set_progress(
                progress=u"Запрос с тикетом %s находится в очереди" % ticket_guid,
                task_state=FAILURE)
            kte_labs_get_result_task.apply_async(
                countdown=retry_after,
                kwargs={
                    'ticket_guid': ticket_guid
                }
            )
        else:
            self.set_progress(
                progress=u"Запрос с тикетом %s успешно обработан" % ticket_guid,
                task_state=SUCCESS)

        return self.state


kte_labs_get_result_task = register_task(KteLabsGetResultTask())


# TODO вынести это из файла tasks.py
def change_schedule():
    if is_in_migration_command():
        return

    try:
        from django_celery_beat.models import CrontabSchedule
        from django_celery_beat.models import PeriodicTask
    except ImportError:
        try:
            from djcelery.models import CrontabSchedule
            from djcelery.models import PeriodicTask
        except ImportError:
            return

    # В зависимости от настроек, подключаем или удаляем расписание
    # запуска задачи
    KTE_PERIODIC_TASK_NAME = 'KTE_PERIODIC_TASK'

    if dt_settings.KTE_AIS_GUID and dt_settings.KTE_PERIODIC_TASK_ENABLED:
        crontab_params = dict(
            day_of_week='*',
            day_of_month='*',
            month_of_year='*',
            hour=dt_settings.KTE_SEND_DATA_TIME_HOUR,
            minute=dt_settings.KTE_SEND_DATA_TIME_MINUTE,
        )
        schedule_crontab = CrontabSchedule.objects.filter(
            **crontab_params).first()
        if not schedule_crontab:
            schedule_crontab = CrontabSchedule.objects.create(**crontab_params)

        update_or_create_params = dict(
            name=KTE_PERIODIC_TASK_NAME,
            defaults=dict(
                queue=dt_settings.CELERY_QUEUE,
                crontab=schedule_crontab,
                task=KteLabsSendDataTask.name,
                args=[],
                kwargs=json.dumps({'mode': MODE_UPDATED}),
                enabled=True
            ),
        )

        # Используется вызов функции update_or_create у оригинального QuerySet,
        # поскольку он выполняет select_for_update, а переопределённый - нет
        try:
            QuerySet(PeriodicTask).update_or_create(**update_or_create_params)
        except ValidationError as e:
            if 'name' in e.message_dict:
                # Скорее всего в другом процессе почти синхронно создали
                # объект (очень редкая ситуация), запись уже есть
                QuerySet(PeriodicTask).update_or_create(
                    **update_or_create_params)
            else:
                raise e
    else:
        PeriodicTask.objects.filter(name=KTE_PERIODIC_TASK_NAME).delete()


change_schedule()
