# -*- coding:utf-8 -*-
from django.contrib import admin
#from ac_site.models import Prefecture, Company_table, Member_table
from ac_site.models import Company_table, Member_table


# Register your models here.
#admin.site.register(Prefecture)
admin.autodiscover()


#class PrefectureAdmin(admin.ModelAdmin):
#    '''Prefectureを編集する'''
#    # リストを表示する
#    list_display = ('prefecture_id', 'prefecture',)
#    admin.site.register(Prefecture)


class Company_tableAdmin(admin.ModelAdmin):
    '''company_tableを編集する'''
    # リストを表示する
    list_display = ('comp_id', 'name', 'address', 'phone', 'ceo', 'gmap', 'url',)
    admin.site.register(Company_table)


class Member_tableAdmin(admin.ModelAdmin):
    '''Member_tableを編集する'''
    # リストを表示する
    list_display = ('member_id', 'name', 'comment', 'position', 'member_flg', 'twitter_url', 'facebook_url', 'linkedin_url',)
    admin.site.register(Member_table)
