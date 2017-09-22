# -*- coding:utf-8 -*-
from django.db import models
from datetime import datetime
from django.utils.timezone import now
# Create your models here.


class Prefecture(models.Model):
    '''都道府県テーブル'''
    prefecture_id = models.IntegerField(default=0)
    prefecture = models.CharField(max_length=10)


class City(models.Model):
    '''市町村テーブル'''
    city_id = models.IntegerField(default=0)
    city = models.CharField(max_length=30)


class PriceofLand(models.Model):
    '''地価テーブル'''
    priceofland_id = models.IntegerField(default=0)
    prefecture_id = models.IntegerField(default=0)
    city_id = models.IntegerField(default=0, null=True)
    properties = models.IntegerField(default=0, null=True)
    average_price = models.IntegerField(default=0, null=True)
    upper_price = models.IntegerField(default=0, null=True)
    lower_price = models.IntegerField(default=0, null=True)


class TourResource(models.Model):
    '''観光資源テーブル'''
    scr_id = models.IntegerField(default=0)
    prefecture_id = models.IntegerField(default=0)
    city_id = models.IntegerField(default=0, null=True)
    scr_type1 = models.CharField(max_length=20, null=True)
    scr_type2 = models.CharField(max_length=20, null=True)
    scr_name = models.CharField(max_length=50, null=True)
    scr_rank = models.CharField(max_length=5, null=True)
    scr_score = models.IntegerField(default=0, null=True)


class ForeignGuest(models.Model):
    '''外国人旅行客テーブル'''
    num_of_foreign_id = models.IntegerField(default=0)
    prefecture_id = models.IntegerField(default=0)
    year = models.IntegerField(default=0)
    number_of_guest = models.IntegerField(default=0, null=True)


class ForeignGuestM(models.Model):
    '''月次外国人旅行客テーブル'''
    num_of_foreign_month_id = models.IntegerField(default=0)
    prefecture_id = models.IntegerField(default=0)
    year = models.IntegerField(default=0)
    month = models.IntegerField(default=0)
    number_of_guest = models.IntegerField(default=0, null=True)


class Consumption(models.Model):
    '''消費単価テーブル'''
    csm_id = models.IntegerField(default=0)
    prefecture_id = models.IntegerField(default=0)
    num_of_answers = models.IntegerField(default=0, null=True)
    consumption = models.IntegerField(default=0, null=True)


class HotelType(models.Model):
    '''宿泊施設テーブル'''
    hotel_id = models.IntegerField(default=0)
    prefecture_id = models.IntegerField(default=0)
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
    prefecture_id = models.IntegerField(default=0)
    city_id = models.IntegerField(default=0, null=True)
    website = models.IntegerField(default=0, null=True)


class RegionSummary(models.Model):
    '''Airb情報テーブルサマリー'''
    region_id = models.IntegerField(default=0)
    total_listing = models.IntegerField(default=0, null=True)
    publish_count = models.IntegerField(default=0, null=True)
    suspend_count = models.IntegerField(default=0, null=True)
    reviewed_count = models.IntegerField(default=0, null=True)
    non_reviewed_count = models.IntegerField(default=0, null=True)
    average_price = models.IntegerField(default=0, null=True)
    monthly_sales = models.IntegerField(default=0, null=True)
    region_summary_id = models.IntegerField(default=0)


class SummarySizeBreakdown(models.Model):
    '''Airb情報（物件サイズ別情報）テーブル'''
    region_summary_id = models.IntegerField(default=0)
    room_size = models.CharField(max_length=10, null=True)
    listing_count = models.IntegerField(default=0, null=True)
    monthly_sales = models.IntegerField(default=0, null=True)
    created_at = models.DateTimeField(default=datetime.utcnow())


class SummaryArticleBreakdown(models.Model):
    '''Airb情報（部屋タイプ別詳細）テーブル'''
    region_summary_id = models.IntegerField(default=0)
    article_type = models.CharField(max_length=10, null=True)
    listing_count = models.IntegerField(default=0, null=True)
    created_at = models.DateTimeField(default=datetime.utcnow())


class SummaryLanguageBreakdown(models.Model):
    '''Airb情報（言語別詳細）テーブル'''
    region_summary_id = models.IntegerField(default=0)
    dutch = models.IntegerField(default=0, null=True)
    germany = models.IntegerField(default=0, null=True)
    thai = models.IntegerField(default=0, null=True)
    italian = models.IntegerField(default=0, null=True)
    french = models.IntegerField(default=0, null=True)
    korean = models.IntegerField(default=0, null=True)
    chinese = models.IntegerField(default=0, null=True)
    spanish = models.IntegerField(default=0, null=True)
    english = models.IntegerField(default=0, null=True)
    japanese = models.IntegerField(default=0, null=True)


class ListingTrend(models.Model):
    '''リスティング登録数推移テーブル'''
    region_summary_id = models.IntegerField(default=0)
    total_listing = models.IntegerField(default=0, null=True)
    publish_count = models.IntegerField(default=0, null=True)
    suspend_count = models.IntegerField(default=0, null=True)
    created_at = models.DateTimeField(default=datetime.utcnow())


class Region(models.Model):
    '''ID紐付け用中間テーブル'''
    prefecture_id = models.IntegerField(default=0)
    city_id = models.IntegerField(default=0)


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
