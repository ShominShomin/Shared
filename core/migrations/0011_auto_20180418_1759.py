# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-18 09:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20180415_1237'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reservation',
            old_name='city_name',
            new_name='address',
        ),
    ]
