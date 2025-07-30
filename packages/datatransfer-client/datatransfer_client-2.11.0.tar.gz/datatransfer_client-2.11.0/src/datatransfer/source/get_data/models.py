# coding: utf-8

from __future__ import absolute_import

import datetime

from django.contrib.contenttypes.models import ContentType
from django.db import models
from m3.db import BaseEnumerate
from m3_django_compat.models import GenericForeignKey


class GetDataRecordStatus(BaseEnumerate):
    WAIT = 0
    REJECT = 1
    ACCEPT = 2

    values = {
        WAIT: u"Ожидает решения",
        REJECT: u"Отказано",
        ACCEPT: u"Принято"}


class GetDataSession(models.Model):

    """Информация о сессии обмена данными."""

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

    class Meta:
        verbose_name = u"Сессия обмена данными"
        verbose_name_plural = u"Сессии обмена данными"


class GetDataStatistic(models.Model):

    """Информация о статистике сессии обмена данными."""

    session = models.ForeignKey(
        GetDataSession,
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

    class Meta:
        verbose_name = u"Статистика сессии обмена данными"
        verbose_name_plural = u"Статистика сессий обмена данными"


class GetDataPerson(models.Model):

    """Информация о персоне."""

    model = models.ForeignKey(
        ContentType,
        verbose_name=u"Модель",
        on_delete=models.CASCADE,
    )
    local_id = models.PositiveIntegerField(
        verbose_name=u"Локальный идентификатор")
    person = GenericForeignKey(
        'model', 'local_id')
    regional_id = models.BigIntegerField(
        verbose_name=u"Региональный идентификатор")
    source_id = models.BigIntegerField(
        verbose_name=u"Идентификатор источника данных РС")
    external_id = models.BigIntegerField(
        verbose_name=u"Идентификатор записи в РИС")
    federal_id = models.CharField(
        blank=True,
        null=True,
        max_length=4096,
        verbose_name=u"Федеральный идентификатор")
    session = models.ForeignKey(
        GetDataSession,
        verbose_name=u"Сессия обмена данными",
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(
        default=datetime.datetime.now,
        verbose_name=u"Дата/время создания/обновления")
    first_name = models.CharField(
        blank=True,
        null=True,
        max_length=4096,
        verbose_name=u"Имя")
    middle_name = models.CharField(
        blank=True,
        null=True,
        max_length=4096,
        verbose_name=u"Отчество")
    last_name = models.CharField(
        blank=True,
        null=True,
        max_length=4096,
        verbose_name=u"Фамилия")
    gender = models.CharField(
        blank=True,
        null=True,
        max_length=4096,
        verbose_name=u"Пол")
    birth_date = models.DateField(
        blank=True,
        null=True,
        verbose_name=u"Дата рождения")
    birth_place = models.CharField(
        blank=True,
        null=True,
        max_length=4096,
        verbose_name=u"Место рождения")
    snils = models.CharField(
        blank=True,
        null=True,
        max_length=4096,
        verbose_name=u"СНИЛС")
    health_group = models.CharField(
        blank=True,
        null=True,
        max_length=4096,
        verbose_name=u"Группа здоровья")
    long_term_treatment = models.CharField(
        blank=True,
        null=True,
        max_length=4096,
        verbose_name=u"Наличие потребности в длительном лечении")
    disability_group = models.CharField(
        blank=True,
        null=True,
        max_length=4096,
        verbose_name=u"Группа инвалидности")
    disability_expiration_date = models.DateField(
        null=True,
        verbose_name=u"Срок действия группы инвалидности")
    disability_reason = models.CharField(
        blank=True,
        null=True,
        max_length=4096,
        verbose_name=u"Причина инвалидности")
    adaptation_program = models.CharField(
        blank=True,
        null=True,
        max_length=4096,
        verbose_name=u"Наличие потребности в адаптированной программе обучения"
    )
    physical_culture_group = models.CharField(
        blank=True,
        null=True,
        max_length=4096,
        verbose_name=u"Медицинская группа для занятия физической культурой")
    difficult_situation = models.CharField(
        blank=True,
        null=True,
        max_length=4096,
        verbose_name=u"Трудная жизненная ситуация")
    document_registry_number = models.CharField(
        blank=True,
        null=True,
        max_length=4096,
        verbose_name=u"Номер актовой записи о рождении")
    document_registry_issuer = models.CharField(
        blank=True,
        null=True,
        max_length=4096,
        verbose_name=u"Наименование органа, составившего запись акта")
    document_registry_issue_date = models.DateField(
        blank=True,
        null=True,
        verbose_name=u"Дата актовой записи о рождении")
    citizenship = models.CharField(
        blank=True,
        null=True,
        max_length=4096,
        verbose_name=u"Наличие гражданства")
    registration_address_place = models.CharField(
        blank=True,
        null=True,
        max_length=4096,
        verbose_name=u"Населенный пункт")
    registration_address_street = models.CharField(
        blank=True,
        null=True,
        max_length=4096,
        verbose_name=u"Улица")
    registration_address_house = models.CharField(
        blank=True,
        null=True,
        max_length=4096,
        verbose_name=u"Дом")
    registration_address_flat = models.CharField(
        blank=True,
        null=True,
        max_length=4096,
        verbose_name=u"Квартира")
    registration_address = models.CharField(
        blank=True,
        null=True,
        max_length=4096,
        verbose_name=u"Адрес")
    residence_address_place = models.CharField(
        blank=True,
        null=True,
        max_length=4096,
        verbose_name=u"Населенный пункт")
    residence_address_street = models.CharField(
        blank=True,
        null=True,
        max_length=4096,
        verbose_name=u"Улица")
    residence_address_house = models.CharField(
        blank=True,
        null=True,
        max_length=4096,
        verbose_name=u"Дом")
    residence_address_flat = models.CharField(
        blank=True,
        null=True,
        max_length=4096,
        verbose_name=u"Квартира")
    residence_address = models.CharField(
        blank=True,
        null=True,
        max_length=4096,
        verbose_name=u"Адрес")
    actual_address_place = models.CharField(
        blank=True,
        null=True,
        max_length=4096,
        verbose_name=u"Населенный пункт")
    actual_address_street = models.CharField(
        blank=True,
        null=True,
        max_length=4096,
        verbose_name=u"Улица")
    actual_address_house = models.CharField(
        blank=True,
        null=True,
        max_length=4096,
        verbose_name=u"Дом")
    actual_address_flat = models.CharField(
        blank=True,
        null=True,
        max_length=4096,
        verbose_name=u"Квартира")
    actual_address = models.CharField(
        blank=True,
        null=True,
        max_length=4096,
        verbose_name=u"Адрес")
    status = models.SmallIntegerField(
        choices=GetDataRecordStatus.get_choices(),
        verbose_name=u"Статус записи",
        default=GetDataRecordStatus.WAIT)

    class Meta:
        verbose_name = u"Персона"
        verbose_name_plural = u"Персоны"


class GetDataPersonDocument(models.Model):

    """Информация о ДУЛ."""

    model = models.ForeignKey(
        ContentType,
        verbose_name=u"Модель",
        on_delete=models.CASCADE,
    )
    local_id = models.PositiveIntegerField(
        null=True,
        verbose_name=u"Локальный идентификатор")
    document = GenericForeignKey(
        'model', 'local_id')
    person = models.ForeignKey(
        GetDataPerson,
        verbose_name=u"Персона",
        on_delete=models.CASCADE,
    )
    regional_id = models.BigIntegerField(
        verbose_name=u"Региональный идентификатор")
    source_id = models.BigIntegerField(
        verbose_name=u"Идентификатор источника данных РС")
    external_id = models.BigIntegerField(
        verbose_name=u"Идентификатор записи в РИС")
    session = models.ForeignKey(
        GetDataSession,
        verbose_name=u"Сессия обмена данными",
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(
        default=datetime.datetime.now,
        verbose_name=u"Дата/время создания/обновления")
    type = models.CharField(
        blank=True,
        null=True,
        max_length=4096,
        verbose_name=u"Тип")
    series = models.CharField(
        blank=True,
        null=True,
        max_length=4096,
        verbose_name=u"Серия")
    number = models.CharField(
        blank=True,
        null=True,
        max_length=4096,
        verbose_name=u"Номер")
    issuer = models.CharField(
        blank=True,
        null=True,
        max_length=4096,
        verbose_name=u"Кем выдан")
    issue_date = models.DateField(
        blank=True,
        null=True,
        verbose_name=u"Дата выдачи")
    status = models.SmallIntegerField(
        choices=GetDataRecordStatus.get_choices(),
        verbose_name=u"Статус записи",
        default=GetDataRecordStatus.WAIT)

    class Meta:
        verbose_name = u"Документ удостоверяющий личность"
        verbose_name_plural = u"Документы удостоверяющие личность"


class GetDataChanges(models.Model):

    """Примененные изменения."""

    session = models.ForeignKey(
        GetDataSession,
        verbose_name=u"Сессия обмена данными",
        on_delete=models.CASCADE,
    )
    model = models.ForeignKey(
        ContentType,
        related_name='getdatachangesmodel',
        verbose_name=u"Модель",
        on_delete=models.CASCADE,
    )
    local_id = models.PositiveIntegerField(
        null=True,
        verbose_name=u"Локальный идентификатор")
    record = GenericForeignKey(
        'model', 'local_id')
    applied = models.DateTimeField(
        default=datetime.datetime.now,
        verbose_name=u"Дата/время применения")
    user_model = models.ForeignKey(
        ContentType,
        related_name='getdatachangesusermodel',
        verbose_name=u"Модель пользователя",
        on_delete=models.CASCADE,
    )
    user_id = models.PositiveIntegerField(
        null=True,
        verbose_name=u"Идентификатор пользователя")
    user = GenericForeignKey(
        'user_model', 'user_id')
    data = models.TextField(
        blank=False,
        max_length=4096,
        verbose_name=u"Данные")
    status = models.SmallIntegerField(
        choices=GetDataRecordStatus.get_choices(),
        verbose_name=u"Статус записи",
        default=GetDataRecordStatus.REJECT)

    class Meta:
        verbose_name = u"Примененные изменения"
        verbose_name_plural = u"Примененные изменения"
