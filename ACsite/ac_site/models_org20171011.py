# -*- coding:utf-8 -*-
from django.db import models
from datetime import datetime
from django.utils import timezone
# Create your models here.


class Region(models.Model):
    '''地域情報テーブル'''
    #prefecture_id = models.IntegerField(default=0, unique=True)
    #city_id = models.IntegerField(default=0, unique=True)
    #prefecture_id = models.OneToOneField('Prefecture', blank=True, null=True, db_column='link_prefecture_id', to_field='prefecture_id', related_name='link_region', on_delete=models.CASCADE, unique=True)
    #prefecture_id = models.IntegerField(default=0, unique=True)
    prefecture = models.ForeignKey('Prefecture', blank=True, null=True, related_name='link_region_prefecture', on_delete=models.CASCADE)
    #city_id = models.IntegerField(default=0, null=True, unique=True) # city_idへのリンクはphase2以降に対応
    city = models.ForeignKey('City', blank=True, null=True, related_name='link_region_city', on_delete=models.CASCADE)


class Prefecture(models.Model):
    '''都道府県テーブル'''
    prefecture_code = models.IntegerField(default=0)
    #prefecture_id_pref = models.ForeignKey('Region', blank=True, null=True, db_column='prefecture_id_pref', to_field='prefecture_id', related_name='prefecture_id_pref', on_delete=models.CASCADE)
    prefecture_name = models.CharField(max_length=10)
    #region = models.ForeignKey('Region', blank=True, null=True, related_name='link_prefecture', on_delete=models.CASCADE)
    #priceofland = models.ForeignKey('PriceofLand', blank=True, null=True, db_column='priceofland', to_field='prefecture_id_pol', related_name='priceofland', on_delete=models.CASCADE)
    #tourresource = models.ForeignKey('TourResource', blank=True, null=True, db_column='tourresource', to_field='prefecture_id_scr', related_name='tourresource', on_delete=models.CASCADE)
    #foreignguest = models.ForeignKey('ForeignGuest', blank=True, null=True, db_column='foreignguest', to_field='prefecture_id_frg', related_name='foreignguest', on_delete=models.CASCADE)
    #foreignguestm = models.ForeignKey('ForeignGuestM', blank=True, null=True, db_column='foreignguestm', to_field='prefecture_id_pref', related_name='foreignguestm', on_delete=models.CASCADE)
    #pref_id_consumption = models.ForeignKey('Consumption', blank=True, null=True, db_column='consumption_id', to_field='link_prefecture_id', related_name='link_prefecture_csm', on_delete=models.CASCADE)
    #pref_id_hoteltype = models.ForeignKey('HotelType', blank=True, null=True, db_column='hoteltype_id', to_field='link_prefecture_id', related_name='link_prefecture_hotel', on_delete=models.CASCADE)
    #pref_id_website = models.ForeignKey('WebSite', blank=True, null=True, db_column='website_id', to_field='link_prefecture_id', related_name='link_prefecture_web', on_delete=models.CASCADE)
    #regionsum = models.ForeignKey('RegionSummary', blank=True, null=True, db_column='regionsum', to_field='prefecture_id_rgs', related_name='regionsum', on_delete=models.CASCADE)


class City(models.Model):
    '''市町村テーブル'''
    city_code = models.IntegerField(default=0)
    #city_id = models.ForeignKey(Region) phase2以降に対応
    city_name = models.CharField(max_length=30)
    #region = models.ForeignKey('Region', blank=True, null=True, related_name='link_city', on_delete=models.CASCADE)


