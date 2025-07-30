# coding: utf-8
from __future__ import absolute_import
from __future__ import print_function

from celery import current_app
from django.core.management.base import BaseCommand

from datatransfer.source.get_data.tasks import get_data_task


class Command(BaseCommand):
    u"""Запуск асинхронной задачи получения данных из "ИС Контингент"."""

    help = __doc__

    def handle(self, *args, **options):
        current_app.config_from_object('django.conf:settings')

        get_data_task.apply_async([], {})

        print(u'Процесс получения данных запущен')
