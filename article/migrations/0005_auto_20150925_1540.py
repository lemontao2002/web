# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0004_auto_20150925_1434'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='publish_time_new',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='publish_time',
            field=models.DateField(auto_now_add=True),
        ),
    ]
