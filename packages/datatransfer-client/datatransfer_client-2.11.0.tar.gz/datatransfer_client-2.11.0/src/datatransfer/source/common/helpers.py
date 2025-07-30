# coding: utf-8

from __future__ import absolute_import

from django.db import connection


def set_isolation_level(level):
    u"""Устанавливает текущий уровень изоляции транзакций."""
    cursor = connection.cursor()
    cursor.execute('set transaction isolation level {}'.format(level))


def get_isolation_level():
    u"""Возвращает текущий уровень изоляции транзакций."""
    cursor = connection.cursor()
    cursor.execute("select current_setting('transaction_isolation')")
    return cursor.cursor.fetchone()[0]
