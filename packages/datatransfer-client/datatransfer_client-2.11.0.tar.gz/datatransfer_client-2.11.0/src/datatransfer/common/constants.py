# coding: utf-8

from __future__ import absolute_import

import os


DATATRANSFER_NAMESPACE = 'http://bars-open.ru/inf'

DATATRANSFER_SERVICE_MNEMONICS = 'CNTNG0000'
DATATRANSFER_SERVICE_VERSION = '0.01'

DATAPUSH_NAMESPACE = 'http://bars-open.ru/inf'

DATAPUSH_SERVICE_MNEMONICS = 'CNTNG0001'
DATAPUSH_SERVICE_VERSION = '0.01'

SMEV_TYPE_CODE = 'OTHR'
SMEV_STATUS = 'REQUEST'
SMEV_EXCHANGE_TYPE = '0'

CONFIGURATION_ARCHIVE_IN = (
    os.path.join('archive', 'in'))
CONFIGURATION_ARCHIVE_OUT = (
    os.path.join('archive', 'out'))

MODE_ALL = 'ALL'
MODE_UPDATED = 'UPDATED'
