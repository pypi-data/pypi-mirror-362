# coding: utf-8

from __future__ import absolute_import

import json

from django.contrib.contenttypes.models import ContentType
from django.utils.functional import cached_property
from m3 import M3JSONEncoder
from m3_django_compat import atomic

from ..models import GetDataChanges
from ..models import GetDataPerson
from ..models import GetDataPersonDocument
from ..models import GetDataRecordStatus
from .constants import CHANGE_DIFF
from .constants import CHANGE_MIXED
from .constants import CHANGE_NEW
from .utils import DiffField
from .utils import get_field_name_display
from .utils import get_value_display


class ChangeWrapper(object):

    u"""Класс, предоставляющий интерфейс для работы с изменениями.

    На уровне этого класса производится сохранение примененного изменения
    и обновление статусов объекта контингента.
    """

    def __init__(self, change):
        self._change = change

    @property
    def old(self):
        u"""Старые значения полей.

        :return tuple: ((имя_поля, значение))
        """
        return tuple((row.name, row.old) for row in self.diff)

    @property
    def new(self):
        u"""Новые значения полей.

        :return tuple: ((имя_поля, значение), ...)
        """
        return tuple((row.name, row.new) for row in self.diff)

    @cached_property
    def diff(self):
        u"""Список изменений для отображения.

        :return tuple: ((идентификатор_поля, имя_поля,
                         старое_значение, новое_начение),)
        """
        return self._change.diff

    @property
    def change_type(self):
        u"""Тип изменения: новые данные, старые или всё вместе."""
        if any(self._change.old_is_none_mask):
            if all(self._change.old_is_none_mask):
                return CHANGE_NEW
            else:
                return CHANGE_MIXED
        return CHANGE_DIFF

    def _save_change_info(self, diffs, user):
        u"""Сохраняет diff в модель с примененными изменениями."""
        data = M3JSONEncoder().encode(diffs)

        # FIXME: Убрать workaround в следующей мажорной версии.
        # Данный класс не должен ничего знать о моделях GetData!
        if isinstance(self._change.source, GetDataPerson):
            person = self._change.source.person
        elif isinstance(self._change.source, GetDataPersonDocument):
            person = self._change.source.person.person
        else:
            raise AssertionError('Wrong type of source for change object!')

        GetDataChanges.objects.create(
            record=person,
            session_id=self._change.source.session_id,
            data=data,
            user=user,
            status=GetDataRecordStatus.ACCEPT
        )

    def _match_changed_fields(self, fields):
        u"""Определяет, совпадают ли переданные поля с измененными."""
        changed_fields = set((row.id for row in self.diff))
        fields = set(fields)
        return len(changed_fields - fields) == 0

    @atomic
    def apply(self, user, only_fields=None):
        u"""Применяет изменения.

        :param user: Пользователь, применивший изменения.
        :type user: extedu.user.models.User
        :param only_fields: Поля, для которых необходимо применить изменение,
                            если не указано, то для всех.
        :type collections.Iterable or None
        """
        result = self._change.apply(only_fields)
        if result:
            if isinstance(result, dict):
                result = [result]
            self._save_change_info(result, user)
        if only_fields is None or self._match_changed_fields(only_fields):
            self._change.source.status = GetDataRecordStatus.ACCEPT
            self._change.source.save()


class AppliedChangeViewer(object):

    u"""Класс для просмотра примененных изменений."""
    
    hidden_fields = tuple()

    def __init__(self, change):
        assert isinstance(change, GetDataChanges), type(change)
        self._change = change

    @property
    def old(self):
        u"""Старые значения полей.

        :return tuple: ((имя_поля, значение))
        """
        return tuple((row.name, row.old) for row in self.diff)

    @property
    def new(self):
        u"""Новые значения полей.

        :return tuple: ((имя_поля, значение), ...)
        """
        return tuple((row.name, row.new) for row in self.diff)

    @cached_property
    def diff(self):
        u"""Список различий всех объектов-изменений.

        :return tuple: ((идентификатор_поля, имя_поля,
                         старое_значение, новое_начение),)
        """
        result = []
        for obj in self._data:

            model_id = obj['model_id']
            model = ContentType.objects.get_for_id(model_id).model_class()
            result += tuple(
                DiffField(
                    field,
                    self._get_field_name_display(model, field),
                    get_value_display(model, field, old),
                    get_value_display(model, field, new)
                )
                for field, old, new in obj['diff']
                if field not in self.hidden_fields
            )
        return result

    def _get_field_name_display(self, model, field):
        u"""Возвращает текстовое описание поля модели."""
        return get_field_name_display(model, field)

    @property
    def change_type(self):
        u"""Тип изменения: новые данные, старые или всё вместе."""
        is_none = tuple(obj['diff'][0] is None for obj in self._data)
        if any(is_none):
            if all(is_none):
                return CHANGE_NEW
            else:
                return CHANGE_MIXED
        return CHANGE_DIFF

    @cached_property
    def _data(self):
        u"""Информация об изменениях.

        Записанный в БД результат метода `apply()` изменения
        или группы изменений.
        """
        return json.JSONDecoder().decode(self._change.data)
