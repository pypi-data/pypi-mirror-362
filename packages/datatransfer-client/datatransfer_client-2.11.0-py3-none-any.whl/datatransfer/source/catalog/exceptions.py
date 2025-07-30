# -*- coding: utf-8 -*-


class NotClearDetails(Exception):
    u"""Исключение возникающее если детали выгрузки не удалены."""

    def __init__(self, feedback):
        self.message = u"У выгрузки с ID={0} не очищена история".format(
            feedback
        )
