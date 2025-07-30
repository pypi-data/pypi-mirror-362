# coding: utf-8

from __future__ import absolute_import

from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from educommon.contingent.contingent_plugin.models import \
    ContingentModelChanged


def choices(model, field):
    return dict(model._meta.get_field(field).choices)


def multi_choices(model, field):
    return dict(model._meta.get_field(field).base_field.choices)


def join_workaround(field):
    return (Q(**{'{0}__isnull'.format(field): True})
    | Q(**{'{0}__isnull'.format(field): False}))


def date_skip(info_date):
    return info_date and info_date.year < 9000 and info_date or None


def updated_filter(model, field='pk'):
    u"""Возвращает Q фильтр по измененным моделям."""
    content_type = ContentType.objects.get_for_model(model)
    objects = ContingentModelChanged.objects.filter(content_type=content_type)
    return Q(**{'%s__in' % field: objects.values_list('object_id', flat=True)})
