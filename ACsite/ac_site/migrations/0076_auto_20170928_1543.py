# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-28 06:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ac_site', '0075_auto_20170928_1541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='summaryarticlebreakdown',
            name='region_summary_id_artcl',
            field=models.ForeignKey(blank=True, db_column=b'region_summary_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='article_breakdown', to='ac_site.RegionSummary', to_field=b'region_id'),
        ),
        migrations.AlterField(
            model_name='summarycapacitybreakdown',
            name='region_summary_id_cap',
            field=models.ForeignKey(blank=True, db_column=b'region_summary_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='capacity_breakdown', to='ac_site.RegionSummary', to_field=b'region_id'),
        ),
        migrations.AlterField(
            model_name='summarylanguagebreakdown',
            name='region_summary_id_lang',
            field=models.ForeignKey(blank=True, db_column=b'region_summary_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='language_breakdown', to='ac_site.RegionSummary', to_field=b'region_id'),
        ),
        migrations.AlterField(
            model_name='summarysizebreakdown',
            name='region_summary_id_size',
            field=models.ForeignKey(blank=True, db_column=b'region_summary_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='size_breakdown', to='ac_site.RegionSummary', to_field=b'region_id'),
        ),
    ]