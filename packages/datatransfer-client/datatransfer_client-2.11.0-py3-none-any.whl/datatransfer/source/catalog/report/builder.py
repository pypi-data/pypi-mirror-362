# -*- coding: utf-8 -*-

from __future__ import absolute_import

from educommon.report import AbstractReportBuilder


bool_to_word = {
    True: u"Да",
    False: u"Нет"
}


class FeedBackReportBuilder(AbstractReportBuilder):
    u"""Билдер."""

    def __init__(self, provider, adapter, report, params):
        self.provider = provider
        self.report = report

    def build(self):

        header_section = self.report.get_section("header")
        data_section = self.report.get_section("row")

        header_section.flush({
            "session_id": self.provider.session,
            "date_time": self.provider.date_time
        })

        for num, row in enumerate(self.provider.details, start=1):
            data_section.flush({
                "num": num,
                "model": row["feedback_statistic__model_verbose"],
                "record_id": row["record_id"],
                "message": row["message"],
                "processed": bool_to_word[row["processed"]]
            })
