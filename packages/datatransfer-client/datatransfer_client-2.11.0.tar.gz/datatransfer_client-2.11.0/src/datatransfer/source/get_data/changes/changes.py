# coding: utf-8

from __future__ import absolute_import

from abc import ABCMeta
from collections import Iterable
from functools import partial

from django.contrib.contenttypes.models import ContentType
from django.utils.functional import cached_property
from m3_django_compat import atomic
import six

from .utils import DiffField
from .utils import get_field_name_display
from .utils import get_value_display


class MappedChange(six.with_metaclass(ABCMeta, object)):

    u"""Базовый объект-изменение.

    Связывает объект модели данных из datatransfer и объект модели ЭДО
    с помощью маппинга полей.


    Объявление атрибута `mapping`:

    >>>  class Change(MappedChange):
    >>>      mapping = (
    >>>          ('datatransfer_field', 'extedu_field'),
    >>>          ('datatransfer_field', 'extedu_field', func),
    >>>          ...
    >>>      )

    где func - callable объект, преобразующий значение данного поля
    в значение для ЭДО.
    """

    mapping = None

    def __init__(self, source, target, apply_empty=True):
        u"""Инициализация экземпляра класса.

        :param source: экземпляр модели datatransfer.
        :type source: django.db.models.Model
        :param target: экземпляр соответствующей модели ЭДО.
        :type target: django.db.models.Model
        :param apply_empty: определяет применение пустых значений.
        :type apply_empty: boolean
        """
        assert isinstance(self.mapping, Iterable), (
            u'Необходимо определить атрибут mapping как итерируемую'
            u' последовательность кортежей.'
        )
        self._source = source
        self._target = target
        self._apply_empty = apply_empty

    @property
    def target(self):
        return self._target

    @property
    def source(self):
        return self._source

    @property
    def exclude_fields(self):
        u"""Поля модели РИС для исключения при сравнении.

        Используется для временной отмены сравнения определенных полей.
        При внесении стоит обратить внимание, что названия полей разных
        моделей могут совпадать.
        :return tuple: перечень полей
        """
        return 'difficult_situation', 'difficult_situations'

    @cached_property
    def _target_fields(self):
        # pylint: disable=not-an-iterable
        return tuple(
            row[1] for row in self.mapping
            if row[1] not in self.exclude_fields
        )

    @cached_property
    def _old_dict(self):
        u"""Словарь: идентификатор_поля => старое значение."""
        result = {
            field: getattr(self._target, field)
            for field in self._target_fields
        }
        return result

    @cached_property
    def _new_dict(self):
        u"""Словарь: идентификатор_поля => новое значение."""
        # pylint: disable=not-an-iterable
        result = {}
        for row in self.mapping:
            row_len = len(row)
            assert row_len in (2, 3), (
                u'Неверное количество параметров в маппинге {}: {}'.format(
                    self.__class__.__name__, row
                )
            )
            source_field, field, convert = (row + (None,))[:3]

            value = getattr(self._source, source_field)
            if convert:
                assert callable(convert)
                value = convert(value)
            result[field] = value
        return result

    @cached_property
    def _raw_diff(self):
        u"""Список кортежей с изменениями."""
        result = []
        for field in self._target_fields:
            new_value = self._new_dict[field]
            old_value = self._old_dict[field]
            if (old_value != new_value
                    and not self._both_empty(old_value, new_value)
                    and self._can_apply(new_value)):
                result.append((field, old_value, new_value))
        return result

    def _can_apply(self, value):
        u"""Проверяет может ли значение быть применено.

        :rtype: bool
        """
        return self._apply_empty or value not in (None, '')

    def _both_empty(self, old_value, new_value):
        u"""Проверяет, что оба значения пустые.

        :rtype: bool
        """
        return old_value in (None, '') and new_value in (None, '')

    @cached_property
    def diff(self):
        u"""Список именованных кортежей с изменениями для отображения.

        :rtype tuple
        """
        return tuple(
            DiffField(*self._get_diff_row(*data))
            for data in self._raw_diff
        )

    def _get_diff_row(self, field, old, new):
        u"""Преобразует строку списка различий в читаемый вид.

        :param basestring field: Идентификатор поля.
        :param basestring old: Старое значение.
        :param basestring new: Новое значение.

        :rtype: tuple
        """
        return (
            field,
            get_field_name_display(self._target, field),
            get_value_display(self._target, field, old),
            get_value_display(self._target, field, new)
        )

    @property
    def old_is_none_mask(self):
        u"""Булева маска заполненности полей "значения до".

        :return: Кортеж булевых значений, в котором False означает
        незаполненное поле, True - заполненное.
        :rtype: tuple
        """
        return tuple(old is None for _, old, _ in self._raw_diff)

    @atomic
    def apply(self, only_fields=None):
        u"""Копирует поля из source в target и сохраняет target.

        :param only_fields: Поля, к которым должны применятся изменения
                            если не указан, то изменяются все поля.
        :type only_fields: iterable or None
        :return: Информация об изменении для сериализации в json.
        :rtype: dict
        """
        diff = self._get_filtered_diff(only_fields)
        self._fill_fields(diff)
        self._save()
        if diff:
            return dict(
                id=self._target.id,
                model_id=ContentType.objects.get_for_model(self._target).id,
                diff=diff
            )

    def _get_filtered_diff(self, fields):
        u"""Возвращает изменения, отфильтрованные по указанным полям.

        Если поля не указаны, возвращает все изменения.
        """
        diff = self._raw_diff
        if fields is None:
            return diff
        return tuple(
            (field, old, new)
            for field, old, new in diff
            if field in fields
        )

    def _fill_fields(self, diff):
        u"""Заполняет атрибуты target."""
        for field, _, value in diff:
            setattr(self._target, field, value)

    def _save(self):
        u"""Сохраняет target в БД."""
        self._target.save()


