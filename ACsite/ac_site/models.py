# -*- coding:utf-8 -*-
from django.db import models
from datetime import datetime
from django.utils import timezone
# Create your models here.

class Region(models.Model):
    '''地域情報テーブル'''
    prefecture_id = models.IntegerField(default=0, unique=True)
    city_id = models.IntegerField(default=0, unique=True)


class Prefecture(models.Model):
    '''都道府県テーブル'''
    #prefecture_id_pref = models.IntegerField(default=0)
    prefecture_id_pref = models.ForeignKey('Region', blank=True, null=True, db_column='prefecture_id_pref', to_field='prefecture_id', related_name='prefecture_id_pref', on_delete=models.CASCADE)
    prefecture = models.CharField(max_length=10)


class City(models.Model):
    '''市町村テーブル'''
    city_id_city = models.IntegerField(default=0)
    #city_id = models.ForeignKey(Region) phase2以降に対応
    city = models.CharField(max_length=30)


class PriceofLand(models.Model):
    '''地価テーブル'''
    priceofland_id = models.IntegerField(default=0)
    #prefecture_id_pol = models.IntegerField(default=0)
    prefecture_id_pol = models.ForeignKey('Region', blank=True, null=True, db_column='prefecture_id_pol', to_field='prefecture_id', related_name='prefecture_id_pol', on_delete=models.CASCADE)
    city_id_pol = models.IntegerField(default=0, null=True)
    #city_id_pol = models.ForeignKey(City) phase2以降に対応
    properties = models.IntegerField(default=0, null=True)
    average_price = models.IntegerField(default=0, null=True)
    upper_price = models.IntegerField(default=0, null=True)
    lower_price = models.IntegerField(default=0, null=True)


class TourResource(models.Model):
    '''観光資源テーブル'''
    scr_id = models.IntegerField(default=0)
    #prefecture_id_scr = models.IntegerField(default=0)
    prefecture_id_scr = models.ForeignKey('Region', blank=True, null=True, db_column='prefecture_id_scr', to_field='prefecture_id', related_name='prefecture_id_scr', on_delete=models.CASCADE)
    city_id_scr = models.IntegerField(default=0, null=True)
    #city_id = models.ForeignKey(City) phase2以降に対応
    scr_type1 = models.CharField(max_length=20, null=True)
    scr_type2 = models.CharField(max_length=20, null=True)
    scr_name = models.CharField(max_length=50, null=True)
    scr_rank = models.CharField(max_length=5, null=True)
    scr_score = models.IntegerField(default=0, null=True)


class ForeignGuest(models.Model):
    '''外国人旅行客テーブル'''
    num_of_foreign_id = models.IntegerField(default=0)
    #prefecture_id_frg = models.IntegerField(default=0)
    prefecture_id_frg = models.ForeignKey('Region', blank=True, null=True, db_column='prefecture_id_frg', to_field='prefecture_id', related_name='prefecture_id_frg', on_delete=models.CASCADE)
    year = models.IntegerField(default=0)
    number_of_guest = models.IntegerField(default=0, null=True)


class ForeignGuestM(models.Model):
    '''月次外国人旅行客テーブル'''
    num_of_foreign_month_id = models.IntegerField(default=0)
    #prefecture_id_frgm = models.IntegerField(default=0)
    prefecture_id_frgm = models.ForeignKey('Region', blank=True, null=True, db_column='prefecture_id_frgm', to_field='prefecture_id', related_name='prefecture_id_frgm', on_delete=models.CASCADE)
    year = models.IntegerField(default=0)
    month = models.IntegerField(default=0)
    number_of_guest = models.IntegerField(default=0, null=True)


class Consumption(models.Model):
    '''消費単価テーブル'''
    csm_id = models.IntegerField(default=0)
    #prefecture_id_csm = models.IntegerField(default=0)
    prefecture_id_csm = models.ForeignKey('Region', blank=True, null=True, db_column='prefecture_id_csm', to_field='prefecture_id', related_name='prefecture_id_csm', on_delete=models.CASCADE)
    num_of_answers = models.IntegerField(default=0, null=True)
    consumption = models.IntegerField(default=0, null=True)


class HotelType(models.Model):
    '''宿泊施設テーブル'''
    hotel_id = models.IntegerField(default=0)
    #prefecture_id_htl = models.IntegerField(default=0)
    prefecture_id_htl = models.ForeignKey('Region', blank=True, null=True, db_column='prefecture_id_htl', to_field='prefecture_id', related_name='prefecture_id_htl', on_delete=models.CASCADE)
    hotel = models.IntegerField(default=0, null=True)
    ryokan = models.IntegerField(default=0, null=True)
    condominium = models.IntegerField(default=0, null=True)
    dorm = models.IntegerField(default=0, null=True)
    house = models.IntegerField(default=0, null=True)
    youth_hostel = models.IntegerField(default=0, null=True)
    other = models.IntegerField(default=0, null=True)


class WebSite(models.Model):
    '''サイトテーブル'''
    web_id = models.IntegerField(default=0)
    #prefecture_id_web = models.IntegerField(default=0)
    prefecture_id_web = models.ForeignKey('Region', blank=True, null=True, db_column='prefecture_id_web', to_field='prefecture_id', related_name='prefecture_id_web', on_delete=models.CASCADE)
    city_id_web = models.IntegerField(default=0, null=True)
    website = models.IntegerField(default=0, null=True)


