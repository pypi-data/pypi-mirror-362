# coding: utf-8

from __future__ import absolute_import

from datatransfer.source.common.configuration import get_object

from educommon.utils.ui import formed
from m3.actions.exceptions import ApplicationLogicException
from m3_ext.ui.containers import ExtContainer
from m3_ext.ui.containers import ExtFieldSet
from m3_ext.ui.containers import ExtRadioGroup
from m3_ext.ui.containers.container_complex import ExtContainerTable
from m3_ext.ui.containers.grids import ExtGrid
from m3_ext.ui.containers.grids import ExtGridCheckBoxSelModel
from m3_ext.ui.controls import ExtButton
from m3_ext.ui.fields import ExtDisplayField
from m3_ext.ui.fields.simple import ExtDateField
from m3_ext.ui.fields.simple import ExtRadio
from m3_ext.ui.icons import Icons
from m3_ext.ui.misc.store import ExtDataStore
from objectpack.ui import BaseEditWindow
from objectpack.ui import BaseListWindow
from objectpack.ui import BaseWindow
from objectpack.ui import ComboBoxWithStore

from .models import GetDataChanges
from .models import GetDataPerson
from .models import GetDataPersonDocument
from .models import GetDataRecordStatus
from .constants import PERIOD_CHOICES


extensions = get_object('get_data_extensions')()


class GetDataSettingsWindow(BaseEditWindow):

    u"""Окно настроек получения данных из Контингента."""

    def _init_components(self):
        super(GetDataSettingsWindow, self)._init_components()

        self.title = u'Настройка получения данных из Контингента'

        self.replace_container = ExtFieldSet(
            flex=1,
            label_width=230,
            title=u'Настройки получения данных',
        )

        self.radio_group = ExtRadioGroup(
            columns=1,
            hide_label=True
        )
        self.radio_group.items.extend([
            ExtRadio(
                box_label=u'Заменять заполненные значения на пустые',
                name='replace_empty',
                value=True
            ),
            ExtRadio(
                box_label=u'Не заменять заполненные значения на пустые',
                name='replace_empty',
                value=False
            )
        ])

        self.autorun_container = ExtFieldSet(
            flex=1,
            label_width=130,
            title=u'Настройки автоматического запуска',
        )
        self.autorun_combobox = ComboBoxWithStore(
            name='autorun_period',
            label=u'Периодичность',
            data=PERIOD_CHOICES,
            allow_blank=False
        )

    def _do_layout(self):
        super(GetDataSettingsWindow, self)._do_layout()
        self.replace_container.items.append(self.radio_group)
        self.autorun_container.items.append(self.autorun_combobox)
        self.form.items.extend(
            (self.replace_container, self.autorun_container)
        )

    def set_params(self, params):
        super(GetDataSettingsWindow, self).set_params(params)
        if params['replace_empty']:
            self.radio_group.items[0].checked = True
        else:
            self.radio_group.items[1].checked = True

        combobox = self.autorun_combobox
        combobox.value = params['autorun_period']
        combobox.default_text = dict(combobox.data)

        self.width = 420


class GetDataListWindow(BaseListWindow):

    u"""Окно просмотра списка выгрузок."""

    def _init_components(self):
        super(GetDataListWindow, self)._init_components()
        self.from_date = ExtDateField(label=u'Период с', name='from_date')
        self.to_date = ExtDateField(label=u'по', name='to_date')

        self.top_container_table = ExtContainerTable(
            columns=2, rows=1, height=40,
            region='north', style={'padding': '5px'}
        )

        self.view_btn = ExtButton(
            text=u"Просмотр",
            handler='viewWindow',
            icon_cls=Icons.APPLICATION_VIEW_DETAIL
        )

    def _do_layout(self):
        super(GetDataListWindow, self)._do_layout()
        self.layout = 'border'

        self.top_container_table.set_item(
            row=0, col=0, cmp=self.from_date,
            width=180, label_width=60
        )
        self.top_container_table.set_item(
            row=0, col=1, cmp=self.to_date,
            width=150, label_width=20
        )

        self.grid.top_bar.items.insert(0, self.view_btn)
        self.items.insert(0, self.top_container_table)

    def set_params(self, params):
        super(GetDataListWindow, self).set_params(params)
        self.width = 800
        self.template_globals = 'get_data/get-data-list-window.js'
        self.grid.region = 'center'
        self.view_window_url = params['view_window_url']


