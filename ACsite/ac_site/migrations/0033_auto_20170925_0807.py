# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-24 23:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ac_site', '0032_delete_listingtrend'),
    ]

    operations = [
        migrations.RenameField(
            model_name='summarycapacitybreakdown',
            old_name='average_salses',
            new_name='average_sales',
        ),
    ]
