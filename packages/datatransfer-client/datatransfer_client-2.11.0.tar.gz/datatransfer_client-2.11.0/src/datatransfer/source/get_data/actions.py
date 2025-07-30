# coding: utf-8
from __future__ import absolute_import

from datetime import datetime
from datetime import time
from functools import partial
import logging

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from educommon.m3 import convert_validation_error_to
from educommon.m3 import get_id_value
from educommon.utils.ui import ChoicesFilter
from m3 import ApplicationLogicException
from m3.actions.results import OperationResult
from m3.actions.utils import create_search_filter
from objectpack.actions import BaseAction
from objectpack.actions import BaseWindowAction
from objectpack.actions import ObjectPack
from objectpack.exceptions import ValidationError as ObjectPackValidationError
from objectpack.filters import ColumnFilterEngine
from objectpack.filters import FilterByField

from .changes.models import ChangesVirtualModel
from .models import GetDataPerson
from .models import GetDataPersonDocument
from .models import GetDataSession
from .models import GetDataStatistic
from .ui import ChangesEditWindow
from .ui import GetDataListWindow
from .ui import GetDataSettingsWindow
from .ui import PersonDataListWindow
from .ui import StatisticsListWindow

from datatransfer.source.common.configuration import get_object


extensions = get_object('get_data_extensions')()
get_data_config = get_object("get_data_config")()


class GetDataSessionPack(ObjectPack):

    u"""Пак реестра сессий загрузки данных из контенгента."""

    title = u'Реестр операций'
    model = GetDataSession

    _is_primary_for_model = False

    list_window = GetDataListWindow

    columns = [
        dict(
            header=u'Сессия',
            data_index='session',
            sortable=True,
        ),
        dict(
            header=u"Дата и время",
            data_index='timestamp',
            sortable=True,
        ),
        dict(
            header=u'Результат',
            data_index='processed',
            sortable=True,
        ),
        dict(
            header=u'Комментарий',
            data_index='message',
            sortable=True,
        )
    ]

    list_sort_order = ('-timestamp',)

    def __init__(self):
        super(GetDataSessionPack, self).__init__()

        self.person_data_pack = PersonDataPack()
        self.statistics_pack = StatisticPack()
        self.subpacks.extend((
            self.person_data_pack, self.statistics_pack
        ))
        self.settings_action = GetDataSettingsWindowAction()
        self.update_settings_action = GetDataSettingsAction()
        self.get_data_action = GetDataAction()
        self.actions.extend((
            self.get_data_action,
            self.settings_action,
            self.update_settings_action
        ))

    def declare_context(self, action):
        result = super(GetDataSessionPack, self).declare_context(action)

        if action is self.rows_action:
            result['from_date'] = dict(
                type="date_or_none",
                default=None
            )
            result['to_date'] = dict(
                type='date_or_none',
                default=None
            )

        return result

    def get_rows_query(self, request, context):
        query = super(GetDataSessionPack, self).get_rows_query(
            request, context
        )

        if context.from_date:
            from_time = datetime.combine(context.from_date, time(0))
            query = query.filter(timestamp__gte=from_time)

        if context.to_date:
            to_time = datetime.combine(
                context.to_date,
                time(hour=23, minute=59, second=59, microsecond=999999)
            )
            query = query.filter(timestamp__lte=to_time)

        return query

    def get_list_window_params(self, params, request, context):
        params = super(
            GetDataSessionPack, self
        ).get_list_window_params(params, request, context)

        params['view_window_url'] = (
            self.statistics_pack.list_window_action.get_absolute_url()
        )

        return params

    def extend_menu(self, menu):
        return menu.administry(
            menu.SubMenu(
                u'Взаимодействие с ИС "Контингент"',
                menu.SubMenu(
                    u'Получение данных из контингента',
                    menu.Item(u'Запуск', self.get_data_action),
                    menu.Item(u'Результаты', self.list_window_action),
                    menu.Item(u'Настройки', self.settings_action),
                )
            )
        )


