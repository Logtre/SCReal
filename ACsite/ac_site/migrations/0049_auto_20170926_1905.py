# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-26 10:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ac_site', '0048_auto_20170926_1902'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='consumption',
            name='prefecture_id',
        ),
        migrations.AddField(
            model_name='consumption',
            name='prefecture',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ac_site.Prefecture'),
        ),
    ]
