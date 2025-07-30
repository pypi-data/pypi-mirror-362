# -*- coding: utf-8 -*-

from __future__ import absolute_import

from django.db.models import Q
from django.utils.functional import cached_property
from educommon.report import AbstractDataProvider

from ..models import FeedBackDetails


class FeedBackDetailProvider(AbstractDataProvider):
    u"""Провайдер данных для ошибок в отчете."""

    def init(self, feedback, feedback_statistic_id):

        self._feedback = feedback
        self._feedback_statistic_id = feedback_statistic_id

    @cached_property
    def details(self):
        filter_statistic = Q(feedback_statistic=self._feedback_statistic_id) if self._feedback_statistic_id else Q()
        for detail in FeedBackDetails.objects.filter(
                filter_statistic, feedback_statistic__feedback_id=self._feedback,
        ).values(
            "feedback_statistic__model_verbose",
            "record_id",
            "message",
            "processed"
        ):
            yield detail

    @property
    def session(self):
        return self._feedback.session

    @property
    def date_time(self):
        return self._feedback.date_time
