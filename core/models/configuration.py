# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

import six


@python_2_unicode_compatible
class AppConfigurationDefault(models.Model):
    """Freeform application configuration key-value pairs.

    Applications can publish configuration keys via PublishAppConfiguration
    and they can be accessed anywhere
    """
    key = models.CharField(max_length=200, blank=False)
    default_value = models.CharField(max_length=200, blank=True)
    choices = ArrayField(models.CharField(max_length=200, blank=True), default=list)

    def __str__(self):
        return '{}: {} {}'.format(self.key, self.default_value, self.choices)


def get_configuration_default(key):
    if not isinstance(key, six.string_types):
        raise TypeError('key must be a string')
    if not key:
        raise ValueError('key must not be an empty string')
    if '.' not in key:
        raise ValueError('key must be formatted as appname.keyname')

    config = AppConfigurationDefault.objects.get(key=key)
    return config.default_value


def get_configuration_choices(key):
    if not isinstance(key, six.string_types):
        raise TypeError('key must be a string')
    if not key:
        raise ValueError('key must not be an empty string')
    if '.' not in key:
        raise ValueError('key must be formatted as appname.keyname')

    config = AppConfigurationDefault.objects.get(key=key)
    return config.choices


def list_configuration_keys(app_name=None):
    if app_name is not None:
        if not isinstance(app_name, six.string_types):
            raise TypeError('app_name must be a string')
        if not app_name:
            raise ValueError('app_name must not be an empty string')

        return list(AppConfigurationDefault.objects.filter(key__startswith=app_name)
                                                   .values_list('key', flat=True))
    return list(AppConfigurationDefault.objects.all().values_list('key', flat=True))


@python_2_unicode_compatible
class InstanceConfiguration(models.Model):
    configuration = JSONField(default=dict)

    def __str__(self):
        return str(self.configuration)

    def __contains__(self, key):
        return key in self.configuration or key in list_configuration_keys()

    def __getitem__(self, key):
        if key in self.configuration:
            return self.configuration[key]
        elif key in list_configuration_keys():
            return get_configuration_default(key)
        else:
            raise KeyError('Configuration key "{}" is not defined'.format(key))

    def __setitem__(self, key, value):
        if key not in list_configuration_keys():
            raise KeyError('Configuration key "{}" is not defined'.format(key))
        choices = get_configuration_choices(key)
        if choices and value not in choices:
            raise ValueError(
                'Configuration value "{}" for key "{}" is not a valid choice. '
                'Valid options include {}.'.format(value, key, choices))
        self.configuration[key] = value
        self.save()
