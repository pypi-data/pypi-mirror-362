# -*- coding: utf-8 -*-
from __future__ import absolute_import

from datatransfer.source.common.configuration import get_object

from m3.actions import ApplicationLogicException
from m3.actions import ControllerCache
from m3.actions.results import OperationResult
from m3_ext.ui.containers.grids import ExtGridRowSelModel
from m3_ext.ui.fields.simple import ExtCheckBox

from objectpack.actions import BaseAction
from objectpack.actions import BaseWindowAction
from objectpack.actions import ObjectListWindowAction
from objectpack.actions import ObjectPack
from objectpack.actions import ObjectRowsAction

from . import permissions
from .models import FeedBack
from .models import FeedBackDetails
from .models import FeedBackStatistic
from .project_models.common import project_models_class
from .report.report import FeedbackReporter
from .tasks import update_feedback_details
from .ui import DetailErrorWindow
from .ui import FeedBackListWindow
from .ui import FeedBackViewWindow


class FeedBackPack(ObjectPack):
    u"""Пак для отображения результатов выгрузки."""

    __PERMISSION_NS = "datatransfer.source.catalog.actions.FeedBackPack"

    title = u'Реестр взаимодействия с ИС "Контингент обучающихся"'

    model = FeedBack
    list_window = FeedBackListWindow
    need_check_permission = True

    sub_permissions = permissions.PACK_SUB_PERMISSIONS

    columns = [
        {
            "header": u"Сессия",
            "data_index": "session"
        },
        {
            "header": u"Дата и время",
            "data_index": "date_time"
        },
        {
            "header": u"Результат",
            "data_index": "result"
        },
        {
            "header": u"Комментарий",
            "data_index": "comment"
        }
    ]

    def __init__(self):
        super(FeedBackPack, self).__init__()
        self.view_win_action = ViewWinAction()

        self.actions.extend([
            self.view_win_action,
        ])
        self.replace_action("list_window_action", FeedBackListWindowAction())

    def declare_context(self, action):
        result = super(FeedBackPack, self).declare_context(action)

        if action is self.rows_action:
            result["from_date"] = {
                "type": "date_or_none",
                "default": None
            }
            result["to_date"] = {
                "type": "date_or_none",
                "default": None
            }
        elif action is self.view_win_action:
            result["feedback"] = {
                "type": int
            }

        return result

    def get_rows_query(self, request, context):
        query = super(FeedBackPack, self).get_rows_query(request, context)

        if context.from_date:
            query = query.filter(date_time__gte=context.from_date)
        if context.to_date:
            query = query.filter(date_time__lte=context.to_date)

        return query

    def get_list_window_params(self, params, request, context):
        parameters = super(
            FeedBackPack, self
        ).get_list_window_params(params, request, context)

        parameters["view_window_url"] = (
            self.view_win_action.get_absolute_url())

        return parameters

    def extend_menu(self, menu):
        return menu.Item(
            u"Контингент обучающихся",
            self.list_window_action
        )


class FeedBackListWindowAction(ObjectListWindowAction):
    u"""Переопределен для спецификации perm_code для ЭДС"""

    perm_code = "view"
    verbose_name = u"Просмотр результатов выгрузки"

    need_check_permission = True


class ViewWinAction(BaseWindowAction):
    u"""Экшен показа окна просмотра выгрузки."""

    def create_window(self):
        self.win = FeedBackViewWindow()

    def set_window_params(self):
        super(ViewWinAction, self).set_window_params()

        try:
            feedback = FeedBack.objects.get(id=self.context.feedback)
        except FeedBack.DoesNotExist:
            raise ApplicationLogicException(
                u"Не найдена выгрузка с идентификатором ID={0}".format(
                    self.context.feedback)
            )

        self.win_params["session"] = feedback.session
        self.win_params["feedback_id"] = feedback.id
        self.win_params["date_time"] = feedback.date_time
        self.win_params["error_detail_window_url"] = (
            ControllerCache.find_pack(
                "datatransfer.source.catalog.actions.ErrorDetailPack"
            ).error_detail_win_action.get_absolute_url()
        )
        self.win_params["error_save_url"] = ControllerCache.find_pack(
            "datatransfer.source.catalog.actions.ErrorDetailPack"
        ).save_action.get_absolute_url()
        self.win_params["upload_action"] = ControllerCache.find_pack(
            "datatransfer.source.catalog.actions.ErrorDetailPack"
        ).upload_action.get_absolute_url()
        self.win_params["active_upload_button"] = (
            not FeedBackDetails.objects.filter(
                feedback_statistic__feedback=feedback).exists())
        self.win_params["report_action"] = ControllerCache.find_pack(
            "datatransfer.source.catalog.actions.ErrorDetailPack"
        ).report_action.get_absolute_url()


