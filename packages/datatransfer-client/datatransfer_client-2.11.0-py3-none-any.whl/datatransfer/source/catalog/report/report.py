# -*- coding: utf-8 -*-
from __future__ import absolute_import

from educommon.report.reporter import SimpleReporter

from .builder import FeedBackReportBuilder
from .provider import FeedBackDetailProvider


class FeedbackReporter(SimpleReporter):
    u"""Репортер для отчета ошибок."""

    template_file_path = "../templates/report/report.xlsx"
    extension = '.xlsx'
    data_provider_class = FeedBackDetailProvider
    builder_class = FeedBackReportBuilder
