# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-26 11:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ac_site', '0050_remove_consumption_prefecture'),
    ]

    operations = [
#        migrations.RemoveField(
#            model_name='regionsummary',
#            name='region_summary_id',
#        ),
#        migrations.AddField(
#            model_name='consumption',
#            name='prefecture_id',
#            field=models.ForeignKey(blank=True, db_column=b'prefecture_id_csm', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='prefecture_id_csm', to='ac_site.Region', to_field=b'prefecture_id'),
#        ),
#        migrations.AlterField(
#            model_name='region',
#            name='city_id',
#            field=models.IntegerField(default=0, unique=True),
#        ),
#        migrations.AlterField(
#            model_name='region',
#            name='prefecture_id',
#            field=models.IntegerField(default=0, unique=True),
#        ),
#        migrations.AlterField(
#            model_name='regionsummary',
#            name='region_id',
#            field=models.IntegerField(default=0, unique=True),
#        ),
    ]