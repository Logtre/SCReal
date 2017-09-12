# -*- coding:utf-8 -*-
from django.contrib import admin
from ac_site.models import Pref_table

# Register your models here.
# admin.site.register(Pref_table)

class Pref_tableAdmin(admin.ModelAdmin):
    '''pref_tableを編集する'''
    # リストを表示する
    list_display = ('pf_id', 'pref',)
admin.site.register(Pref_table, Pref_tableAdmin)
