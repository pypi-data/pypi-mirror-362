# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django.db import models
from m3.db import BaseEnumerate


class ResultTypes(BaseEnumerate):
    u"""Виды результатов."""

    SUCCESS = 1
    WITH_ERRORS = 2
    FAILURE = 3

    values = {
        SUCCESS: u"Успешно",
        WITH_ERRORS: u"Есть ошибки",
        FAILURE: u"Ошибка"
    }


class FeedBack(models.Model):
    u"""Результат взаимодействия."""

    session = models.CharField(
        max_length=50, verbose_name=u"Сессия")
    date_time = models.DateTimeField(verbose_name=u"Дата и время")
    result = models.PositiveSmallIntegerField(
        choices=ResultTypes.get_choices(),
        verbose_name=u"Результат")
    comment = models.TextField(
        null=True, blank=True, verbose_name=u"Комментарий")
    xml = models.CharField(max_length=200, verbose_name=u"XML")
    archive = models.CharField(max_length=4096, verbose_name=u"Архив")
    last_update_date = models.DateField(
        verbose_name=u"Дата последнего обновления")

    class Meta:
        verbose_name = u"Результат взаимодействия"
        verbose_name_plural = u"Результаты взаимодействия"


class FeedBackStatistic(models.Model):
    u"""Статистическая выкладка по выгрузке."""

    feedback = models.ForeignKey(
        FeedBack,
        verbose_name=u"Результат выгрузки",
        on_delete=models.CASCADE,
    )
    # Совпадает с тегом в xml
    model = models.CharField(max_length=100, verbose_name=u"Модель")
    # Совпадает с атрибутом description
    model_verbose = models.CharField(
        max_length=100, verbose_name=u"Наименование модели")
    total = models.IntegerField(verbose_name=u"Всего")
    invalid = models.IntegerField(verbose_name=u"Некорректных")
    processed = models.IntegerField(verbose_name=u"Обработано")
    created = models.IntegerField(verbose_name=u"Создано")
    updated = models.IntegerField(verbose_name=u"Обновлено")

    class Meta:
        verbose_name = u"Статистическая выкладка по выгрузке"
        verbose_name_plural = u"Статистические выкладки по выгрузке"


class FeedBackDetails(models.Model):
    u"""Детализация выгрузки"""

    feedback_statistic = models.ForeignKey(
        FeedBackStatistic,
        verbose_name=u"Статистическая выкладка",
        on_delete=models.CASCADE,
    )
    record_id = models.PositiveIntegerField(verbose_name=u"ID записи")
    message = models.TextField(verbose_name=u"Сообщение")
    processed = models.BooleanField(default=False, verbose_name=u"Обработано")

    class Meta:
        verbose_name = u"Детализация ошибки выгрузки"
        verbose_name_plural = u"Детализация ошибок выгрузки"
