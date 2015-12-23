# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0006_auto_20150929_1106'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentReply',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('content', models.TextField(verbose_name='内容', blank=True, null=True)),
                ('publish_time', models.DateTimeField(auto_now_add=True)),
                ('author', models.CharField(max_length=100, default='匿名网友')),
                ('to', models.CharField(max_length=100, default='匿名网友')),
            ],
        ),
        migrations.RenameField(
            model_name='article',
            old_name='count',
            new_name='read_count_num',
        ),
        migrations.AddField(
            model_name='article',
            name='comment_count',
            field=models.IntegerField(verbose_name='评论数', default=0),
        ),
        migrations.AddField(
            model_name='comment',
            name='level',
            field=models.PositiveIntegerField(editable=False, db_index=True, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='comment',
            name='lft',
            field=models.PositiveIntegerField(editable=False, db_index=True, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='comment',
            name='parent',
            field=models.ForeignKey(to='article.Comment', blank=True, null=True, related_name='children'),
        ),
        migrations.AddField(
            model_name='comment',
            name='rght',
            field=models.PositiveIntegerField(editable=False, db_index=True, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='comment',
            name='tree_id',
            field=models.PositiveIntegerField(editable=False, db_index=True, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='commentreply',
            name='comment',
            field=models.ForeignKey(to='article.Comment', blank=True, null=True),
        ),
    ]