class StatisticPack(ObjectPack):
    title = u'Протокол'
    model = GetDataStatistic

    _is_primary_for_model = False

    list_window = StatisticsListWindow

    columns = [
        dict(
            header=u'Модель',
            data_index='model_name',
        ),
        dict(
            header=u"Получено",
            data_index='count',
        )
    ]

    def declare_context(self, action):
        result = super(StatisticPack, self).declare_context(action)

        if action in (self.list_window_action, self.rows_action):
            result['session_id'] = dict(type=int)

        return result

    def prepare_row(self, obj, request, context):
        obj = super(StatisticPack, self).prepare_row(obj, request, context)
        obj.model_name = obj.model.model_class()._meta.verbose_name
        return obj

    def get_rows_query(self, request, context):
        query = super(StatisticPack, self).get_rows_query(request, context)
        query = query.filter(session_id=context.session_id)
        return query

    def get_list_window_params(self, params, request, context):
        params = super(StatisticPack, self).get_list_window_params(
            params, request, context
        )

        sessions = self.parent.model.objects
        session = sessions.get(id=context.session_id)
        params['session'] = session

        try:
            latest_id = sessions.filter(processed=True).latest('id').id
        except self.parent.model.DoesNotExist:
            latest_id = 0
        if latest_id == session.id:
            # Показываем окно просмотра изменений только для последней сессии.
            view_pack = self.parent.person_data_pack
            view_url = view_pack.list_window_action.get_absolute_url()
        else:
            view_url = ''
        params['view_window_url'] = view_url
        return params


class GetDataAction(BaseAction):

    def run(self, request, context):
        from datatransfer.source.get_data.tasks import get_data_task

        get_data_task.apply_async([], {})
        return OperationResult(
            message=(
                u'Процесс получения данных запущен'
            )
        )


class PersonDataPack(ObjectPack):

    u"""Пак для данных о физ. лицах, полученных из контингента."""

    title = u'Данные из Контингента обучающихся'
    model = GetDataPerson

    list_window = PersonDataListWindow
    edit_window = ChangesEditWindow

    can_delete = False

    gender_map = {'Male': u'мужской', 'Female': u'женский'}

    filter_engine_clz = ColumnFilterEngine
    ff = partial(FilterByField, GetDataPerson)

    _full_name_fields = ('last_name', 'first_name', 'middle_name')

    columns = [
        dict(
            data_index='index',
            header=u'№',
            width=2,
            column_renderer='numRenderer',
        ),
        dict(
            data_index='full_name',
            header=u'ФИО',
            width=15,
            filter=ff(
                field_name='last_name',
                lookup=partial(create_search_filter, fields=_full_name_fields),
            ),
            sortable=True,
            sort_fields=('last_name', 'first_name', 'middle_name')
        ),
        dict(
            data_index='birth_date',
            header=u'Дата рождения',
            width=6,
            filter=ff('birth_date'),
            sortable=True,
        ),
        dict(
            data_index='snils',
            header=u'СНИЛС',
            width=8,
            filter=ff('snils'),
            sortable=True,
        ),
        dict(
            data_index='gender_str',
            width=4,
            header=u'Пол',
            filter=ChoicesFilter(
                choices=list(gender_map.items()),
                parser=str,
                lookup='gender',
                tooltip=u'Пол',
            ),
            sortable=True,
            sort_fields=('gender',)
        ),
        dict(
            data_index='birth_place',
            header=u'Место рождения',
            width=15,
            filter=ff('birth_place'),
            sortable=True,
        ),
        dict(
            data_index='status',
            header=u'Статус данных',
            width=10,
            filter=ff('status'),
            sortable=True,
        ),
    ]

    def __init__(self):
        super(PersonDataPack, self).__init__()
        self.apply_changes_action = ApplyChangesAction()
        self.partial_apply_change_action = PartialApplyChangesAction()
        self.actions.extend((
            self.apply_changes_action,
            self.partial_apply_change_action
        ))

    def declare_context(self, action):
        result = super(PersonDataPack, self).declare_context(action)

        if action in (self.list_window_action, self.rows_action):
            result['session_id'] = dict(type=int)

        return result

    def get_rows_query(self, request, context):
        query = super(PersonDataPack, self).get_rows_query(request, context)
        query = query.filter(session_id=context.session_id)
        return query

    def prepare_row(self, obj, request, context):
        obj.full_name = u' '.join(
            (obj.last_name or '', obj.first_name or '', obj.middle_name or '')
        )
        obj.gender_str = self.gender_map.get(obj.gender, obj.gender)
        return obj

    def format_window_title(self, action):
        return u'{}: {}'.format(u'Изменения', action)

    def get_list_window_params(self, params, request, context):
        params = super(PersonDataPack, self).get_list_window_params(
            params, request, context
        )
        params['apply_url'] = self.apply_changes_action.get_absolute_url()
        return params

    def get_edit_window_params(self, params, request, context):
        params = super(PersonDataPack, self).get_edit_window_params(
            params, request, context
        )
        apply_url = self.partial_apply_change_action.get_absolute_url()
        params['apply_changes_url'] = apply_url

        params['change_id'] = ChangesVirtualModel.get_id(
            GetDataPerson, get_id_value(context, self)
        )
        return params


