# coding: utf-8

from __future__ import absolute_import

import datetime

from django.db import models
from django.contrib.contenttypes.models import ContentType


class GetPrivilegeData(models.Model):
    risid = models.PositiveIntegerField(u'ID в РИС')
    person_type = models.SmallIntegerField(u'1 - школьник, 2 - заявление')
    exemption = models.PositiveIntegerField(
        u'ID льготы')
    start_date = models.DateField(
        u'Дата начала действия льготы', null=True, blank=True)
    expiration_date = models.DateField(
        u'Дата окончания действия льготы', null=True, blank=True)
    deleted = models.BooleanField(
        u'Признак удаления', default=False)
    deleted_date = models.DateField(
        u'Дата получения информации об удалении', null=True, blank=True)

    class Meta:
        verbose_name = u'Данные о привелегиях из Контингента'
        verbose_name_plural = u'Данные о привелегиях из Контингента'


class GetPrivilegeSession(models.Model):

    PROCESSED_CHOICES = (
        (True, u'Завершено'),
        (False, u'Не завершено')
    )

    timestamp = models.DateTimeField(
        default=datetime.datetime.now,
        verbose_name=u"Дата/время создания")
    session = models.CharField(
        unique=True,
        max_length=256,
        verbose_name=u"Сессия")
    processed = models.BooleanField(
        default=False,
        verbose_name=u"Обработано",
        choices=PROCESSED_CHOICES)
    message = models.TextField(
        blank=True,
        verbose_name=u"Сообщение")


class GetPrivilegeStatistic(models.Model):
    session = models.ForeignKey(
        GetPrivilegeSession,
        verbose_name=u"Сессия обмена данными",
        on_delete=models.CASCADE,
    )
    model = models.ForeignKey(
        ContentType,
        verbose_name=u"Модель",
        on_delete=models.CASCADE,
    )
    count = models.PositiveIntegerField(
        verbose_name=u"Количество")
