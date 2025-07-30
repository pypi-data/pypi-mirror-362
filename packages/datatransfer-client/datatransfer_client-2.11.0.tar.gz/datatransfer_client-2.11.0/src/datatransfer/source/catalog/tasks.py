# -*- coding: utf-8 -*-
from __future__ import absolute_import

import datetime

from celery.result import states
from lxml import etree
from petl.io.sources import ZipSource

from datatransfer.common.helpers import get_error
from datatransfer.common.utils import register_task
from datatransfer.source import configs
from datatransfer.source.common.tasks import AsyncTask

from .models import FeedBack
from .models import FeedBackDetails
from .models import FeedBackStatistic
from .models import ResultTypes
from .utils import get_delete_details_date_border
from .utils import load_feedback_details


def parse_bool(v):
    return v == "true"


class SaveFeedbackResult(AsyncTask):

    u"""Парсинг и сохранение результатов запроса."""

    description = u"Выгрузка данных"
    stop_executing = False
    routing_key = configs.CELERY_ROUTING_KEY

    def run(self, xml_filename, archive_filename,
            session, date_time, *args, **kwargs):
        super(SaveFeedbackResult, self).run(*args, **kwargs)

        success = False
        error_msg = None
        have_warnings = False
        statistics = []
        with ZipSource(archive_filename, xml_filename).open('r') as _xml:
            for event, element in etree.iterparse(_xml):
                if element.tag == "Success":
                    success = parse_bool(element.text)
                    element.clear()
                if element.tag == "ErrorMessage":
                    error_msg = element.text
                    element.clear()
                if element.tag == "Data":
                    have_warnings = bool(element.getchildren())
                    element.clear()
                if element.tag == "Statistics":
                    for model in element:
                        record = {
                            "model": model.tag,
                            "model_verbose": model.get("description")
                        }

                        for statistic_tag in model:
                            record[statistic_tag.tag.lower()] = int(
                                statistic_tag.text)

                        statistics.append(record)
                    element.clear()

        result_type = ResultTypes.SUCCESS
        if have_warnings:
            result_type = ResultTypes.WITH_ERRORS
        elif not success:
            result_type = ResultTypes.FAILURE

        feedback = FeedBack(
            session=session, date_time=date_time,
            comment=error_msg, result=result_type,
            xml=xml_filename, archive=archive_filename,
            last_update_date=datetime.date.today())
        feedback.save()

        for statistic in statistics:
            feedback_statistic = FeedBackStatistic(
                feedback=feedback, **statistic)
            feedback_statistic.save()

        load_feedback_details(feedback)
        return self.state

    def on_failure(self, exc, task_id, args, kwargs, einfo):

        msg = get_error(exc)
        self.set_progress(msg, task_state=states.FAILURE)


save_feedback_result = register_task(SaveFeedbackResult())


class ClearDetailsTask(AsyncTask):

    u"""Таск очищающий БД от старых записей с ошибками."""

    description = u"Очистка данных."
    stop_executing = False
    routing_key = configs.CELERY_ROUTING_KEY

    def run(self, *args, **kwargs):
        super(ClearDetailsTask, self).run(*args, **kwargs)
        border_date = get_delete_details_date_border()
        FeedBackDetails.objects.filter(
            feedback_statistic__feedback__last_update_date__lte=border_date
        ).delete()
        return self.state


clear_details_task = register_task(ClearDetailsTask())


class UpdateFeedBackDetails(AsyncTask):
    u"""Таск обновляющий детали feedback."""

    description = u"Обновление данных"
    stop_executing = False
    routing_key = configs.CELERY_ROUTING_KEY

    def run(self, feedback_id, *args, **kwargs):
        super(UpdateFeedBackDetails, self).run(*args, **kwargs)
        load_feedback_details(feedback_id)
        return self.state

    def on_failure(self, exc, task_id, args, kwargs, einfo):

        msg = get_error(exc)
        self.set_progress(msg, task_state=states.FAILURE)


update_feedback_details = register_task(UpdateFeedBackDetails())
