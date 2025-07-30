# coding: utf-8


PERIOD_DAY = 'DAY'
PERIOD_WEEK = 'WEEK'
PERIOD_MONTH = 'MONTH'
PERIOD_NEVER = 'NEVER'

PERIOD_CHOICES = (
    (PERIOD_NEVER, u'Не запрашивать'),
    (PERIOD_DAY, u'1 раз в день'),
    (PERIOD_WEEK, u'1 раз в неделю'),
    (PERIOD_MONTH, u'1 раз в месяц'),
)