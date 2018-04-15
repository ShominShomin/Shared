# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-15 00:12
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20180330_1420'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.CharField(max_length=50)),
                ('start_time', models.TimeField(default=datetime.datetime(2018, 4, 15, 0, 12, 36, 537452, tzinfo=utc))),
                ('end_time', models.TimeField(default=datetime.datetime(2018, 4, 15, 0, 12, 36, 537452, tzinfo=utc))),
            ],
        ),
    ]