class PriceofLand(models.Model):
    '''地価テーブル'''
    #priceofland_id = models.IntegerField(default=0)
    prefecture_code = models.IntegerField(default=0)
    #prefecture_id_pol = models.IntegerField(default=0)
    #prefecture_id_pol = models.ForeignKey('Region', blank=True, null=True, db_column='prefecture_id_pol', to_field='prefecture_id', related_name='prefecture_id_pol', on_delete=models.CASCADE)
    #link_prefecture = models.ForeignKey('Prefecture', blank=True, null=True, db_column='link_prefecture_id', to_field='prefecture_id', related_name='link_priceofland', on_delete=models.CASCADE)
    city_code = models.IntegerField(default=0, null=True)
    #city_id_pol = models.ForeignKey(City) phase2以降に対応
    properties_count = models.IntegerField(default=0, null=True)
    avg_price = models.IntegerField(default=0, null=True)
    upper_price = models.IntegerField(default=0, null=True)
    lower_price = models.IntegerField(default=0, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    region = models.ForeignKey('Region', blank=True, null=True, related_name='link_priceofland', on_delete=models.CASCADE)


class TourResource(models.Model):
    '''観光資源テーブル'''
    #scr_id = models.IntegerField(default=0)
    prefecture_code = models.IntegerField(default=0)
    #prefecture_id_scr = models.IntegerField(default=0)
    #prefecture_id_scr = models.ForeignKey('Region', blank=True, null=True, db_column='prefecture_id_scr', to_field='prefecture_id', related_name='prefecture_id_scr', on_delete=models.CASCADE)
    #link_prefecture = models.ForeignKey('Prefecture', blank=True, null=True, db_column='link_prefecture_id', to_field='prefecture_id', related_name='link_tourresource', on_delete=models.CASCADE)
    city_code = models.IntegerField(default=0, null=True)
    #city_id = models.ForeignKey(City) phase2以降に対応
    scr_type1 = models.CharField(max_length=20, null=True)
    scr_type2 = models.CharField(max_length=20, null=True)
    scr_name = models.CharField(max_length=50, null=True)
    scr_rank = models.CharField(max_length=5, null=True)
    scr_score = models.IntegerField(default=0, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    region = models.ForeignKey('Region', blank=True, null=True, related_name='link_tourresource', on_delete=models.CASCADE)


#class ForeignGuest(models.Model):
#    '''外国人旅行客テーブル'''
#    num_of_foreign_id = models.IntegerField(default=0)
#    #prefecture_id_frg = models.IntegerField(default=0)
#    #prefecture_id_frg = models.ForeignKey('Region', blank=True, null=True, db_column='prefecture_id_frg', to_field='prefecture_id', related_name='prefecture_id_frg', on_delete=models.CASCADE)
#    link_prefecture = models.ForeignKey('Prefecture', blank=True, null=True, db_column='link_prefecture_id', to_field='prefecture_id', related_name='link_foreignguest', on_delete=models.CASCADE)
#    year = models.IntegerField(default=0)
#    number_of_guest = models.IntegerField(default=0, null=True)


class ForeignGuestCount(models.Model):
    '''月次外国人旅行客テーブル'''
    #num_of_foreign_month_id = models.IntegerField(default=0)
    prefecture_code = models.IntegerField(default=0)
    #prefecture_id_frgm = models.IntegerField(default=0)
    #prefecture_id_frgm = models.ForeignKey('Region', blank=True, null=True, db_column='prefecture_id_frgm', to_field='prefecture_id', related_name='prefecture_id_frgm', on_delete=models.CASCADE)
    #link_prefecture = models.ForeignKey('Prefecture', blank=True, null=True, db_column='link_prefecture_id', to_field='prefecture_id', related_name='link_foreignguestm', on_delete=models.CASCADE)
    year = models.IntegerField(default=0)
    month = models.IntegerField(default=0)
    guest_count = models.IntegerField(default=0, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    region = models.ForeignKey('Region', blank=True, null=True, related_name='link_foreignguestcount', on_delete=models.CASCADE)


class AnnualSummary(models.Model):
    '''年次サマリーテーブル'''
    prefecture_code = models.IntegerField(default=0)
    year = models.IntegerField(default=0, null=True)
    consumer_count = models.IntegerField(default=0, null=True)
    consumption_ammount = models.IntegerField(default=0, null=True)
    guest_count_hotel = models.IntegerField(default=0, null=True)
    guest_count_ryokan = models.IntegerField(default=0, null=True)
    guest_count_condominium = models.IntegerField(default=0, null=True)
    guest_count_dorm = models.IntegerField(default=0, null=True)
    guest_count_house = models.IntegerField(default=0, null=True)
    guest_count_youthhostel = models.IntegerField(default=0, null=True)
    guest_count_other = models.IntegerField(default=0, null=True)
    website_count = models.IntegerField(default=0, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    region = models.ForeignKey('Region', blank=True, null=True, related_name='link_annualsummary', on_delete=models.CASCADE)


#class MonthlySummary(models.Model):
#    '''月次サマリーテーブル'''
#    prefecture_code = models.IntegerField(default=0)
#    city_code = models.IntegerField(default=0, null=True)
#    year = models.IntegerField(default=0)
#    month = models.IntegerField(default=0)
#    foreignguest_count = models.IntegerField(default=0, null=True)
#    total_listing = models.IntegerField(default=0, null=True)
#    publish_count = models.IntegerField(default=0, null=True)
#    suspend_count = models.IntegerField(default=0, null=True)
#    reviewed_count = models.IntegerField(default=0, null=True)
#    non_reviewed_count = models.IntegerField(default=0, null=True)
#    average_price = models.IntegerField(default=0, null=True)
#    monthly_sales = models.IntegerField(default=0, null=True)
#    created_at = models.DateTimeField(default=timezone.now)
#    region = models.ForeignKey('Region', blank=True, null=True, related_name='link_foreignguestcount', on_delete=models.CASCADE)


#class Consumption(models.Model):
#    '''消費単価テーブル'''
#    csm_id = models.IntegerField(default=0)
#    #prefecture_id_csm = models.IntegerField(default=0)
#    #prefecture_id_csm = models.ForeignKey('Region', blank=True, null=True, db_column='prefecture_id_csm', to_field='prefecture_id', related_name='prefecture_id_csm', on_delete=models.CASCADE)
#    #prefecture_id_csm = models.ForeignKey('Prefecture', blank=True, null=True, db_column='prefecture_id_csm', to_field='prefecture_id_pref', related_name='prefecture_id_csm', on_delete=models.CASCADE, unique=True)
#    link_prefecture = models.OneToOneField('Prefecture', blank=True, null=True, db_column='link_prefecture_id', to_field='prefecture_id', related_name='link_consumption', on_delete=models.CASCADE)
#    num_of_answers = models.IntegerField(default=0, null=True)
#    consumption = models.IntegerField(default=0, null=True)


#class HotelType(models.Model):
#    '''宿泊施設テーブル'''
#    hotel_id = models.IntegerField(default=0)
#    #prefecture_id_htl = models.IntegerField(default=0)
#    #prefecture_id_htl = models.ForeignKey('Region', blank=True, null=True, db_column='prefecture_id_htl', to_field='prefecture_id', related_name='prefecture_id_htl', on_delete=models.CASCADE)
#    #prefecture_id_htl = models.ForeignKey('Prefecture', blank=True, null=True, db_column='prefecture_id_htl', to_field='prefecture_id_pref', related_name='prefecture_id_htl', on_delete=models.CASCADE, unique=True)
#    link_prefecture = models.OneToOneField('Prefecture', blank=True, null=True, db_column='link_prefecture_id', to_field='prefecture_id', related_name='link_hoteltype', on_delete=models.CASCADE)
#    hotel = models.IntegerField(default=0, null=True)
#    ryokan = models.IntegerField(default=0, null=True)
#    condominium = models.IntegerField(default=0, null=True)
#    dorm = models.IntegerField(default=0, null=True)
#    house = models.IntegerField(default=0, null=True)
#    youth_hostel = models.IntegerField(default=0, null=True)
#    other = models.IntegerField(default=0, null=True)


#class WebSite(models.Model):
#    '''サイトテーブル'''
#    web_id = models.IntegerField(default=0)
#    #prefecture_id_web = models.IntegerField(default=0)
#    #prefecture_id_web = models.ForeignKey('Region', blank=True, null=True, db_column='prefecture_id_web', to_field='prefecture_id', related_name='prefecture_id_web', on_delete=models.CASCADE)
#    #prefecture_id_web = models.ForeignKey('Prefecture', blank=True, null=True, db_column='prefecture_id_web', to_field='prefecture_id_pref', related_name='prefecture_id_web', on_delete=models.CASCADE, unique=True)
#    link_prefecture = models.OneToOneField('Prefecture', blank=True, null=True, db_column='link_prefecture_id', to_field='prefecture_id', related_name='link_website', on_delete=models.CASCADE)
#    link_city = models.IntegerField(default=0, null=True)
#    website = models.IntegerField(default=0, null=True)


class RegionSummary(models.Model):
    '''Airb情報テーブルサマリー'''
    #region_id = models.IntegerField(default=0, unique=True)
    #prefecture_id_rgs = models.IntegerField(default=0)
    #prefecture_id_rgs = models.ForeignKey('Region', blank=True, null=True, db_column='prefecture_id_rgs', to_field='prefecture_id', related_name='prefecture_id_rgs', on_delete=models.CASCADE)
    #link_prefecture = models.ForeignKey('Prefecture', blank=True, null=True, db_column='link_prefecture_id', to_field='prefecture_id', related_name='link_regionsummary', on_delete=models.CASCADE)
    prefecture_code = models.IntegerField(default=0, null=True)
    city_code = models.IntegerField(default=0, null=True)
    #city_id_rgs = models.ForeignKey(City) phase2以降に対応
    year = models.IntegerField(default=0)
    month = models.IntegerField(default=0)
    total_listing = models.IntegerField(default=0, null=True)
    publish_count = models.IntegerField(default=0, null=True)
    suspend_count = models.IntegerField(default=0, null=True)
    reviewed_count = models.IntegerField(default=0, null=True)
    non_reviewed_count = models.IntegerField(default=0, null=True)
    average_price = models.IntegerField(default=0, null=True)
    monthly_sales = models.IntegerField(default=0, null=True)
    #region_summary_id = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    region = models.ForeignKey('Region', blank=True, null=True, related_name='link_regionsummary', on_delete=models.CASCADE)
    #region = models.IntegerField(default=0, null=True)


class SummaryCapacityBreakdown(models.Model):
    '''Airb情報（収容人数別詳細）テーブル'''
    #region_summary_id_cap = models.IntegerField(default=0)
    region_summary = models.ForeignKey('RegionSummary', blank=True, null=True, related_name='capacity_breakdown', on_delete=models.CASCADE)
    link_prefecture_code = models.IntegerField(default=0)
    link_city_code = models.IntegerField(default=0, null=True)
    capacity_type = models.CharField(max_length=10, null=True)
    listing_count = models.IntegerField(default=0, null=True)
    average_sales = models.IntegerField(default=0, null=True)
    average_rental_fee = models.IntegerField(default=0, null=True)
    created_at = models.DateTimeField(default=timezone.now)


class SummaryArticleBreakdown(models.Model):
    '''Airb情報（物件タイプ別詳細）テーブル'''
    #region_summary_id_artcl = models.IntegerField(default=0)
    region_summary = models.ForeignKey('RegionSummary', blank=True, null=True, related_name='article_breakdown', on_delete=models.CASCADE)
    link_prefecture_code = models.IntegerField(default=0)
    link_city_code = models.IntegerField(default=0, null=True)
    article_type = models.CharField(max_length=10, null=True)
    listing_count = models.IntegerField(default=0, null=True)
    created_at = models.DateTimeField(default=timezone.now)


class SummarySizeBreakdown(models.Model):
    '''Airb情報（部屋タイプ別情報）テーブル'''
    #region_summary_id_size = models.IntegerField(default=0)
    region_summary = models.ForeignKey('RegionSummary', blank=True, null=True, related_name='size_breakdown', on_delete=models.CASCADE)
    link_prefecture_code = models.IntegerField(default=0)
    link_city_code = models.IntegerField(default=0, null=True)
    room_size = models.CharField(max_length=10, null=True)
    listing_count = models.IntegerField(default=0, null=True)
    created_at = models.DateTimeField(default=timezone.now)


class SummaryLanguageBreakdown(models.Model):
    '''Airb情報（言語別詳細）テーブル'''
    #region_summary_id_lang = models.IntegerField(default=0)
    region_summary = models.ForeignKey('RegionSummary', blank=True, null=True, related_name='language_breakdown', on_delete=models.CASCADE)
    link_prefecture_code = models.IntegerField(default=0)
    link_city_code = models.IntegerField(default=0, null=True)
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
