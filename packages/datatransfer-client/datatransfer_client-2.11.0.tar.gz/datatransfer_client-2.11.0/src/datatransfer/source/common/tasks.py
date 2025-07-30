# coding: utf-8

from __future__ import absolute_import

import datetime
import os

from celery.states import SUCCESS

from datatransfer.common import constants
from datatransfer.common.constants import MODE_ALL
from datatransfer.common.helpers import get_error
from datatransfer.common.utils import archive_xml
from datatransfer.common.utils import encode_archive
from datatransfer.common.utils import register_task
from datatransfer.source import configs as dt_settings
from datatransfer.source.common.configuration import get_object
from datatransfer.source.etl.packet.extractor.common.mapping import rules
from datatransfer.source.transport.smev.datatransfer.client import (
    DataTransferClient
)
from datatransfer.source.utils import create_export_packet


# Класс асинхронной задачи
AsyncTask = get_object("task_class")


class DataTransferTask(AsyncTask):
    """Задача - формирующая xml"""

    description = u"Контингент. Выгрузка данных"
    stop_executing = False
    routing_key = dt_settings.CELERY_ROUTING_KEY

    LOG_TIME_FORMAT = "%d.%m.%Y %H:%M"

    def run(self, *args, **kwargs):
        super(DataTransferTask, self).run(*args, **kwargs)

        packet_mapping = rules

        session_id = kwargs.get('session_id', None) or self.request.id
        mode = kwargs.get('mode', MODE_ALL)

        today = datetime.date.today()
        now = datetime.datetime.now()

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

        filename = create_export_packet(archive_path, session_id, mode)

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

        client = DataTransferClient()
        client.DataTransfer(session_id, encoded_file_name, filename)

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
        return self.state


data_transfer_task = register_task(DataTransferTask())
