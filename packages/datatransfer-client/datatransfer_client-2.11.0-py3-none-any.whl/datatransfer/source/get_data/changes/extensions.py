# coding: utf-8

from __future__ import absolute_import

from abc import ABCMeta
from abc import abstractmethod

from django.utils.functional import cached_property
from educommon import ioc
import six


class BaseExtensions(six.with_metaclass(ABCMeta, object)):

    @abstractmethod
    def get_change(self, data, replace):
        u"""Возвращает объект-изменение."""
        pass

    def get_current_user(self, request):
        u"""Возвращает текущего пользователя."""
        return ioc.get_current_user(request)

    @cached_property
    def change_viewer_class(self):
        u"""Класс для отображения принятых изменений."""
        from .wrappers import AppliedChangeViewer
        return AppliedChangeViewer

    @cached_property
    def person_model_class(self):
        u"""Класс физ. лица."""
        from datatransfer.source.common.configuration import get_object
        return get_object('person_models')

    @abstractmethod
    def apply_changes(self, person_data_ids, request, replace):
        u"""Принимает все изменения для заданных id."""
        pass
