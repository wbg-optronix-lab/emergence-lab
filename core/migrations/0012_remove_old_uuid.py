# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-14 15:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_uuid_tmp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalprocess',
            name='uuid_full',
        ),
        migrations.RemoveField(
            model_name='process',
            name='uuid_full',
        ),
        migrations.RemoveField(
            model_name='processnode',
            name='uuid_full',
        ),
    ]
