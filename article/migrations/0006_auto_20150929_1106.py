# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0005_auto_20150925_1540'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='publish_time_new',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='publish_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
