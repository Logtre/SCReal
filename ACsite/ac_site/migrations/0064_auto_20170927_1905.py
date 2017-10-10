# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-27 10:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ac_site', '0063_prefecture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prefecture',
            name='prefecture_id_pref',
            field=models.OneToOneField(blank=True, db_column=b'prefecture_id_pref', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='prefecture_id_pref', to='ac_site.Region', to_field=b'prefecture_id'),
        ),
    ]
