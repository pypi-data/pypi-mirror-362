# coding: utf-8

from __future__ import (
    absolute_import,
)

import os

from django.conf import (
    settings as dj_settings,
)
from django.utils.encoding import (
    smart_str,
)

from datatransfer.common.configuration import (
    ExtendedConfigParser,
)
from datatransfer.source.common.configuration import (
    get_object,
)


# Общие настройки
DATATRANSFER_CONFIG_FILE_NAME = 'datatransfer.config'

# переменная пути к конфигам может быть разной в разных проектах
if hasattr(dj_settings, '_CONFIG_PATH'):
    config_path = dj_settings._CONFIG_PATH
elif hasattr(dj_settings, 'CONFIG_PATH'):
    config_path = dj_settings.CONFIG_PATH
else:
    raise ValueError('Variable CONFIG_PATH is not found')


DATATRANSFER_CONFIG = os.path.join(config_path, DATATRANSFER_CONFIG_FILE_NAME)

# Значение параметров по умолчанию
DEFAULT_CONFIG = {
    ('DATATRANSFER', 'WSDL'): '',
    ('DATATRANSFER', 'MNEMONICS'): 'CTNG00000',
    ('DATATRANSFER', 'NAME'): 'EDUCTNG',
    ('DATATRANSFER', 'AUTHORIZATION_KEY'): '',
    ('DATATRANSFER', 'DESTINATION_SYSTEM_CODE'): 'BARS_CONT',
    ('DATAPUSH', 'AUTHORIZATION_KEY'): '',
    ('WEBSERVICE', 'TIMEOUT'): '120',
    ('CELERY', 'QUEUE'): '',
    ('CELERY', 'ROUTING_KEY'): '',
    ('STORAGE', 'MAILBOX_PATH'): '',
    ('SMEV', 'MNEMONICS'): '',
    ('SMEV', 'NAME'): '',
    ('SMEV', 'CERTIFICATE_FILE'): '',
    ('SMEV', 'PRIVATE_KEY_FILE'): '',
    ('SMEV', 'PRIVATE_KEY_PASSWORD'): '',
    ('SMEV', 'DIGEST_METHOD'): 'md_gost94',
    ('KTE', 'AIS_GUID'): '',
    ('KTE', 'KTE_SEND_DATA_TIME_HOUR'): '2',
    ('KTE', 'KTE_SEND_DATA_TIME_MINUTE'): '30',
    ('KTE', 'KTE_PERIODIC_TASK_ENABLED'): 'False',
    ('GET_PRIVILEGE', 'RUN_PRIVILEGE_TASK_AT'): '00:00',
    ('GET_DATA', 'AUTORUN_HOUR'): '2',
    ('GET_DATA', 'AUTORUN_MINUTE'): '30',
    ('FEEDBACK', 'CLEAR_FEEDBACK_DETAILS_DAYS'): '10',
    ('VALIDATE', 'XSD_FILE_PATH'): '',
}

config_parser = ExtendedConfigParser(DEFAULT_CONFIG)

config_parser.read(DATATRANSFER_CONFIG)

# Настройки, специфичные для проекта
WEBSERVICE_TIMEOUT = config_parser.getint('WEBSERVICE', 'TIMEOUT')
DATATRANSFER_WSDL = config_parser.get('DATATRANSFER', 'WSDL')
DATATRANSFER_MNEMONICS = config_parser.get('DATATRANSFER', 'MNEMONICS')
DATATRANSFER_NAME = config_parser.get('DATATRANSFER', 'NAME')
DATATRANSFER_AUTHORIZATION_KEY = config_parser.get('DATATRANSFER', 'AUTHORIZATION_KEY')
DESTINATION_SYSTEM_CODE = config_parser.get('DATATRANSFER', 'DESTINATION_SYSTEM_CODE')
DATAPUSH_AUTHORIZATION_KEY = config_parser.get('DATAPUSH', 'AUTHORIZATION_KEY')

CELERY_QUEUE = config_parser.get('CELERY', 'QUEUE')
CELERY_ROUTING_KEY = config_parser.get('CELERY', 'ROUTING_KEY')
STORAGE_MAILBOX_PATH = config_parser.get('STORAGE', 'MAILBOX_PATH')

SMEV_MNEMONICS = config_parser.get('SMEV', 'MNEMONICS') or smart_str(get_object('smev_mnemonics'))
SMEV_NAME = config_parser.get('SMEV', 'NAME') or smart_str(get_object('smev_name'))
SMEV_CERTIFICATE_FILE = config_parser.get('SMEV', 'CERTIFICATE_FILE') or smart_str(get_object('smev_pem'))
SMEV_PRIVATE_KEY_FILE = config_parser.get('SMEV', 'PRIVATE_KEY_FILE') or smart_str(get_object('smev_pem'))
SMEV_PRIVATE_KEY_PASSWORD = config_parser.get('SMEV', 'PRIVATE_KEY_PASSWORD') or smart_str(
    get_object('smev_private_key_password')
)
SMEV_DIGEST_METHOD = config_parser.get('SMEV', 'DIGEST_METHOD')

KTE_AIS_GUID = config_parser.get('KTE', 'AIS_GUID')
KTE_SEND_DATA_TIME_HOUR = config_parser.getint('KTE', 'KTE_SEND_DATA_TIME_HOUR')
KTE_SEND_DATA_TIME_MINUTE = config_parser.getint('KTE', 'KTE_SEND_DATA_TIME_MINUTE')
# Автоматическая выгрузка вкл/выкл
KTE_PERIODIC_TASK_ENABLED = config_parser.getboolean('KTE', 'KTE_PERIODIC_TASK_ENABLED')

# Время запуска переодической задачи получения льгот
RUN_PRIVILEGE_TASK_AT = config_parser.get('GET_PRIVILEGE', 'RUN_PRIVILEGE_TASK_AT')

GET_DATA_AUTORUN_HOUR = config_parser.getint('GET_DATA', 'AUTORUN_HOUR')
GET_DATA_AUTORUN_MINUTE = config_parser.getint('GET_DATA', 'AUTORUN_MINUTE')

# Насколько старые данные мы должны удалять из деталей.
CLEAR_FEEDBACK_DETAILS_DAYS = config_parser.getint('FEEDBACK', 'CLEAR_FEEDBACK_DETAILS_DAYS')

# валидация выгружаемого xml файла с данными для КО
# необходимо прописать путь до главного файла XSD и его зависимостей
XSD_FILE_PATH = config_parser.get('VALIDATE', 'XSD_FILE_PATH')