class RegionSummary(models.Model):
    '''Airb情報テーブルサマリー'''
    region_id = models.IntegerField(default=0, unique=True)
    #prefecture_id_rgs = models.IntegerField(default=0)
    prefecture_id_rgs = models.ForeignKey('Region', blank=True, null=True, db_column='prefecture_id_rgs', to_field='prefecture_id', related_name='prefecture_id_rgs', on_delete=models.CASCADE)
    city_id_rgs = models.IntegerField(default=0, null=True)
    #city_id_rgs = models.ForeignKey(City) phase2以降に対応
    total_listing = models.IntegerField(default=0, null=True)
    publish_count = models.IntegerField(default=0, null=True)
    suspend_count = models.IntegerField(default=0, null=True)
    reviewed_count = models.IntegerField(default=0, null=True)
    non_reviewed_count = models.IntegerField(default=0, null=True)
    average_price = models.IntegerField(default=0, null=True)
    monthly_sales = models.IntegerField(default=0, null=True)
    #region_summary_id = models.IntegerField(default=0)


class SummaryCapacityBreakdown(models.Model):
    '''Airb情報（収容人数別詳細）テーブル'''
    #region_summary_id_cap = models.IntegerField(default=0)
    region_summary_id_cap = models.ForeignKey('RegionSummary', blank=True, null=True, db_column='region_summary_id_cap', to_field='region_id', related_name='region_summary_id_cap', on_delete=models.CASCADE)
    capacity_type = models.CharField(max_length=10, null=True)
    listing_count = models.IntegerField(default=0, null=True)
    average_sales = models.IntegerField(default=0, null=True)
    average_rental_fee = models.IntegerField(default=0, null=True)
    created_at = models.DateTimeField(default=timezone.now)


class SummaryArticleBreakdown(models.Model):
    '''Airb情報（物件タイプ別詳細）テーブル'''
    #region_summary_id_artcl = models.IntegerField(default=0)
    region_summary_id_artcl = models.ForeignKey('RegionSummary', blank=True, null=True, db_column='region_summary_id_artcl', to_field='region_id', related_name='region_summary_id_artcl', on_delete=models.CASCADE)
    article_type = models.CharField(max_length=10, null=True)
    listing_count = models.IntegerField(default=0, null=True)
    created_at = models.DateTimeField(default=timezone.now)


class SummarySizeBreakdown(models.Model):
    '''Airb情報（部屋タイプ別情報）テーブル'''
    #region_summary_id_size = models.IntegerField(default=0)
    region_summary_id_size = models.ForeignKey('RegionSummary', blank=True, null=True, db_column='region_summary_id_size', to_field='region_id', related_name='region_summary_id_size', on_delete=models.CASCADE)
    room_size = models.CharField(max_length=10, null=True)
    listing_count = models.IntegerField(default=0, null=True)
    created_at = models.DateTimeField(default=timezone.now)


class SummaryLanguageBreakdown(models.Model):
    '''Airb情報（言語別詳細）テーブル'''
    #region_summary_id_lang = models.IntegerField(default=0)
    region_summary_id_lang = models.ForeignKey('RegionSummary', blank=True, null=True, db_column='region_summary_id_lang', to_field='region_id', related_name='region_summary_id_lang', on_delete=models.CASCADE)
    language_type = models.CharField(max_length=10, null=True)
    listing_count = models.IntegerField(default=0, null=True)
    created_at = models.DateTimeField(default=timezone.now)
#    dutch = models.IntegerField(default=0, null=True)
#    germany = models.IntegerField(default=0, null=True)
#    thai = models.IntegerField(default=0, null=True)
#    italian = models.IntegerField(default=0, null=True)
#    french = models.IntegerField(default=0, null=True)
#    korean = models.IntegerField(default=0, null=True)
#    chinese = models.IntegerField(default=0, null=True)
#    spanish = models.IntegerField(default=0, null=True)
#    english = models.IntegerField(default=0, null=True)
#    japanese = models.IntegerField(default=0, null=True)


#class ListingTrend(models.Model):
#    '''リスティング登録数推移テーブル'''
#    region_summary_id = models.IntegerField(default=0)
#    total_listing = models.IntegerField(default=0, null=True)
#    suspend_count = models.IntegerField(default=0, null=True)
#    created_at = models.DateTimeField(default=timezone.now)


class Company_table(models.Model):
    '''会社テーブル'''
    comp_id = models.IntegerField(default=0)
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=30)
    phone = models.CharField(max_length=15)
    ceo = models.CharField(max_length=30)
    gmap = models.CharField(max_length=300)
    url = models.CharField(max_length=30)


class Member_table(models.Model):
    '''メンバーテーブル'''
    member_id = models.IntegerField(default=0)
    name = models.CharField(max_length=30)
    comment = models.CharField(max_length=60, null=True)
    position = models.CharField(max_length=15, null=True)
    member_flg = models.IntegerField(default=0)
    twitter_url = models.CharField(max_length=100, null=True)
    facebook_url = models.CharField(max_length=100, null=True)
    linkedin_url = models.CharField(max_length=100, null=True)


class MemberFlg_table(models.Model):
    '''メンバーフラグテーブル'''
    member_flg = models.IntegerField(default=0)
    role = models.CharField(max_length=60)
