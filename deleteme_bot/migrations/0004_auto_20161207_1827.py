# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-07 23:27
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deleteme_bot', '0003_auto_20161207_1826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deletemebotsingleton',
            name='last_run',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 7, 23, 27, 56, 605940)),
        ),
        migrations.AlterField(
            model_name='statecode',
            name='expires',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 8, 0, 27, 56, 607422)),
        ),
        migrations.AlterField(
            model_name='statecode',
            name='state_code',
            field=models.CharField(max_length=80, unique=True),
        ),
    ]