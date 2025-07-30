# coding: utf-8
from __future__ import unicode_literals

from django.apps.config import AppConfig


class EnrollGetDataAppConfig(AppConfig):

    name = __package__

    def _register_tasks(self):
        """Регистрирует асинхронные задачи."""
        from .tasks import enroll_get_data_autorun_task
        from .tasks import enroll_get_data_push_rules
        from .tasks import enroll_get_data_push_task
        from .tasks import enroll_get_data_task

    def ready(self):
        super(EnrollGetDataAppConfig, self).ready()
        self._register_tasks()
