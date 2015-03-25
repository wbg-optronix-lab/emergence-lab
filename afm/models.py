# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.db import models

from core.models import DataFile, Process


class AFMScan(Process):
    """
    Stores afm characterization information.
    """
    name = 'AFM Scan'
    slug = 'afm'
    is_destructive = False


class AFMFile(DataFile):
    """
    Stores the raw file and extracted data associated with an afm scan.
    """
    LOCATION_CHOICES = [
        ('c', 'Center'),
        ('r', 'Round'),
        ('f', 'Flat'),
    ]

    scan_number = models.IntegerField(default=0)

    rms = models.DecimalField(max_digits=7, decimal_places=3)
    zrange = models.DecimalField(max_digits=7, decimal_places=3)
    location = models.CharField(max_length=45, choices=LOCATION_CHOICES, default='c')
    size = models.DecimalField(max_digits=7, decimal_places=3)
