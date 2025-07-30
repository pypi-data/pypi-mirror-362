# coding: utf-8
from __future__ import absolute_import

from django.contrib.contenttypes.models import ContentType
from six.moves import zip
from objectpack.models import VirtualModel

from datatransfer.source.common.configuration import get_object
from datatransfer.source.get_data.models import GetDataChanges
from datatransfer.source.get_data.models import GetDataPerson
from datatransfer.source.get_data.models import GetDataPersonDocument
from datatransfer.source.get_data.models import GetDataRecordStatus

from .constants import CHANGE_DIFF
from .constants import CHANGE_MIXED
from .constants import CHANGE_NEW


extensions = get_object('get_data_extensions')()


class ChangesVirtualModel(VirtualModel):

    u"""Виртуальная модель изменений из контингента.

    Объединяет различия между принятыми данными и текущей моделью физлица,
    а также принятые изменения.
    """

    fields = (
        # Время получения изменения из контингента,
        'timestamp',
        # Время применения изменения,
        'applied',
        # Пользователь, внесший изменения,
        'user',
        # Старое значение поля,
        'old',
        # Новое значение поля,
        'new',
        # Является сохраненным изменением в GetDataChanges,
        'status',
        # Статус: принято/отклонено/ожидает решения.
        'comment'
    )

    models = (
        GetDataChanges,
        GetDataPerson,
        GetDataPersonDocument
    )

    change_types = {
        CHANGE_NEW: u'информация',
        CHANGE_DIFF: u'изменение данных',
        CHANGE_MIXED: u'информация / изменение данных',
    }

    def __init__(self, data):
        (pk, values) = data
        super(ChangesVirtualModel, self).__init__()
        self.id = pk
        for field, value in zip(self.fields, values):
            setattr(self, field, value)

    @classmethod
    def get_id(cls, model, pk):
        return '{}_{}'.format(cls.models.index(model), pk)

    @classmethod
    def get_instance(cls, id_value):
        try:
            model_id, pk = id_value.split('_')
            model = cls.models[int(model_id)]
        except (ValueError, KeyError):
            raise cls.DoesNotExist()
        instance = model.objects.get(id=pk)
        return instance

    @classmethod
    def _get_row(cls, person_data, change):
        if change.old:
            return (
                person_data.created,
                None,
                u'РС Контингент обучающихся',
                change.old,
                change.new,
                GetDataRecordStatus.values[GetDataRecordStatus.WAIT],
                cls.change_types[change.change_type]
            )

    @classmethod
    def _get_ids(cls, person_id=None):

        if person_id:
            # Отдаём изменение по физ. лицу и его документам
            try:
                person_data = GetDataPerson.objects.filter(
                    local_id=person_id
                )
                # Учитываем только актуальные данные из Контингента
                person_data = person_data.latest('id')
                change = extensions.get_change(person_data, True)
                row = cls._get_row(person_data, change)
                if row:
                    yield (
                        cls.get_id(GetDataPerson, person_data.id),
                        row
                    )

                documents = person_data.getdatapersondocument_set.iterator()
                for document in documents:
                    change = extensions.get_change(document, True)
                    row = cls._get_row(person_data, change)
                    if row:
                        yield (
                            cls.get_id(GetDataPersonDocument, document.id),
                            row
                        )

            except GetDataPerson.DoesNotExist:
                pass

            # Отдаём принятые изменения
            changes = GetDataChanges.objects.filter(
                local_id=person_id,
                model=ContentType.objects.get_for_model(
                    extensions.person_model_class
                )
            ).order_by('-applied')

            for change in changes:
                change_viewer = extensions.change_viewer_class(change)

                yield cls.get_id(GetDataChanges, change.id), (
                    change.session.timestamp,
                    change.applied,
                    change.user,
                    change_viewer.old,
                    change_viewer.new,
                    GetDataRecordStatus.values[change.status],
                    cls.change_types[change_viewer.change_type]
                )
