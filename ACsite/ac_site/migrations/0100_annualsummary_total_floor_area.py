# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-18 10:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ac_site', '0099_auto_20171014_1656'),
    ]

    operations = [
        migrations.AddField(
            model_name='annualsummary',
            name='total_floor_area',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
    ]
