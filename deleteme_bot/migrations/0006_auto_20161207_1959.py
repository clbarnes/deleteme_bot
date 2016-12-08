# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-08 00:59
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deleteme_bot', '0005_auto_20161207_1958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deletemebotsingleton',
            name='last_run',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 8, 0, 59, 44, 566740)),
        ),
        migrations.AlterField(
            model_name='reddituser',
            name='refresh_token',
            field=models.CharField(max_length=80, unique=True),
        ),
        migrations.AlterField(
            model_name='statecode',
            name='expires',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 8, 1, 59, 44, 568138)),
        ),
    ]