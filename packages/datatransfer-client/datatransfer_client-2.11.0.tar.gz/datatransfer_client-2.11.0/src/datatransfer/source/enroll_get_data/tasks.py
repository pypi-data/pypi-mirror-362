# coding: utf-8
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
from datatransfer.common.helpers import get_packet
from datatransfer.common.utils import archive_xml
from datatransfer.common.utils import encode_archive
from datatransfer.common.utils import register_task
from datatransfer.common.xml.parser import XMLModelParser
from datatransfer.source import configs as dt_settings
from datatransfer.source.enroll_get_data.etl.packet.extractor.common.mapping import (
    rules
)
from datatransfer.source.enroll_get_data.etl.packet.loader.mapping import (
    rules as enroll_get_data_push_rules
)
from datatransfer.source.get_data.models import GetDataRecordStatus
from datatransfer.source.get_data.models import GetDataSession
from datatransfer.source.get_data.models import GetDataStatistic
from datatransfer.source.get_data.utils import Loader
from datatransfer.source.get_data.utils import clear_tables

from .client import EnrollGetDataClient
from .models import EnrollGetDataDeclaration
from .models import EnrollGetDataDeclarationDocument
from .models import EnrollGetDataMainEducation
from .models import EnrollGetDataMiddleEducation
from .models import EnrollGetDataPreschoolEducation
from ..common.configuration import get_object

AsyncTask = get_object("task_class")


class EnrollGetDataTask(AsyncTask):
    """Задача - формирующая xml"""

    description = "Контингент. Запрос данных для заявлений на зачисление."
    stop_executing = False
    routing_key = dt_settings.CELERY_ROUTING_KEY

    LOG_TIME_FORMAT = "%d.%m.%Y %H:%M"

    def run(self, *args, **kwargs):
        super().run(*args, **kwargs)
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
                progress="Процесс формирования XML с данными ...",
                values={
                    "Время начала формирования XML c данными": (
                        datetime.datetime.now().strftime(self.LOG_TIME_FORMAT)
                    )
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
                timestamp=now,
                declaration_ids=kwargs.get('declaration_ids', [])
            )

            self.set_progress(
                progress="Процесс формирования XML c данными окончен",
                values={
                    "Время окончания процесса формирования XML c данными": (
                        datetime.datetime.now().strftime(self.LOG_TIME_FORMAT)
                    )
                }
            )

            self.set_progress(
                progress="Процесса архивирования XML ...",
                values={
                    "Время начала процесса архивирования XML": (
                        datetime.datetime.now().strftime(self.LOG_TIME_FORMAT)
                    )
                }
            )
            archive_filename = archive_xml(filename)
            self.set_progress(
                progress="Процесс архивирования XML завершен",
                values={
                    "Время окончания процесса архивирования XML": (
                        datetime.datetime.now().strftime(self.LOG_TIME_FORMAT)
                    )
                }
            )

            try:
                os.remove(filename)
            except OSError as e:
                error_desc = "Ошибка в процессе удаления файла {0}".format(
                    filename
                )
                self.set_progress(values={error_desc: e.message})
            else:
                self.set_progress(
                    values={
                        "Выполнено удаление XML": ""
                    }
                )

            self.set_progress(
                progress="Начало процесса кодирования архива",
                values={
                    "Время начала процесса "
                    "кодирования архива": datetime.datetime.now(
                    ).strftime(self.LOG_TIME_FORMAT)
                }
            )
            encoded_file_name = encode_archive(archive_filename)
            self.set_progress(
                progress="Конец процесса кодирования архива",
                values={
                    "Время окончания процесса "
                    "кодирования архива": datetime.datetime.now(
                    ).strftime(self.LOG_TIME_FORMAT)
                }
            )

            client = EnrollGetDataClient()

            client.EnrollGetData(session_id, encoded_file_name, filename)

            try:
                os.remove(encoded_file_name)
            except OSError as e:
                self.set_progress(
                    values={
                        "Ошибка в процессе "
                        "удаления временного файла {0}".format(
                            encoded_file_name): e.message
                    }
                )
            else:
                self.set_progress(
                    values={
                        "Выполнено удаление XML": ""
                    }
                )

            self.set_progress(
                progress="Формирование прошло успешно",
                task_state=SUCCESS)
        except Exception as e:
            session.message = e.message
            session.save()
            raise
        return self.state


enroll_get_data_task = register_task(EnrollGetDataTask())


class EnrollGetDataAutorunTask(EnrollGetDataTask):

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
            return super(EnrollGetDataAutorunTask, self).run(*args, **kwargs)
        else:
            # Не вызываем run родителя
            super(EnrollGetDataAutorunTask, self).run(*args, **kwargs)
            sleep(1)
            try:
                from celery.exceptions import Reject
                raise Reject()
            except ImportError:
                self.set_progress(progress=u'Задача отменена.')
                return self.state


enroll_get_data_autorun_task = register_task(EnrollGetDataAutorunTask())


class EducationLoader(Loader):
    """Загрузчик данных образовательных организациций."""

    def _copy(self):
        """Выполняет копирование из временной базы в целевую."""
        sql = (
            'INSERT INTO {target} ({columns}) '
            'SELECT DISTINCT ON (get_data_external_id) {columns} '
            'FROM {source} ORDER BY get_data_external_id, id DESC;'
        ).format(
            target=self._target_table,
            source=self.temp_table,
            columns=', '.join(self._fields)
        )
        self._cursor.execute(sql)


