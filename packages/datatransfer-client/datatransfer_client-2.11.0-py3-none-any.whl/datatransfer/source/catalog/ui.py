# -*- coding: utf-8 -*-

from __future__ import absolute_import

from m3.actions import ControllerCache
from m3_ext.ui import all_components as ext
from m3_ext.ui.icons import Icons
from objectpack import ui


class FeedBackListWindow(ui.BaseListWindow):
    u"""Окно просмотра списка выгрузок."""

    def _init_components(self):
        super(FeedBackListWindow, self)._init_components()
        self.from_date = ext.ExtDateField(label=u"Период с", name="from_date")
        self.to_date = ext.ExtDateField(label=u"по", name="to_date")

        self.top_container_table = ext.ExtContainerTable(
            columns=2, rows=1, height=40,
            region='north', style={'padding': '5px'})

        self.view_btn = ext.ExtButton(
            text=u"Просмотр",
            handler="viewWindow",
            icon_cls=Icons.APPLICATION_VIEW_DETAIL)

    def _do_layout(self):
        super(FeedBackListWindow, self)._do_layout()
        self.layout = "border"

        self.top_container_table.set_item(
            row=0, col=0, cmp=self.from_date,
            width=180, label_width=60)
        self.top_container_table.set_item(
            row=0, col=1, cmp=self.to_date,
            width=150, label_width=20)

        self.grid.top_bar.items.insert(0, self.view_btn)
        self.items.insert(0, self.top_container_table)

    def set_params(self, params):
        super(FeedBackListWindow, self).set_params(params)
        self.width = 800
        self.template_globals = "ui-js/feedback-list-window.js"
        self.grid.region = "center"
        self.view_window_url = params["view_window_url"]


class FeedBackViewWindow(ui.BaseWindow):
    u"""Окно просмотра деталей выгрузки."""

    def _init_components(self):
        super(FeedBackViewWindow, self)._init_components()
        self.north_panel = ext.ExtPanel(layout="border", anchor="100% 50%")
        self.statistic_top_bar = ext.ExtContainerTable(
            columns=2, rows=2, height=70,
            region="north", style={"padding": "5px"})
        self.session_field = ext.ExtDisplayField(
            label=u"Сессия", name="session")
        self.date_time_field = ext.ExtDisplayField(
            label=u"Дата и время", name="date_time")
        self.statistic_grid = ext.ExtObjectGrid(
            region="center", anchor="100%", flex=1)
        self.print_btn = ext.ExtButton(
            text=u"Печать ошибок", handler="printReport")
        self.load_detail_data = ext.ExtButton(
            text=u"Выгрузить ошибки", handler="loadErrors", disabled=True)

        self.errors_top_bar = ext.ExtContainerTable(
            columns=3, rows=1, height=50,
            region="north", style={"padding": "5px"})
        self.view_btn = ext.ExtButton(
            text=u"Просмотр", handler="detailErrorWindow",
            icon_cls=Icons.APPLICATION_VIEW_DETAIL)
        self.errors_grid = ext.ExtObjectGrid(
            anchor="100% 50%", flex=1)

        self.feedback_hidden_fld = ext.ExtHiddenField(
            type=ext.ExtHiddenField.INT)

    def _do_layout(self):
        super(FeedBackViewWindow, self)._do_layout()
        self.layout = "anchor"

        self.statistic_top_bar.set_item(
            row=0, col=0, cmp=self.session_field, width=400, label_width=100)
        self.statistic_top_bar.set_item(
            row=0, col=1, cmp=self.date_time_field,
            width=200, label_width=100)
        self.statistic_top_bar.set_item(
            row=1, col=0, cmp=self.print_btn, width=100)
        self.statistic_top_bar.set_item(
            row=1, col=1, cmp=self.load_detail_data, width=120)
        self.north_panel.items.extend([
            self.statistic_top_bar,
            self.statistic_grid
        ])

        self.errors_grid.top_bar.items.insert(0, self.view_btn)

        self.items.extend([
            self.north_panel,
            self.errors_grid,
            self.feedback_hidden_fld
        ])

    def set_params(self, params):
        super(FeedBackViewWindow, self).set_params(params)

        self.template_globals = "ui-js/feedback-view-window.js"

        self.session_field.value = params.get("session")
        self.date_time_field.value = params.get("date_time")
        self.feedback_hidden_fld.value = params.get("feedback_id")

        statistic_pack = ControllerCache.find_pack(
            "datatransfer.source.catalog.actions.StatisticFeedBackPack")
        statistic_pack.configure_grid(self.statistic_grid)
        self.statistic_grid.top_bar.button_refresh.hidden = True

        error_details_pack = ControllerCache.find_pack(
            "datatransfer.source.catalog.actions.ErrorDetailPack")
        error_details_pack.configure_grid(self.errors_grid)
        self.errors_grid.store.auto_load = False

        self.error_detail_window_url = params["error_detail_window_url"]
        self.error_save_url = params["error_save_url"]
        self.upload_action = params["upload_action"]
        self.report_action = params["report_action"]

        self.load_detail_data.disabled = not params["active_upload_button"]

        self.title = u"Протокол"
        self.width = 800
        self.height = 500

        return params


class DetailErrorWindow(ui.BaseWindow):
    u"""Окно с представлением об ошибках выгрузки."""

    def _init_components(self):
        super(DetailErrorWindow, self)._init_components()

        field_common_params = {
            "read_only": True,
            "anchor": "100%"
        }

        self.model = ext.ExtStringField(
            label=u"Модель", name="model", **field_common_params)
        self.record_id = ext.ExtStringField(
            label=u"ID записи", name="record_id", **field_common_params)
        self.record_name = ext.ExtTextArea(
            label=u"Наименование", name="name",
            height=100, **field_common_params)
        self.message = ext.ExtTextArea(
            label=u"Сообщение", name="message", **field_common_params)

    def _do_layout(self):
        super(DetailErrorWindow, self)._do_layout()

        self.items.extend([
            self.model,
            self.record_id,
            self.record_name,
            self.message
        ])

    def set_params(self, params):
        super(DetailErrorWindow, self).set_params(params)

        self.layout = "form"
        self.title = u"Сообщение об ошибке"
        self.height = 300

        self.model.value = params["model"]
        self.record_id.value = params["record_id"]
        self.record_name.value = params["record_name"]
        self.message.value = params["message"]
