# coding: utf-8

from __future__ import absolute_import

from time import sleep
import datetime
import os
import re

from celery.states import FAILURE
from celery.states import SUCCESS
from django.contrib.contenttypes.models import ContentType
from m3_django_compat import atomic
from petl.io.sources import ZipSource

from datatransfer.common import constants
from datatransfer.common.helpers import get_error
from datatransfer.common.helpers import get_packet
from datatransfer.common.utils import archive_xml
from datatransfer.common.utils import encode_archive
from datatransfer.common.utils import register_task
from datatransfer.common.xml.parser import XMLModelParser
from datatransfer.source import configs as dt_settings
from datatransfer.source.common.configuration import get_object
from datatransfer.source.get_data.etl.packet.extractor.common.mapping import \
    rules
from datatransfer.source.get_data.etl.packet.loader.mapping import \
    rules as get_data_push_rules
from datatransfer.source.get_data.models import GetDataPerson
from datatransfer.source.get_data.models import GetDataPersonDocument
from datatransfer.source.get_data.models import GetDataRecordStatus
from datatransfer.source.get_data.models import GetDataSession
from datatransfer.source.get_data.models import GetDataStatistic
from datatransfer.source.get_data.service.client import GetDataClient

from .utils import Loader
from .utils import clear_tables
from .utils import update_persons_ids


# Класс асинхронной задачи
AsyncTask = get_object("task_class")