class EnrollGetDataPushTask(AsyncTask):
    """Парсинг и сохранение результатов запроса."""

    description = "Загрузка данных"
    stop_executing = False
    routing_key = dt_settings.CELERY_ROUTING_KEY

    @atomic
    def run(self, xml_filename, archive_filename,
            session, encoding='utf-8', *args, **kwargs):
        super().run(*args, **kwargs)
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

        results = {
            'person_count': 0,
            'document_count': 0,
            'preschool_edu_count': 0,
            'main_edu_count': 0,
            'middle_edu_count': 0,
        }

        person_fields = (
            'session_id',
            'regional_id',
            'federal_id',
            'source_id',
            'external_id',
            'first_name',
            'middle_name',
            'last_name',
            'gender',
            'birth_date',
            'snils',
            'health_group',
            'disability_group',
            'disability_expiration_date',
            'disability_reason',
            'adaptation_program',
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
            'session_id',
            'regional_id',
            'get_data_external_id',
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

        education_fields = (
            'session_id',
            'regional_id',
            'person_contingent_id',
            'get_data_external_id',
            'name',
            'enroll_date',
            'created',
            'status',
        )

        person_loader = Loader(
            EnrollGetDataDeclaration._meta.db_table,
            person_fields
        )
        document_loader = Loader(
            EnrollGetDataDeclarationDocument._meta.db_table,
            document_fields
        )
        preschool_loader = EducationLoader(
            EnrollGetDataPreschoolEducation._meta.db_table,
            education_fields
        )
        main_loader = EducationLoader(
            EnrollGetDataMainEducation._meta.db_table,
            education_fields
        )
        middle_loader = EducationLoader(
            EnrollGetDataMiddleEducation._meta.db_table,
            education_fields
        )

        def adaptation_program_fixup(value):
            if value in ('1', '2'):
                return None

            return value

        def person_handler(data):
            person_data = data['Person']
            results['person_count'] += 1
            values = (
                session.id,
                person_data['RegionalID'],
                person_data['FederalID'],
                person_data['SourceID'],
                person_data['ExternalID'],
                person_data['FirstName'],
                person_data['MiddleName'],
                person_data['LastName'],
                gender_mapping.get(person_data['Gender']),
                person_data['BirthDate'],
                person_data['SNILS'],
                person_data['HealthGroup'],
                person_data['DisabilityGroup'],
                person_data['DisabilityExpirationDate'],
                person_data['DisabilityReason'],
                adaptation_program_fixup(person_data['AdaptationProgram']),
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
                session.id,
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

        def _edu_values(edu_data):
            return (
                session.id,
                edu_data['PersonRegionalID'],
                edu_data['PersonLocalID'],
                edu_data['Person'],
                edu_data['Name'],
                edu_data['Date'],
                datetime.datetime.now(),
                GetDataRecordStatus.WAIT
            )

        def preschool_edu_handler(data):
            preschool_data = data['PreschoolEducation']
            results['preschool_edu_count'] += 1
            values = _edu_values(preschool_data)
            preschool_loader.insert(values)

        def main_edu_handler(data):
            main_data = data['MainEducation']
            results['main_edu_count'] += 1
            values = _edu_values(main_data)
            main_loader.insert(values)

        def middle_edu_handler(data):
            middle_data = data['MiddleEducation']
            results['middle_edu_count'] += 1
            values = _edu_values(middle_data)
            middle_loader.insert(values)
        handlers = {
            '/Packet/Data/Persons/Person': person_handler,
            '/Packet/Data/PersonDocuments/Document': document_handler,
            '/Packet/Data/PreschoolEducations/PreschoolEducation': (
                preschool_edu_handler
            ),
            '/Packet/Data/MainEducations/MainEducation': main_edu_handler,
            '/Packet/Data/MiddleEducations/MiddleEducation': (
                middle_edu_handler
            ),
        }

        with ZipSource(archive_filename, xml_filename).open('r') as xmlio:
            for (path, data) in XMLModelParser(
                    enroll_get_data_push_rules
            ).parse(xmlio):
                path = re.sub(index_pattern, '', path)
                handler = handlers.get(path)
                # pylint:disable=expression-not-assigned
                handler and handler(data)

        clear_tables(
            EnrollGetDataDeclarationDocument._meta.db_table,
            EnrollGetDataDeclaration._meta.db_table
        )
        # Копируем и завершаем загрузку данных:
        # 1. О персоне
        person_loader.close()
        # 2. О ДУЛ
        document_loader.close()
        # 3. О дошкольном образовании
        preschool_loader.close()
        # 4. О среднем образовании
        main_loader.close()
        # 5. О среднеспециальном образовании
        middle_loader.close()

        statistic = GetDataStatistic()
        statistic.session = session
        statistic.model = ContentType.objects.get_for_model(
            EnrollGetDataDeclaration
        )
        statistic.count = results['person_count']
        statistic.save()

        statistic = GetDataStatistic()
        statistic.session = session
        statistic.model = ContentType.objects.get_for_model(
            EnrollGetDataDeclarationDocument
        )
        statistic.count = results['document_count']
        statistic.save()

        session.processed = True
        session.save()

        self.set_progress(
            progress="Загрузка прошла успешно",
            task_state=SUCCESS)

        return self.state

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        msg = str(exc.message)
        self.set_progress(msg, task_state=FAILURE)


enroll_get_data_push_task = register_task(EnrollGetDataPushTask())
