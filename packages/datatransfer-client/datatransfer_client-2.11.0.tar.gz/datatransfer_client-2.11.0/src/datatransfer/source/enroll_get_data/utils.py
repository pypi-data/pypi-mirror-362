# coding: utf-8
from django.apps import apps


def get_all_level_education_info(obj_external_id):
    """Возвращает данные об образовании из Контингента.

    :param obj_external_id: Идентификатор записи.
    :return: Информация об образовании по уровням.
    """
    EnrollGetDataPreschoolEducation = apps.get_model(
        'enroll_get_data.EnrollGetDataPreschoolEducation'
    )
    EnrollGetDataMainEducation = apps.get_model(
        'enroll_get_data.EnrollGetDataMainEducation'
    )
    EnrollGetDataMiddleEducation = apps.get_model(
        'enroll_get_data.EnrollGetDataMiddleEducation'
    )
    return dict(
        preschool=EnrollGetDataPreschoolEducation.objects.filter(
            get_data_external_id=obj_external_id
        ).first(),
        main=EnrollGetDataMainEducation.objects.filter(
            get_data_external_id=obj_external_id,
        ).first(),
        middle=EnrollGetDataMiddleEducation.objects.filter(
            get_data_external_id=obj_external_id
        ).first()
    )


def get_education_info(obj_external_id):
    """Формирует данные об образовательной организации.

    Приоритет выбора значений(EDUADNL-3932):
        1. Дошкольное образование.
        2. Среднее образование.
        3. Среднеспециальное образование.
    :param obj_external_id: Идентификатор записи в Контингент.
    :return: Информация об образовательной организации.
    """
    education_info_map = (
        ("Дошкольное образование", "preschool"),
        ("Общее образование", "main"),
        ("Профессиональное образование", "middle"),
    )
    result = None, None
    edu_data = get_all_level_education_info(obj_external_id)
    for description, edu_level in education_info_map:
        edu_info = edu_data.get(edu_level)
        if edu_info:
            result = description, edu_info.name
            break

    return result
