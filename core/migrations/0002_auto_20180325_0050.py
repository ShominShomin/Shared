# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-24 16:50
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='is_occupied',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='room',
            name='last_cleaned',
            field=models.DateField(default=datetime.datetime.now),
        ),
    ]