class StatisticFeedBackPack(ObjectPack):
    u"""Пак для отображения статистики выгрузки."""

    model = FeedBackStatistic
    allow_paging = False

    columns = [
        {
            "header": u"Модель",
            "data_index": "model_verbose"
        },
        {
            "header": u"Всего",
            "data_index": "total"
        },
        {
            "header": u"Обработано",
            "data_index": "processed"
        },
        {
            "header": u"Создано",
            "data_index": "created"
        },
        {
            "header": u"Обновлено",
            "data_index": "updated"
        },
        {
            "header": u"Некорректных",
            "data_index": "invalid"
        }
    ]

    def declare_context(self, action):
        result = super(StatisticFeedBackPack, self).declare_context(action)

        if action == self.rows_action:
            result["feedback"] = {"type": "int_or_zero"}

        return result

    def configure_grid(self, grid):
        super(StatisticFeedBackPack, self).configure_grid(grid)
        grid.sm = ExtGridRowSelModel()
        grid.sm.single_select = True

    def get_rows_query(self, request, context):
        query = super(
            StatisticFeedBackPack, self
        ).get_rows_query(request, context)

        return query.filter(feedback=context.feedback)


class ErrorDetailPack(ObjectPack):
    u"""Пак для отображения деталей ошибок."""

    model = FeedBackDetails

    id_param_name = "record_id"
    search_fields = ("record_id",)
    select_related = ("feedback_statistic", )

    columns = [
        {
            "header": u"Модель",
            "data_index": "feedback_statistic.model_verbose",
            "flex": 4
        },
        {
            "header": u"ID записи",
            "data_index": "record_id",
            "flex": 1
        },
        {
            "header": u"Наименование",
            "data_index": "record_name",
            "flex": 4
        },
        {
            "header": u"Сообщение",
            "data_index": "message",
            "flex": 4
        }
    ]

    def __init__(self):
        super(ErrorDetailPack, self).__init__()
        self.save_action = ErrorSaveAction()
        self.upload_action = ErrorWindowUploadAction()
        self.error_detail_win_action = ErrorDetailWindowAction()
        self.report_action = PrintDetailsReportAction()

        self.replace_action("rows_action", ErrorRowsAction())
        self.actions.extend([
            self.save_action,
            self.upload_action,
            self.error_detail_win_action,
            self.report_action
        ])

    def declare_context(self, action):
        result = super(ErrorDetailPack, self).declare_context(action)

        if action is self.rows_action:
            result["feedback_statistic"] = {
                "type": "int_or_zero",
                "default": None
            }
        elif action in [self.upload_action, self.report_action]:
            result["feedback"] = {"type": int}
            result['feedback_statistic_id'] = {
                "type": "int_or_zero",
                "default": None
            }
        elif action is self.error_detail_win_action:
            result["detail_id"] = {"type": int}

        return result

    def configure_grid(self, grid):
        super(ErrorDetailPack, self).configure_grid(grid)

        # Добавляется здесь, потому, что нельзя указать сложную
        # колонку в атрибуте columns у пака.
        grid.add_check_column(
            header=u"Обработано", data_index='processed', flex=2,
            editor=ExtCheckBox())
        grid.sm = ExtGridRowSelModel()
        grid.sm.single_select = True

    def prepare_row(self, obj, request, context):
        obj = super(ErrorDetailPack, self).prepare_row(
            obj, request, context)

        if hasattr(context, "cache"):
            obj.record_name = context.cache.get(obj.record_id, "")

        return obj

    def _get_model(self, query):
        u"""Получение модели, записи которой, представлены в QuerySet."""

        # Достаем имя модели, ошибки по которой отображаются.
        # В гриде отображаются данные только по одной модели.
        try:
            first_record = query[:1].get()
        except self.model.DoesNotExist:
            return None

        try:
            model = project_models_class.get_model(
                first_record.feedback_statistic.model)
        except project_models_class.ModelNotFound:
            raise ApplicationLogicException(u"Невозможно отобразить записи.")

        return model

    def _get_filter(self, query):
        u"""Получение фильтра для записей которые, представлены в QuerySet."""
        try:
            first_record = query[:1].get()
        except self.model.DoesNotExist:
            return None

        try:
            filter_ = project_models_class.get_unit_filter(
                first_record.feedback_statistic.model)
        except project_models_class.SpecificNotFound:
            raise ApplicationLogicException(u"Невозможно отобразить записи.")

        return filter_

    def get_rows_query(self, request, context):
        query = super(ErrorDetailPack, self).get_rows_query(request, context)

        query = query.filter(
            feedback_statistic=context.feedback_statistic).order_by("id")

        model = self._get_model(query)

        filter_ = self._get_filter(query)
        get_current_unit = get_object("current_unit_function")
        if filter_ and model and get_current_unit:
            current_unit = get_current_unit(request)
            if current_unit and current_unit.id:
                q_filter = filter_(current_unit)
                allowed_records_ids = model.objects.filter(
                    q_filter
                ).values_list(
                    "id", flat=True
                )
                query = query.filter(record_id__in=allowed_records_ids)

        if model:
            primary_keys = query.values_list("record_id", flat=True)
            # Достаём записи.
            records = model.objects.filter(id__in=primary_keys)
            context.cache = {
                record.id: record.id for record in records
            }

        return query


