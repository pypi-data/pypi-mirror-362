# coding: utf-8
from __future__ import absolute_import

from datatransfer.source.common import constants
from django.conf import settings
from educommon import ioc

from . import configs as dt_settings


def register_actions():
    if dt_settings.DESTINATION_SYSTEM_CODE == 'KTELABS_CONT':
        from .actions import ContingentKteLabsPack
        ioc.get("main_controller").packs.append(ContingentKteLabsPack())
