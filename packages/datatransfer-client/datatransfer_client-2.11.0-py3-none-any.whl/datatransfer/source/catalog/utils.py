# -*- coding: utf-8 -*-

from __future__ import absolute_import

import datetime

from dateutil import relativedelta
from lxml import etree
from petl.io.sources import ZipSource

from datatransfer.source import configs

from .exceptions import NotClearDetails
from .models import FeedBack
from .models import FeedBackDetails


def load_feedback_details(feedback):
    u"""Выгрузка деталей feedback."""

    feedback_id = feedback
    if isinstance(feedback, FeedBack):
        feedback_id = feedback.id
    else:
        feedback = FeedBack.objects.get(id=feedback_id)

    if FeedBackDetails.objects.filter(
            feedback_statistic__feedback=feedback_id).exists():
        raise NotClearDetails(feedback_id)

    tag_to_statistic_bind = {}
    for feedback_statistic in feedback.feedbackstatistic_set.all():
        tag_to_statistic_bind[
            feedback_statistic.model] = feedback_statistic.id

    with ZipSource(feedback.archive, feedback.xml).open('r') as _xml:
        for event, element in etree.iterparse(_xml, tag='Data'):
            for model in element:
                feedback_statistic_id = tag_to_statistic_bind.get(
                    model.tag, None)
                if feedback_statistic_id:
                    for record in model:
                        try:
                            record_id = int(record.xpath("ID")[0].text)
                        except (IndexError, ValueError, TypeError):
                            record_id = 0

                        try:
                            message = record.xpath("Message")[0].text
                        except (IndexError,):
                            message = u"Сообщение отсутствует"

                        FeedBackDetails(
                            feedback_statistic_id=feedback_statistic_id,
                            record_id=record_id,
                            message=message
                        ).save()

            element.clear()

    feedback.last_update_date = datetime.date.today()
    feedback.save()


def get_delete_details_date_border():
    u"""Функция возвращает дату раньше, которой можно удалять все записи."""

    return (
        datetime.datetime.now() - relativedelta.relativedelta(
            days=configs.CLEAR_FEEDBACK_DETAILS_DAYS)).date()
