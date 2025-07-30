# coding: utf-8
from __future__ import absolute_import

from datatransfer.source.common.configuration import get_object
from datatransfer.source.get_data.changes.models import ChangesVirtualModel

from educommon.m3 import get_id_value
from objectpack.actions import ObjectPack
import six

from ..actions import BasePartialApplyChangesAction
from ..ui import ChangesEditWindow


extensions = get_object('get_data_extensions')()


class GetDataChangesPack(ObjectPack):

    u"""Пак для вкладки "История изменений" портфолио учащегося."""

    model = ChangesVirtualModel

    edit_window = ChangesEditWindow

    can_delete = False

    # Renderer колонки преформатированного текста.
    # Пробельные символы из ячейки не убираются. Не влияет на шрифт.
    pre_whitespace_renderer = (
        'function(value, metaData){'
            'metaData.attr += \'style="white-space: pre;"\';'
            'return value;'
        '}'
    )

    columns = [
        {
            'data_index': 'timestamp',
            'header': u'Дата и время получения'
        },
        {
            'data_index': 'user_name',
            'header': u'Пользователь'
        },
        {
            'data_index': 'old_str',
            'header': u'Старое значение',
            'column_renderer': pre_whitespace_renderer
        },
        {
            'data_index': 'new_str',
            'header': u'Новое значение',
            'column_renderer': pre_whitespace_renderer
        },
        {
            'data_index': 'comment',
            'header': u'Комментарий'
        },
        {
            'data_index': 'status',
            'header': u'Статус'
        },
    ]

    def __init__(self):
        super(GetDataChangesPack, self).__init__()

        self.apply_changes_action = ApplyChangesAction()
        self.actions.append(self.apply_changes_action)

    def configure_grid(self, grid):
        u"""Конфигурирование грида.

        Добавляется css класс для переноса строк в ячейках грида.
        """
        super(GetDataChangesPack, self).configure_grid(grid)
        grid.cls = 'word-wrap-grid'

    def declare_context(self, action):
        result = super(GetDataChangesPack, self).declare_context(action)

        if self.id_param_name in result:
            result[self.id_param_name] = {'type': str}
        return result

    def format_window_title(self, action):
        return u'{}: {}'.format(u'Изменения', action)

    def get_edit_window_params(self, params, request, context):
        params = super(GetDataChangesPack, self).get_edit_window_params(
            params, request, context
        )
        apply_url = self.apply_changes_action.get_absolute_url()
        params['apply_changes_url'] = apply_url
        params['change_id'] = get_id_value(context, self)
        return params

    @staticmethod
    def _get_user_name(user_obj):
        u"""Возвращает имя пользователя по его объекту.

        :param user_obj: Пользователь или его имя.
        :type user_obj: unicode or django.db.models.Model

        :return: Имя пользователя.
        :rtype: unicode
        """
        return six.text_type(user_obj)

    def prepare_row(self, obj, request, context):
        obj = super(GetDataChangesPack, self).prepare_row(
            obj, request, context
        )

        def to_str(data):
            return u'\n'.join(
                u'{}: {}'.format(*row) for row in data
            )
        obj.old_str = to_str(obj.old)
        obj.new_str = to_str(obj.new)
        obj.user_name = self._get_user_name(obj.user)

        return obj

    def get_row(self, row_id):
        return self.model.get_instance(row_id)

    def get_rows_query(self, request, context):
        query = super(GetDataChangesPack, self).get_rows_query(
            request, context
        )
        return query


class ApplyChangesAction(BasePartialApplyChangesAction):

    u"""Экшен применения изменений по выбранным полям."""
