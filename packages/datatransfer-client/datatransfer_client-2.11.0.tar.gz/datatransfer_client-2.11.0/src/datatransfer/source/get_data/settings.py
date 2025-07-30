# coding:utf-8
from __future__ import absolute_import

from abc import ABCMeta
from abc import abstractproperty

import six


class BaseSettingsConfig(six.with_metaclass(ABCMeta, object)):

    u"""Базовый класс для настроек взаимодействия с Контингентом.

    Определяет интерфейс взаимодействия с конфигурацией РИС.
    """

    @abstractproperty
    def replace_empty(self):
        pass

    @abstractproperty
    def autorun_period(self):
        pass
