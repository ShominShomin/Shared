# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-15 00:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20180415_0813'),
    ]

    operations = [
        migrations.CreateModel(
            name='BigText',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='No Title', max_length=40)),
                ('text', models.TextField(default=' ', max_length=1000)),
            ],
        ),
    ]