class PersonDataListWindow(BaseListWindow):

    u"""Окно просмотра данных физ. лиц из контингента."""

    def _init_components(self):
        super(PersonDataListWindow, self)._init_components()
        self.grid.top_bar.button_apply = ExtButton(
            text=u'Принять изменения из Контингента',
            icon_cls='icon-application-view-detail',
            handler='apply_changes'
        )

    def _do_layout(self):
        super(PersonDataListWindow, self)._do_layout()
        self.grid.top_bar.items.insert(0, self.grid.top_bar.button_apply)

    def set_params(self, params):
        super(PersonDataListWindow, self).set_params(params)
        self.grid.sm = ExtGridCheckBoxSelModel()
        self.apply_url = params['apply_url']
        self.template_globals = 'get_data/person-data-list-window.js'
        self.grid.top_bar.button_edit.text = u'Просмотр'

        self.width = 900


class StatisticsListWindow(BaseListWindow):

    u"""Окно просмотра Протокола (статистики) запроса."""

    def _init_components(self):
        super(StatisticsListWindow, self)._init_components()

        self.session_field = ExtDisplayField(
            label=u'Сессия', style={'padding-top': '3px'}
        )
        self.date_field = ExtDisplayField(
            label=u'Дата и время', style={'padding-top': '3px'}
        )
        self.info_bar = ExtContainer(
            layout='hbox', flex=1
        )
        self.buttons_bar = ExtContainer(
            layout='hbox', flex=1
        )
        self.top_region = ExtContainer(
            region='north', layout='vbox', layout_config={'align': 'stretch'},
            height=64
        )

        self.view_data_button = ExtButton(
            text=u'Перейти к просмотру данных в реестре',
            handler='viewData',
            style={'margin-left': '5px'}
        )

    def _do_layout(self):
        super(StatisticsListWindow, self)._do_layout()

        self.layout = 'border'

        self.info_bar.items.extend((
            formed(
                self.session_field, flex=1,
                style=dict(padding='5px'), label_width=50
            ),
            formed(self.date_field, flex=1, style=dict(padding='5px'))
        ))
        self.buttons_bar.items.extend((
            self.view_data_button, ExtContainer(width=10)
        ))
        self.top_region.items.extend((
            self.info_bar, self.buttons_bar
        ))

        self.grid.top_bar.hidden = True
        self.grid.region = 'center'

        self.items[:] = self.top_region, self.grid

    def set_params(self, params):
        super(StatisticsListWindow, self).set_params(params)
        self.width, self.height = 700, 400
        session = params['session']
        self.session_field.value = session.session
        self.date_field.value = session.timestamp.strftime(
            '%d.%m.%Y %H:%M:%S'
        )
        self.view_window_url = params['view_window_url']
        self.session_id = params['session'].id
        self.template_globals = 'get_data/statistics-list-window.js'


class ChangesEditWindow(BaseWindow):

    u"""Окно редактирования/просмотра истории изменений."""

    def _init_components(self):
        super(ChangesEditWindow, self)._init_components()

        self.grid = ExtGrid()
        self.grid.add_column(header=u'Поле', data_index='field')
        self.grid.add_column(header=u'Старое значение', data_index='old')
        self.grid.add_column(header=u'Новое значение', data_index='new')
        self.grid.sm = ExtGridCheckBoxSelModel()

        self.apply_button = ExtButton(
            text=u'Применить изменения', icon_cls=Icons.ACCEPT,
            handler='applyChanges'
        )
        self.cancel_button = ExtButton(
            text=u'Закрыть', handler='closeChangesWindow'
        )
        self._mro_exclude_list.append(self.cancel_button)

    def _do_layout(self):
        super(ChangesEditWindow, self)._do_layout()

        self.items.append(self.grid)
        self.layout = 'fit'
        self.grid.cls = 'word-wrap-grid'

        self.buttons.extend((self.apply_button, self.cancel_button,))

    def set_params(self, params):
        super(ChangesEditWindow, self).set_params(params)

        self.width, self.height = 600, 300
        self.template_globals = 'get_data/changes-edit-window.js'

        # Используется в js шаблоне, передаётся в параметром в apply_url
        self.change_id = params['change_id']
        self.apply_url = params['apply_changes_url']

        obj = params['object']

        if isinstance(obj, (GetDataPerson, GetDataPersonDocument)):
            change = extensions.get_change(obj, True)
            result = change.diff
        elif (isinstance(obj, GetDataChanges) and
                obj.status == GetDataRecordStatus.ACCEPT):
            raise ApplicationLogicException(
                u'Изменения уже были приняты'
            )
        else:
            raise ApplicationLogicException(
                u'Невозможно изменить данную запись'
            )

        self.grid.store = ExtDataStore(result)
