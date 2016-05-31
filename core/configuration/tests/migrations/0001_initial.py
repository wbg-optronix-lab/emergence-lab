# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-30 21:15
from __future__ import unicode_literals

from django.db import migrations, models

import core.configuration.fields
from core.configuration.operations import PublishConfiguration, ConfigurationSubscribe


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('configuration', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfigurationTestModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('configuration', core.configuration.fields.ConfigurationField(default=core.configuration.fields.build_configuration_default)),
            ],
        ),
        PublishConfiguration('existing_key', 'default'),
        ConfigurationSubscribe(
            model_name='ConfigurationTestModel',
            field_name='configuration',
        )
    ]
