# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-28 07:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ac_site', '0080_auto_20170928_1609'),
    ]

    operations = [
#        migrations.RenameField(
#            model_name='consumption',
#            old_name='prefecture_id_csm',
#            new_name='link_prefecture',
#        ),
#        migrations.RenameField(
#            model_name='foreignguest',
#            old_name='prefecture_id_frg',
#            new_name='link_prefecture',
#        ),
#        migrations.RenameField(
#            model_name='foreignguestm',
#            old_name='prefecture_id_frgm',
#            new_name='link_prefecture',
#        ),
#        migrations.RenameField(
#            model_name='hoteltype',
#            old_name='prefecture_id_htl',
#            new_name='link_prefecture',
#        ),
#        migrations.RenameField(
#            model_name='priceofland',
#            old_name='prefecture_id_pol',
#            new_name='link_prefecture',
#        ),
#        migrations.RenameField(
#            model_name='regionsummary',
#            old_name='prefecture_id_rgs',
#            new_name='link_prefecture',
#        ),
#        migrations.RenameField(
#            model_name='tourresource',
#            old_name='prefecture_id_scr',
#            new_name='link_prefecture',
#        ),
#        migrations.RenameField(
#            model_name='website',
#            old_name='prefecture_id_web',
#            new_name='link_prefecture',
#        ),
#        migrations.AlterField(
#            model_name='prefecture',
#            name='pref_id_consumption',
#            field=models.ForeignKey(blank=True, db_column=b'consumption_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='link_prefecture_csm', to='ac_site.Consumption', to_field=b'link_prefecture_id'),
#        ),
#        migrations.AlterField(
#            model_name='prefecture',
#            name='pref_id_hoteltype',
#            field=models.ForeignKey(blank=True, db_column=b'hoteltype_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='link_prefecture_hotel', to='ac_site.HotelType', to_field=b'link_prefecture_id'),
#        ),
#        migrations.AlterField(
#            model_name='prefecture',
#            name='pref_id_website',
#            field=models.ForeignKey(blank=True, db_column=b'website_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='link_prefecture_web', to='ac_site.WebSite', to_field=b'link_prefecture_id'),
#        ),
    ]