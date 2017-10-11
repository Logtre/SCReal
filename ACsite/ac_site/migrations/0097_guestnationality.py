# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-10 08:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ac_site', '0096_auto_20171010_1657'),
    ]

    operations = [
        migrations.CreateModel(
            name='GuestNationality',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prefecture_code', models.IntegerField(default=0)),
                ('answer_count', models.IntegerField(default=0)),
                ('visit_duration', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('nationality', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='link_guestnationality_nationality', to='ac_site.Nationality')),
                ('region', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='link_guestnationality', to='ac_site.Region')),
            ],
        ),
    ]