# coding: utf-8
import datetime

from django.db import models
from educommon.contingent.catalogs import TypeTrainingLongTermTreatment

from datatransfer.common.helpers import make_fullname
from datatransfer.source.get_data.models import GetDataRecordStatus
from datatransfer.source.get_data.models import GetDataSession


class EnrollGetDataDeclaration(models.Model):
    """Данные из Контингента для заявления на зачисление."""

    status = models.SmallIntegerField(
        choices=GetDataRecordStatus.get_choices(),
        verbose_name="Статус записи",
        default=GetDataRecordStatus.WAIT
    )
    session = models.ForeignKey(
        GetDataSession,
        verbose_name="Сессия обмена данными",
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(
        default=datetime.datetime.now,
        verbose_name="Дата/время создания/обновления"
    )

    regional_id = models.BigIntegerField(
        verbose_name="Региональный идентификатор"
    )
    source_id = models.BigIntegerField(
        verbose_name="Идентификатор источника данных РС"
    )
    external_id = models.BigIntegerField(
        verbose_name="Идентификатор записи в РИС"
    )
    federal_id = models.CharField(
        blank=True,
        null=True,
        max_length=4096,
        verbose_name="Федеральный идентификатор"
    )
    first_name = models.CharField(
        blank=True,
        null=True,
        max_length=4096,
        verbose_name="Имя"
    )
    middle_name = models.CharField(
        blank=True,
        null=True,
        max_length=4096,
        verbose_name="Отчество"
    )
    last_name = models.CharField(
        blank=True,
        null=True,
        max_length=4096,
        verbose_name="Фамилия"
    )
    gender = models.CharField(
        blank=True,
        null=True,
        max_length=15,
        verbose_name="Пол"
    )
    birth_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="Дата рождения"
    )
    snils = models.CharField(
        blank=True,
        null=True,
        max_length=4096,
        verbose_name="СНИЛС"
    )
    citizenship = models.CharField(
        blank=True,
        null=True,
        max_length=4096,
        verbose_name="Наличие гражданства"
    )
    registration_address_place = models.CharField(
        blank=True,
        null=True,
        max_length=4096,
        verbose_name="Населенный пункт"
    )
    registration_address_street = models.CharField(
        blank=True,
        null=True,
        max_length=4096,
        verbose_name="Улица"
    )
    registration_address_house = models.CharField(
        blank=True,
        null=True,
        max_length=4096,
        verbose_name="Дом"
    )
    registration_address_flat = models.CharField(
        blank=True,
        null=True,
        max_length=4096,
        verbose_name="Квартира"
    )
    registration_address = models.CharField(
        blank=True,
        null=True,
        max_length=4096,
        verbose_name="Адрес"
    )
    residence_address_place = models.CharField(
        blank=True,
        null=True,
        max_length=4096,
        verbose_name="Населенный пункт"
    )
    residence_address_street = models.CharField(
        blank=True,
        null=True,
        max_length=4096,
        verbose_name="Улица"
    )
    residence_address_house = models.CharField(
        blank=True,
        null=True,
        max_length=4096,
        verbose_name="Дом"
    )
    residence_address_flat = models.CharField(
        blank=True,
        null=True,
        max_length=4096,
        verbose_name="Квартира"
    )
    residence_address = models.CharField(
        blank=True,
        null=True,
        max_length=4096,
        verbose_name="Адрес"
    )
    actual_address_place = models.CharField(
        blank=True,
        null=True,
        max_length=4096,
        verbose_name="Населенный пункт"
    )
    actual_address_street = models.CharField(
        blank=True,
        null=True,
        max_length=4096,
        verbose_name="Улица"
    )
    actual_address_house = models.CharField(
        blank=True,
        null=True,
        max_length=4096,
        verbose_name="Дом"
    )
    actual_address_flat = models.CharField(
        blank=True,
        null=True,
        max_length=4096,
        verbose_name="Квартира"
    )
    actual_address = models.CharField(
        blank=True,
        null=True,
        max_length=4096,
        verbose_name="Адрес"
    )
    health_group = models.CharField(
        blank=True,
        null=True,
        max_length=4096,
        verbose_name="Группа здоровья"
    )
    disability_group = models.CharField(
        blank=True,
        null=True,
        max_length=4096,
        verbose_name="Группа инвалидности"
    )
    disability_expiration_date = models.DateField(
        null=True,
        verbose_name="Срок действия группы инвалидности"
    )
    disability_reason = models.CharField(
        blank=True,
        null=True,
        max_length=4096,
        verbose_name="Причина инвалидности"
    )
    adaptation_program = models.CharField(
        blank=True,
        null=True,
        max_length=4096,
        verbose_name="Потребность в адаптированной программе обучения"
    )
    training_type_in_cure = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        choices=TypeTrainingLongTermTreatment.get_choices(),
        verbose_name='Вид обучения при длительном лечении'
    )

    class Meta:
        verbose_name = "Персона из Контингента"
        verbose_name_plural = "Персоны из Контингента"

    @property
    def pupil_fullname(self):
        """Возвращает ФИО."""
        return make_fullname(
            self.last_name,
            self.first_name,
            self.middle_name,
        )


