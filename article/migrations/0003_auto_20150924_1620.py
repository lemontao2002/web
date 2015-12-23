# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0002_auto_20150923_1556'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('content', models.TextField(verbose_name='内容', null=True, blank=True)),
                ('publish_time', models.DateField(auto_now_add=True)),
                ('author', models.CharField(max_length=30, verbose_name='名字')),
            ],
            options={
                'verbose_name': '评论',
                'verbose_name_plural': '评论',
            },
        ),
        migrations.AlterModelOptions(
            name='article',
            options={'verbose_name': '文章', 'ordering': ['-publish_time'], 'verbose_name_plural': '文章'},
        ),
        migrations.AlterModelOptions(
            name='author',
            options={'verbose_name': '作者', 'verbose_name_plural': '作者'},
        ),
        migrations.AlterModelOptions(
            name='classification',
            options={'verbose_name': '文章分类', 'verbose_name_plural': '文章分类'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'verbose_name': '标签', 'verbose_name_plural': '标签'},
        ),
        migrations.AlterField(
            model_name='article',
            name='author',
            field=models.ForeignKey(to='article.Author', verbose_name='作者'),
        ),
        migrations.AlterField(
            model_name='article',
            name='classification',
            field=models.ForeignKey(to='article.Classification', verbose_name='分类'),
        ),
        migrations.AlterField(
            model_name='article',
            name='content',
            field=models.TextField(verbose_name='内容', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='count',
            field=models.IntegerField(default=0, verbose_name='点击数量'),
        ),
        migrations.AlterField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(verbose_name='标签', to='article.Tag', blank=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(max_length=100, verbose_name='文章名称'),
        ),
        migrations.AlterField(
            model_name='author',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='邮箱', blank=True),
        ),
        migrations.AlterField(
            model_name='author',
            name='name',
            field=models.CharField(max_length=30, verbose_name='名字'),
        ),
        migrations.AlterField(
            model_name='author',
            name='website',
            field=models.URLField(verbose_name='网站', blank=True),
        ),
        migrations.AlterField(
            model_name='classification',
            name='name',
            field=models.CharField(max_length=25, verbose_name='分类名称'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=20, verbose_name='标签名称', blank=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='article',
            field=models.ForeignKey(to='article.Article', verbose_name='文章'),
        ),
    ]
