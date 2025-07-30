# coding: utf-8
from datetime import (
    date,
    timedelta,
)
import json

from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django.utils import datetime_safe

from datatransfer.source.get_data.models import (
    GetDataPerson,
    GetDataSession,
)
from test_project.system.models import Person
from test_project.system.utils import get_current_user


def date2str(date):
    return datetime_safe.new_datetime(date).strftime('%d.%m.%Y')


class FromRSTestCase(TestCase):

    u"""Тесты получения данных из РС КО и их обработки."""

    def setUp(self):
        # Создаём ученика
        person = Person.objects.create(**self._person_values)
        self._person_id = person.id

        # Создаём запись в дататрансфере для ученика
        data = GetDataPerson.objects.create(
            local_id=person.id,
            regional_id=person.id,
            external_id=person.id,
            model_id=ContentType.objects.get_for_model(Person).id,
            source_id=1,
            session_id=GetDataSession.objects.create(session='1').id,
            **self._data_values
        )
        self.data_id = data.id

    def test_view(self):
        u"""Проверяет отображаемые значения списка изменений.

        Тестирует публичные свойства: diff, old, new.
        """
        change = self._get_change()

        result_diff = {tuple(row) for row in change.diff}
        self.assertEquals(result_diff, self._view_diff)

        self.assertEquals(set(change.new), self._view_new)
        self.assertEquals(set(change.old), self._view_old)

    def test_change_type(self):
        u"""Проверяет типы изменений.

        Типы: новые данные, измененные существующие данные, смешанный.
        """
        from datatransfer.source.get_data.changes.constants import CHANGE_DIFF
        from datatransfer.source.get_data.changes.constants import CHANGE_MIXED
        from datatransfer.source.get_data.changes.constants import CHANGE_NEW
        from datatransfer.source.get_data.models import GetDataPerson

        # По умолчанию у нас нет новых данных.
        self.assertEquals(self._get_change().change_type, CHANGE_DIFF)

        # Добавляем новое - изменения смешанные.
        data = GetDataPerson.objects.get(id=self.data_id)
        data.snils = '929-282-657 53'
        data.save()
        change = self._get_change()
        self.assertEquals(change.change_type, CHANGE_MIXED)

        # Оставляем изменение только с новым полем.
        data = GetDataPerson.objects.get(id=self.data_id)
        for k, v in self._person_values.items():
            setattr(data, k, v)

        data.last_name = self._person_values['last_name']
        data.first_name = self._person_values['first_name']
        data.middle_name = self._person_values['middle_name']
        data.gender = 'Male'
        data.birth_date = self._person_values['date_of_birth']
        data.save()

        change = self._get_change()
        self.assertEquals(change.change_type, CHANGE_NEW)

    def test_apply(self):
        u"""Тест массового применения изменений."""
        from datatransfer.source.get_data.models import GetDataChanges
        from datatransfer.source.get_data.models import GetDataPerson
        from datatransfer.source.get_data.models import GetDataRecordStatus
        from datatransfer.source.get_data.actions import extensions

        # Применяем изменение.
        data = GetDataPerson.objects.get(id=self.data_id)
        person = data.person
        user = get_current_user()
        extensions.get_change(data, person).apply(user)

        # Загружаем изменение заново.
        change = self._get_change()

        self.assertEquals(
            len(change.diff), 0, 'Some changes have not been applied.'
        )

        expected_diff = self._raw_diff

        # Проверяем корректность применения изменения
        new_person = Person.objects.get(id=person.id)
        person_values = self._person_values
        person_fields = set(person_values.keys())
        for field in person_fields:
            value = getattr(new_person, field)
            if field == 'date_of_birth':
                value = date2str(value)
            self.assertEquals(
                value, expected_diff[field][1]
            )

        # Проверяем информацию о применении изменения.
        applied_change = GetDataChanges.objects.get(
            local_id=person.id,
            session_id=data.session_id,
        )
        change_data = json.JSONDecoder().decode(applied_change.data)[0]
        self.assertEquals(change_data['id'], person.id)
        self.assertEquals(
            change_data['model_id'],
            ContentType.objects.get_for_model(person).id
        )
        diff_dict = {key: (old, new) for key, old, new in change_data['diff']}

        for field in person_fields:
            self.assertIn(field, diff_dict)
            self.assertEquals(expected_diff[field], diff_dict[field])

        self.assertEquals(
            set(diff_dict.items()), set(expected_diff.items())
        )

        self.assertEquals(applied_change.user, user)
        self.assertEquals(applied_change.status, GetDataRecordStatus.ACCEPT)

    def test_virtual_model(self):
        u"""Проверяет виртуальную модель контингента."""
        from datatransfer.source.get_data.changes.models import (
            ChangesVirtualModel
        )
        from datatransfer.source.get_data.models import GetDataChanges
        from datatransfer.source.get_data.models import GetDataPerson

        query = ChangesVirtualModel.objects.configure(
            person_id=self._person_id
        )
        self.assertEquals(query.count(), 1)
        obj = query.get()
        data = GetDataPerson.objects.get(id=self.data_id)

        # Непримененное изменение
        self.assertLessEqual(
            obj.timestamp - data.session.timestamp, timedelta(seconds=1)
        )
        self.assertIs(obj.applied, None)
        self.assertEquals(obj.user, u'РС Контингент обучающихся')
        self.assertEquals(set(obj.old), self._view_old)
        self.assertEquals(set(obj.new), self._view_new)
        self.assertEquals(obj.status, u'Ожидает решения')
        self.assertEquals(obj.comment, u'изменение данных')

        only_fields = ('last_name', 'first_name')
        change = self._get_change()
        user = get_current_user()
        change.apply(user=user, only_fields=only_fields)

        self.assertEquals(query.count(), 2)

        # Изменение, оставшееся непримененным
        obj = query.get(user=u'РС Контингент обучающихся')

        def without_only(_set):
            data = dict(_set)
            for k in (u'Имя', u'Фамилия'):
                data.pop(k)
            return set(data.items())

        self.assertLessEqual(
            obj.timestamp - data.session.timestamp, timedelta(seconds=1)
        )
        self.assertIs(obj.applied, None)
        self.assertEquals(obj.user, u'РС Контингент обучающихся')
        self.assertEquals(set(obj.old), without_only(self._view_old))
        self.assertEquals(set(obj.new), without_only(self._view_new))
        self.assertEquals(obj.status, u'Ожидает решения')
        self.assertEquals(obj.comment, u'изменение данных')

        # Примененное изменение
        obj = query.exclude(user=u'РС Контингент обучающихся')[0]

        def only(_set):
            result = (row for row in _set if row[0] in (u'Имя', u'Фамилия'))
            return set(result)

        change = GetDataChanges.objects.get()

        self.assertLessEqual(
            obj.timestamp - data.session.timestamp, timedelta(seconds=1)
        )
        self.assertLessEqual(
            obj.applied - change.applied, timedelta(seconds=1)
        )
        self.assertEquals(obj.user, user)
        self.assertEquals(set(obj.old), only(self._view_old))
        self.assertEquals(set(obj.new), only(self._view_new))
        self.assertEquals(obj.status, u'Принято')
        self.assertEquals(obj.comment, u'изменение данных')

    def _get_change(self):
        from datatransfer.source.get_data.models import GetDataPerson
        from datatransfer.source.get_data.actions import extensions

        data = GetDataPerson.objects.get(id=self.data_id)
        person = data.person
        return extensions.get_change(data, person)

    @property
    def _view_diff(self):
        u"""Возвращает diff с отображаемыми значениями."""
        return {
            ('last_name', u'Фамилия', u'Тестов', u'Контингентов'),
            ('first_name', u'Имя', u'Тест', u'Контингент'),
            ('middle_name', u'Отчество', u'Тестович', u'Контингентович'),
            ('date_of_birth', u'Дата рождения', u'03.03.1980', u'03.03.1990'),
            ('gender', u'Пол', u'Мужской', u'Женский')
        }

    @property
    def _view_new(self):
        return {(k, v) for _, k, _, v in self._view_diff}

    @property
    def _view_old(self):
        return {(k, v) for _, k, v, _ in self._view_diff}

    @property
    def _raw_diff(self):
        u"""Возвращает diff с "сырыми" данными"."""
        return dict(
            last_name=(u'Тестов', u'Контингентов'),
            first_name=(u'Тест', u'Контингент'),
            middle_name=(u'Тестович', u'Контингентович'),
            date_of_birth=(
                date2str(date(1980, 3, 3)), date2str(date(1990, 3, 3))
            ),
            gender=(Person.GENDER.MALE, Person.GENDER.FEMALE)
        )

    @property
    def _person_values(self):
        u"""Значения для физ. лица в ЭДО."""
        return dict(
            last_name=u'Тестов',
            first_name=u'Тест',
            middle_name=u'Тестович',
            date_of_birth=date(1980, 3, 3),
            gender=Person.GENDER.MALE,
        )

    @property
    def _data_values(self):
        u"""Значения для физ. лица в Datatransfer."""
        return dict(
            last_name=u'Контингентов',
            first_name=u'Контингент',
            middle_name=u'Контингентович',
            birth_date=date(1990, 3, 3),
            gender='Female',
        )