class EnrollGetDataDeclarationDocument(models.Model):

    """Информация о ДУЛ."""

    get_data_external_id = models.BigIntegerField(
        verbose_name="Персона из КО",
    )
    regional_id = models.BigIntegerField(
        verbose_name="Региональный идентификатор")
    source_id = models.BigIntegerField(
        verbose_name="Идентификатор источника данных РС")
    external_id = models.BigIntegerField(
        verbose_name="Идентификатор записи в РИС")
    session = models.ForeignKey(
        GetDataSession,
        verbose_name="Сессия обмена данными",
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(
        default=datetime.datetime.now,
        verbose_name="Дата/время создания/обновления")
    type = models.CharField(
        blank=True,
        null=True,
        max_length=4096,
        verbose_name="Тип")
    series = models.CharField(
        blank=True,
        null=True,
        max_length=4096,
        verbose_name="Серия")
    number = models.CharField(
        blank=True,
        null=True,
        max_length=4096,
        verbose_name="Номер")
    issuer = models.CharField(
        blank=True,
        null=True,
        max_length=4096,
        verbose_name="Кем выдан")
    issue_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="Дата выдачи")
    status = models.SmallIntegerField(
        choices=GetDataRecordStatus.get_choices(),
        verbose_name="Статус записи",
        default=GetDataRecordStatus.WAIT)

    class Meta:
        verbose_name = "Документ удостоверяющий личность"
        verbose_name_plural = "Документы удостоверяющие личность"


class AbstractEnrollGetDataEducation(models.Model):
    """Данные об образовании."""

    regional_id = models.BigIntegerField(
        verbose_name="Региональный идентификатор"
    )
    person_contingent_id = models.BigIntegerField(
        verbose_name="Идентификатор записи в КО."
    )
    get_data_external_id = models.BigIntegerField(
        verbose_name="Персона из КО",
    )
    name = models.CharField(
        verbose_name='Название образовательной организации',
        max_length=500,
    )
    enroll_date = models.DateField(verbose_name="Дата зачисления")
    session = models.ForeignKey(
        GetDataSession,
        verbose_name="Сессия обмена данными",
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(
        default=datetime.datetime.now,
        verbose_name="Дата/время создания/обновления"
    )
    status = models.SmallIntegerField(
        choices=GetDataRecordStatus.get_choices(),
        verbose_name="Статус записи",
        default=GetDataRecordStatus.WAIT
    )

    class Meta:
        abstract = True


class EnrollGetDataPreschoolEducation(AbstractEnrollGetDataEducation):
    """Данные о дошкольном образовании."""


class EnrollGetDataMainEducation(AbstractEnrollGetDataEducation):
    """Данные о среднем образовании."""


class EnrollGetDataMiddleEducation(AbstractEnrollGetDataEducation):
    """Данные о среднеспециальном образовании."""