class ApplyChangesAction(BaseAction):

    u"""Экшен применения изменений для группы физ. лиц."""

    def context_declaration(self):
        result = super(ApplyChangesAction, self).context_declaration()
        result['persons'] = dict(type='int_list')
        return result

    def run(self, request, context):
        try:
            extensions.apply_changes(
                context.persons, request, get_data_config.replace_empty
            )

        except (ValidationError, ObjectPackValidationError,
                ValueError, IntegrityError) as e:
            logger = logging.getLogger(__package__)
            logger.error(e)
            return OperationResult(
                success=False,
                message=u'При применении изменений произошла ошибка валидации.'
            )
        return OperationResult()


class BasePartialApplyChangesAction(BaseAction):

    u"""Базовый экшен применения изменений по выбранным полям."""

    def context_declaration(self):
        result = super(
            BasePartialApplyChangesAction, self).context_declaration()
        result['fields'] = dict(type='str_list')
        return result

    @convert_validation_error_to(ApplicationLogicException)
    def run(self, request, context):
        change_info = ChangesVirtualModel.get_instance(context.change_id)
        if isinstance(change_info, (GetDataPerson, GetDataPersonDocument)):
            change = extensions.get_change(change_info, True)
            change.apply(extensions.get_current_user(request), context.fields)
            return OperationResult()
        else:
            return OperationResult(
                message=(
                    u'Для такого типа записи нельзя применять изменения'
                ),
                success=False
            )


class PartialApplyChangesAction(BasePartialApplyChangesAction):

    u"""Экшен применения изменений по выбранным полям."""


class GetDataSettingsWindowAction(BaseWindowAction):

    u"""Экшен показа окна настроек контингента."""

    def create_window(self):
        self.win = GetDataSettingsWindow()

    def set_window_params(self):
        self.win_params['form_url'] = (
            self.parent.update_settings_action.get_absolute_url()
        )

        self.win_params['replace_empty'] = get_data_config.replace_empty
        self.win_params['autorun_period'] = get_data_config.autorun_period


class GetDataSettingsAction(BaseAction):

    u"""Экшен применения настроек контингента."""

    def context_declaration(self):
        result = super(GetDataSettingsAction, self).context_declaration()
        result['replace_empty'] = dict(type='boolean')
        result['autorun_period'] = dict(type='str')
        return result

    def run(self, request, context):
        get_data_config.replace_empty = context.replace_empty
        get_data_config.autorun_period = context.autorun_period
        return OperationResult()
