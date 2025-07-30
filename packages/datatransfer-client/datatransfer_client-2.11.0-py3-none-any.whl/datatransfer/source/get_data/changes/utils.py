# coding: utf-8

from __future__ import (
    absolute_import,
)

from collections import (
    namedtuple,
)
from datetime import (
    date,
)

from django.db.models import (
    ForeignKey,
)
from django.utils.encoding import (
    force_str,
)

from educommon.contingent.catalogs import (
    IdentityDocumentsTypes,
)
from m3_django_compat import (
    FieldDoesNotExist,
    ModelOptions,
    get_related,
)


# todo: Убрать try после окончания поддержки django < 1.8.
try:
    from django.contrib.postgres.fields import (
        ArrayField,
    )
except ImportError:
    ArrayField = None


# Строка отображаемого списка различий
DiffField = namedtuple('DiffField', ('id', 'name', 'old', 'new'))


def get_field_by_column_name(meta, column):
    """Возвращает объект поля модели по имени колонки БД.

    :param meta: Модель, которой принадлежит поле.
    :type meta: django.db.models.Model
    :param column: Имя колонки в таблице БД.
    :type column: str

    :return: Поле модели, соответствующее колонке или None.
    """
    fields_map = {field.column: field for field in meta.opts.fields}
    return fields_map.get(column)


def get_field_name_display(model, field_name):
    """Возвращает текстовое описание поля модели.

    :param model: Модель, которой принадлежит поле.
    :type model: django.db.models.Model
    :param field_name: Поле модели, которое надо отобразить.
    :type field_name: str

    :return: Имя поля, преобразованное в пригодный для отображения вид
             в соответствии с полем модели.
    :rtype: unicode
    """
    meta = ModelOptions(model)
    try:
        return meta.get_field(field_name).verbose_name
    except FieldDoesNotExist:
        field = get_field_by_column_name(meta, field_name)
        if field:
            return field.verbose_name
        return field_name


def get_value_display(model, field_name, value):
    """Возвращает значение поля в человекочитаемом виде.

    :param model: Модель, которой принадлежит поле.
    :type model: django.db.models.Model
    :param field_name: Поле модели, в котором хранится значение.
    :type field_name: str
    :param value: Значение, которое необходимо отобразить.

    :return: Значение, преобразованное в пригодный для отображения вид
             в соответствии с полем модели.
    :rtype: unicode
    """

    def resolve_value(field_for_value, x):
        """Преобразует идентификаторы в значения choices, если возможно."""
        return force_str(dict(field_for_value.flatchoices).get(x, x), strings_only=True)

    meta = ModelOptions(model)
    try:
        field = meta.get_field(field_name)
        # todo: Убрать проверку ArrayField по окончании поддержки django < 1.8.
        if ArrayField and isinstance(field, ArrayField):
            if value is not None:
                value = ',\n\t'.join(resolve_value(field.base_field, x) for x in value)
        else:
            value = resolve_value(field, value)
    except FieldDoesNotExist:
        field = get_field_by_column_name(meta, field_name)
        if field and isinstance(field, ForeignKey):
            model = get_related(field).parent_model
            try:
                return model.objects.get(id=value).display()
            except model.DoesNotExist:
                pass
    if value is None:
        value = ''
    elif isinstance(value, date):
        value = value.strftime('%d.%m.%Y')

    return value


def maybe_int(value):
    """Конвертирует строку в int, если она не пуста.

    :type value: basestring
    :rtype int or None
    """
    if value:
        return int(value)


def uftt_to_document_type(uftt_code):
    """Возвращает системный код типа, по коду УФТТ.

    :type uftt_code: int
    :rtype int
    """
    types = IdentityDocumentsTypes.values
    mapping = {uftt: system for system, (_, uftt) in six.iteritems(types) if uftt is not None}
    return mapping.get(uftt_code, uftt_code)
