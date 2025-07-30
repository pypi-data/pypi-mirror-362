# coding: utf-8
from __future__ import unicode_literals

from __future__ import absolute_import
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [('catalog', '0001_initial'), ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='comment',
            field=models.TextField(
                null=True, verbose_name='Комментарий', blank=True), ),
    ]
