# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-14 20:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0002_create_processtypes'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActiveStateModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('status_changed', models.DateTimeField(blank=True, editable=False, null=True, verbose_name='status changed')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AutoUUIDModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ParentProcess',
            fields=[
                ('process_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.Process')),
                ('parent_field', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
            bases=('core.process',),
        ),
        migrations.CreateModel(
            name='UUIDModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid_full', models.UUIDField(default=uuid.uuid4, editable=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ChildProcess',
            fields=[
                ('parentprocess_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='tests.ParentProcess')),
                ('child_field', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
            bases=('tests.parentprocess',),
        ),
    ]