class ComplexFieldChange(MappedChange):

    u"""Объект-изменение для группы полей.

    Отображает только одно поле, указанное в view_field, а применяет все,
    указанные в маппинге.

    Может использоваться для работы с адресами, хранящимися в виде guid'ов и
    строки полного адреса. Пользователь будет видеть только изменение строки
    адреса. Если он решит применить только адрес, то guid'ы применятся
    автоматически.
    """

    view_field = None

    @property
    def field_name(self):
        u"""Отображаемое пользователю название поля."""
        field = self._target.__class__._meta.get_field(self.view_field)
        return field.verbose_name

    @cached_property
    def diff(self):
        u"""Список изменений для отображения.

        Отображает только изменение для `view_field`.
        """
        if len(self._raw_diff) > 0:
            display = partial(get_value_display, self._target, self.view_field)

            return (
                DiffField(
                    self.view_field,
                    self.field_name,
                    display(self._old_dict[self.view_field]),
                    display(self._new_dict[self.view_field])
                ),
            )
        return tuple()

    def apply(self, only_fields=None):
        if only_fields is None or self.view_field in only_fields:
            result = super(ComplexFieldChange, self).apply()
            return result


class ChangesGroup(six.with_metaclass(ABCMeta, object)):

    _changes = None
    _source = None

    def __init__(self, *args, **kwargs):
        assert isinstance(self._changes, Iterable), type(self._changes)
        assert self._source is not None

    @property
    def source(self):
        return self._source

    @cached_property
    def diff(self):
        u"""Список различий всех объектов-изменений для отображения.

        :return Кортеж именованных кортежей DiffField.
        :rtype: tuple
        """
        return sum((change.diff for change in self._changes), ())

    @property
    def old_is_none_mask(self):
        u"""Булева маска заполненности полей "значения до".

        :return tuple: Кортеж булевых значений, в котором False означает
        незаполненное поле, True - заполненное.
        :rtype: tuple
        """
        return sum((change.old_is_none_mask for change in self._changes), ())

    @atomic
    def apply(self, only_fields=None):
        u"""Применяет изменения для связанных объектов в БД.

        :param iterable only_fields: список идентификаторов полей.

        :return: список данных об изменениях.
        :rtype: list
        """
        diffs = []
        for change in self._changes:
            diff = change.apply(only_fields)
            if diff:
                diffs.append(diff)
        return diffs