class ErrorRowsAction(ObjectRowsAction):
    u"""Экшен подгрузки ошибок."""

    def prepare_object(self, obj):
        result_dict = super(ErrorRowsAction, self).prepare_object(obj)
        # Небольшой хак, связанный с тем, что эта колонка не описана в
        # атрибуте columns у пака.
        result_dict["processed"] = obj.processed
        return result_dict


class ErrorDetailWindowAction(BaseWindowAction):
    u"""Экшен показа окна просмотра выгрузки."""

    def create_window(self):
        self.win = DetailErrorWindow()

    def set_window_params(self):
        super(ErrorDetailWindowAction, self).set_window_params()

        try:
            detail_feedback = FeedBackDetails.objects.select_related(
                "feedback_statistic"
            ).get(
                id=self.context.detail_id)
        except FeedBackDetails.DoesNotExist:
            raise ApplicationLogicException(
                u"Запись с ID={0} не найдена. "
                u"Пожалуйста обновите грид.".format(self.context.detail_id))

        try:
            model = project_models_class.get_model(
                detail_feedback.feedback_statistic.model)
        except (project_models_class.ModelNotFound,
                project_models_class.SpecificNotFound):
            raise ApplicationLogicException(
                u"Отсутствует маппинг модели для тега '{0}'".format(
                    detail_feedback.feedback_statistic.model_verbose
                ))

        try:
            record = model.objects.get(pk=detail_feedback.record_id)
        except model.DoesNotExist:
            raise ApplicationLogicException(
                u"В модели '{0}' отсутствует запись с ID={1}".format(
                    detail_feedback.feedback_statistic.model_verbose,
                    detail_feedback.record_id
                ))

        self.win_params["model"] = (
            detail_feedback.feedback_statistic.model_verbose)
        self.win_params["record_id"] = str(detail_feedback.record_id)
        self.win_params["record_name"] = str(record)
        self.win_params["message"] = detail_feedback.message


class ErrorSaveAction(BaseAction):
    u"""Экшен сохранения отметки об обработки ошибки."""

    def run(self, request, context):

        try:
            feedback_detail = FeedBackDetails.objects.get(
                id=context.record_id)
        except FeedBackDetails.DoesNotExist:
            raise ApplicationLogicException(
                u"Ошибка выгрузки с ID={0} не найдена".format(
                    context.record_id))

        feedback_detail.processed = not feedback_detail.processed
        feedback_detail.save()

        return OperationResult()


class ErrorWindowUploadAction(BaseAction):
    u"""Экшен выгрузки ошибок в грид."""

    def run(self, request, context):
        update_feedback_details.apply_async((context.feedback,), kwargs={})
        return OperationResult()


class PrintDetailsReportAction(BaseAction):
    u"""Экшен печати отчета по ошибкам."""

    def run(self, request, context):

        try:
            feedback = FeedBack.objects.get(id=context.feedback)
        except FeedBack.DoesNotExist:
            raise ApplicationLogicException(
                u"Запись с ID={0} не найдена. "
                u"Пожалуйста обновите грид.".format(self.context.feedback)
            )
        feedback_statistic_id = context.feedback_statistic_id or None
        reporter = FeedbackReporter(
            provider_params={"feedback": feedback, 'feedback_statistic_id': feedback_statistic_id},
            builder_params={"title": "Отчёт об ошибках"})
        report_file_url = reporter.make_report()

        return OperationResult(
            code="function() {location.href='%s';}" % report_file_url)
