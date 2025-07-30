# coding: utf-8
from __future__ import unicode_literals

from importlib import import_module

from django.apps.config import AppConfig


class GetDataAppConfig(AppConfig):

    name = __package__

    def _register_related_objects_views(self):
        """Добавляет представления для моделей приложения."""
        from educommon.django.db.model_view import registries

        if registries.get('related_objects'):
            model_views = import_module(self.name + '.model_views')
            registries['related_objects'].register(
                *model_views.related_model_views
            )

    def _register_tasks(self):
        """Регистрирует асинхронные задачи."""
        from .tasks import get_data_autorun_task
        from .tasks import get_data_push_rules
        from .tasks import get_data_push_task

    def ready(self):
        super(GetDataAppConfig, self).ready()
        self._register_related_objects_views()
        self._register_tasks()
