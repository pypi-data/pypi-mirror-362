# coding: utf-8
from __future__ import unicode_literals

from educommon.django.db.model_view import AttrValue
from educommon.django.db.model_view import FieldChoiceValue
from educommon.django.db.model_view import FieldVerboseName
from educommon.django.db.model_view import HtmlTableView
from educommon.django.db.model_view import ModelVerboseName


related_model_views = (
    HtmlTableView(
        model='catalog.FeedBack',
        description=ModelVerboseName(),
        columns=(
            dict(
                header=FieldVerboseName('session'),
                data=AttrValue('session')
            ),
            dict(
                header=FieldVerboseName('date_time'),
                data=AttrValue('date_time')
            ),
            dict(
                header=FieldVerboseName('result'),
                data=FieldChoiceValue('result')
            ),
            dict(
                header=FieldVerboseName('comment'),
                data=AttrValue('comment')
            ),
            dict(
                header=FieldVerboseName('xml'),
                data=AttrValue('xml')
            ),
            dict(
                header=FieldVerboseName('archive'),
                data=AttrValue('archive')
            ),
            dict(
                header=FieldVerboseName('last_update_date'),
                data=AttrValue('last_update_date')
            ),
        )
    ),
    HtmlTableView(
        model='catalog.FeedBackStatistic',
        description=ModelVerboseName(),
        columns=(
            dict(
                header=FieldVerboseName('model'),
                data=AttrValue('model')
            ),
            dict(
                header=FieldVerboseName('model_verbose'),
                data=AttrValue('model_verbose')
            ),
            dict(
                header=FieldVerboseName('total'),
                data=AttrValue('total')
            ),
            dict(
                header=FieldVerboseName('invalid'),
                data=AttrValue('invalid')
            ),
            dict(
                header=FieldVerboseName('processed'),
                data=AttrValue('processed')
            ),
            dict(
                header=FieldVerboseName('created'),
                data=AttrValue('created')
            ),
            dict(
                header=FieldVerboseName('updated'),
                data=AttrValue('updated')
            ),
        )
    ),
    HtmlTableView(
        model='catalog.FeedBackDetails',
        description=ModelVerboseName(),
        columns=(
            dict(
                header=FieldVerboseName('record_id'),
                data=AttrValue('record_id')
            ),
            dict(
                header=FieldVerboseName('message'),
                data=AttrValue('message')
            ),
            dict(
                header=FieldVerboseName('processed'),
                data=AttrValue('processed')
            ),
        )
    )
)