class GetDataTask(AsyncTask):
    """Задача - формирующая xml"""

    description = u"Контингент. Запрос данных"
    stop_executing = False
    routing_key = dt_settings.CELERY_ROUTING_KEY

    LOG_TIME_FORMAT = "%d.%m.%Y %H:%M"

    def run(self, *args, **kwargs):
        super(GetDataTask, self).run(*args, **kwargs)

        packet_mapping = rules

        session_id = kwargs.get('session_id', None) or self.request.id

        today = datetime.date.today()
        now = datetime.datetime.now()

        session = GetDataSession()
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

            client = GetDataClient()

            client.GetData(session_id, encoded_file_name, filename)

            try:
                os.remove(encoded_file_name)
            except OSError as e:
                error = get_error(e)
                self.set_progress(
                    values={
                        u"Ошибка в процессе "
                        u"удаления временного файла {0}".format(
                            encoded_file_name): error
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
            session.message = get_error(e)
            session.save()
            raise
        return self.state


get_data_task = register_task(GetDataTask())


class GetDataPushTask(AsyncTask):
    u"""Парсинг и сохранение результатов запроса."""

    description = u"Загрузка данных"
    stop_executing = False
    routing_key = dt_settings.CELERY_ROUTING_KEY

    @atomic
    def run(self, xml_filename, archive_filename,
            session, encoding='utf-8', *args, **kwargs):
        super(GetDataPushTask, self).run(*args, **kwargs)

        session = GetDataSession.objects.get(session=session)

        index_pattern = re.compile(r'\[\d+\]')

        gender_mapping = {
            '1': 'Male',
            '2': 'Female'}

        citizenship_mapping = {
            '0': '1',
            '1': '3',
            '2': '4',
            '3': '0'}

        person_model = ContentType.objects.get_for_model(
            get_object("person_models")
        )
        document_model = ContentType.objects.get_for_model(
            get_object("document_models")
        )
        results = {
            'person_count': 0,
            'document_count': 0
        }

        person_fields = (
            'model_id',
            'session_id',
            'local_id',
            'regional_id',
            'federal_id',
            'source_id',
            'external_id',
            'first_name',
            'middle_name',
            'last_name',
            'gender',
            'birth_date',
            'birth_place',
            'snils',
            'health_group',
            'long_term_treatment',
            'disability_group',
            'disability_expiration_date',
            'disability_reason',
            'adaptation_program',
            'physical_culture_group',
            'difficult_situation',
            'document_registry_number',
            'document_registry_issuer',
            'document_registry_issue_date',
            'citizenship',
            'registration_address_place',
            'registration_address_street',
            'registration_address_house',
            'registration_address_flat',
            'registration_address',
            'residence_address_place',
            'residence_address_street',
            'residence_address_house',
            'residence_address_flat',
            'residence_address',
            'actual_address_place',
            'actual_address_street',
            'actual_address_house',
            'actual_address_flat',
            'actual_address',
            'created',
            'status'
        )

        document_fields = (
            'model_id',
            'session_id',
            'local_id',
            'regional_id',
            'person_id',
            'source_id',
            'external_id',
            'type',
            'series',
            'number',
            'issuer',
            'issue_date',
            'created',
            'status'
        )

        person_loader = Loader(
            GetDataPerson._meta.db_table,
            person_fields
        )
        document_loader = Loader(
            GetDataPersonDocument._meta.db_table,
            document_fields
        )

        def adaptation_program_fixup(value):
            if value in ('1', '2'):
                return None

            return value

        def person_handler(data):
            person_data = data['Person']
            results['person_count'] += 1
            values = (
                person_model.id,
                session.id,
                person_data['ID'],
                person_data['RegionalID'],
                person_data['FederalID'],
                person_data['SourceID'],
                person_data['ExternalID'],
                person_data['FirstName'],
                person_data['MiddleName'],
                person_data['LastName'],
                gender_mapping.get(person_data['Gender']),
                person_data['BirthDate'],
                person_data['BirthPlace'],
                person_data['SNILS'],
                person_data['HealthGroup'],
                person_data['LongTermTreatment'],
                person_data['DisabilityGroup'],
                person_data['DisabilityExpirationDate'],
                person_data['DisabilityReason'],
                adaptation_program_fixup(person_data['AdaptationProgram']),
                person_data['PhysicalCultureGroup'],
                person_data['DifficultSituation'],
                person_data['DocumentRegistryNumber'],
                person_data['DocumentRegistryIssuer'],
                person_data['DocumentRegistryIssueDate'],
                citizenship_mapping.get(person_data['Citizenship']),
                person_data['RegistrationAddressPlace'],
                person_data['RegistrationAddressStreet'],
                person_data['RegistrationAddressHouse'],
                person_data['RegistrationAddressFlat'],
                person_data['RegistrationAddress'],
                person_data['ResidenceAddressPlace'],
                person_data['ResidenceAddressStreet'],
                person_data['ResidenceAddressHouse'],
                person_data['ResidenceAddressFlat'],
                person_data['ResidenceAddress'],
                person_data['ActualAddressPlace'],
                person_data['ActualAddressStreet'],
                person_data['ActualAddressHouse'],
                person_data['ActualAddressFlat'],
                person_data['ActualAddress'],
                datetime.datetime.now(),
                GetDataRecordStatus.WAIT
            )
            person_loader.insert(values)

        def document_handler(data):
            document_data = data['Document']
            results['document_count'] += 1
            values = (
                document_model.id,
                session.id,
                document_data['ID'],
                document_data['PersonRegionalID'],
                document_data['Person'],
                document_data['SourceID'],
                document_data['ExternalID'],
                document_data['Type'],
                document_data['Series'],
                document_data['Number'],
                document_data['Issuer'],
                document_data['IssueDate'],
                datetime.datetime.now(),
                GetDataRecordStatus.WAIT
            )
            document_loader.insert(values)

        handlers = {
            '/Packet/Data/Persons/Person': person_handler,
            '/Packet/Data/PersonDocuments/Document': document_handler
        }

        with ZipSource(archive_filename, xml_filename).open('r') as xmlio:
            for (path, data) in XMLModelParser(get_data_push_rules).parse(xmlio):
                path = re.sub(index_pattern, '', path)

                handler = handlers.get(path)

                handler and handler(data)

        clear_tables(GetDataPersonDocument._meta.db_table,
                     GetDataPerson._meta.db_table)
        person_loader.close()
        update_persons_ids(document_loader.temp_table)
        document_loader.close()

        statistic = GetDataStatistic()
        statistic.session = session
        statistic.model = ContentType.objects.get_for_model(GetDataPerson)
        statistic.count = results['person_count']
        statistic.save()

        statistic = GetDataStatistic()
        statistic.session = session
        statistic.model = ContentType.objects.get_for_model(
            GetDataPersonDocument
        )
        statistic.count = results['document_count']
        statistic.save()

        session.processed = True
        session.save()

        self.set_progress(
            progress=u"Загрузка прошла успешно",
            task_state=SUCCESS)

        return self.state

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        msg = get_error(exc)
        self.set_progress(msg, task_state=FAILURE)


get_data_push_task = register_task(GetDataPushTask())


class GetDataAutorunTask(GetDataTask):

    u"""Задача автоматического запуска запроса данных."""

    PERIOD_RULES = {
        'DAY': lambda: True,
        'WEEK': lambda: datetime.date.today().weekday() == 0,
        'MONTH': lambda: datetime.date.today().day == 1,
        'NEVER': lambda: False
    }

    def run(self, *args, **kwargs):
        config = get_object("get_data_config")()
        period = config.autorun_period

        if self.PERIOD_RULES[period]():
            return super(GetDataAutorunTask, self).run(*args, **kwargs)
        else:
            # Не вызываем run родителя
            super(GetDataTask, self).run(*args, **kwargs)
            sleep(1)
            try:
                from celery.exceptions import Reject
                raise Reject()
            except ImportError:
                self.set_progress(progress=u'Задача отменена.')
                return self.state


get_data_autorun_task = register_task(GetDataAutorunTask())
