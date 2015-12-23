# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0003_auto_20150924_1620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='publish_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
