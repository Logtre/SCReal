# -*- coding:utf-8 -*-
from django.db import models

# Create your models here.


class Prefecture(models.Model):
    '''都道府県テーブル'''
    pf_id = models.IntegerField(default=0)
    prefecture = models.CharField(max_length=10)


class City(models.Model):
    '''市町村テーブル'''
    cty_id = models.IntegerField(default=0)
    city = models.CharField(max_length=30)


class PriceofLand(models.Model):
    '''地価テーブル'''
    pol_id = models.IntegerField(default=0)
    properties = models.IntegerField(default=0)
    average = models.IntegerField(default=0)
    upper = models.IntegerField(default=0)
    lower = models.IntegerField(default=0)


class TourResource(models.Model):
    '''観光資源テーブル'''
    scr_id = models.IntegerField(default=0)
    scr_type1 = models.CharField(max_length=20)
    scr_type2 = models.CharField(max_length=20)
    scr_name = models.CharField(max_length=50)
    scr_rank = models.CharField(max_length=5)
    scr_score = models.IntegerField(default=0)


class ForeignGuest(models.Model):
    '''外国人旅行客テーブル'''
    foreign_id = models.IntegerField(default=0)
    gst_2011 = models.IntegerField(default=0)
    gst_2012 = models.IntegerField(default=0)
    gst_2013 = models.IntegerField(default=0)
    gst_2014 = models.IntegerField(default=0)
    gst_2015 = models.IntegerField(default=0)
    gst_2016 = models.IntegerField(default=0)


class ForeignGuestM(models.Model):
    '''月次外国人旅行客テーブル'''
    foreignm_id = models.IntegerField(default=0)
    gst_201101 = models.IntegerField(default=0)
    gst_201102 = models.IntegerField(default=0)
    gst_201103 = models.IntegerField(default=0)
    gst_201104 = models.IntegerField(default=0)
    gst_201105 = models.IntegerField(default=0)
    gst_201106 = models.IntegerField(default=0)
    gst_201107 = models.IntegerField(default=0)
    gst_201108 = models.IntegerField(default=0)
    gst_201109 = models.IntegerField(default=0)
    gst_201110 = models.IntegerField(default=0)
    gst_201111 = models.IntegerField(default=0)
    gst_201112 = models.IntegerField(default=0)
    gst_201201 = models.IntegerField(default=0)
    gst_201202 = models.IntegerField(default=0)
    gst_201203 = models.IntegerField(default=0)
    gst_201204 = models.IntegerField(default=0)
    gst_201205 = models.IntegerField(default=0)
    gst_201206 = models.IntegerField(default=0)
    gst_201207 = models.IntegerField(default=0)
    gst_201208 = models.IntegerField(default=0)
    gst_201209 = models.IntegerField(default=0)
    gst_201210 = models.IntegerField(default=0)
    gst_201211 = models.IntegerField(default=0)
    gst_201212 = models.IntegerField(default=0)
    gst_201301 = models.IntegerField(default=0)
    gst_201302 = models.IntegerField(default=0)
    gst_201303 = models.IntegerField(default=0)
    gst_201304 = models.IntegerField(default=0)
    gst_201305 = models.IntegerField(default=0)
    gst_201306 = models.IntegerField(default=0)
    gst_201307 = models.IntegerField(default=0)
    gst_201308 = models.IntegerField(default=0)
    gst_201309 = models.IntegerField(default=0)
    gst_201310 = models.IntegerField(default=0)
    gst_201311 = models.IntegerField(default=0)
    gst_201312 = models.IntegerField(default=0)
    gst_201401 = models.IntegerField(default=0)
    gst_201402 = models.IntegerField(default=0)
    gst_201403 = models.IntegerField(default=0)
    gst_201404 = models.IntegerField(default=0)
    gst_201405 = models.IntegerField(default=0)
    gst_201406 = models.IntegerField(default=0)
    gst_201407 = models.IntegerField(default=0)
    gst_201408 = models.IntegerField(default=0)
    gst_201409 = models.IntegerField(default=0)
    gst_201410 = models.IntegerField(default=0)
    gst_201411 = models.IntegerField(default=0)
    gst_201412 = models.IntegerField(default=0)
    gst_201501 = models.IntegerField(default=0)
    gst_201502 = models.IntegerField(default=0)
    gst_201503 = models.IntegerField(default=0)
    gst_201504 = models.IntegerField(default=0)
    gst_201505 = models.IntegerField(default=0)
    gst_201506 = models.IntegerField(default=0)
    gst_201507 = models.IntegerField(default=0)
    gst_201508 = models.IntegerField(default=0)
    gst_201509 = models.IntegerField(default=0)
    gst_201510 = models.IntegerField(default=0)
    gst_201511 = models.IntegerField(default=0)
    gst_201512 = models.IntegerField(default=0)
    gst_201601 = models.IntegerField(default=0)
    gst_201602 = models.IntegerField(default=0)
    gst_201603 = models.IntegerField(default=0)
    gst_201604 = models.IntegerField(default=0)
    gst_201605 = models.IntegerField(default=0)


class Consumption(models.Model):
    '''消費単価テーブル'''
    csm_id = models.IntegerField(default=0)
    num_of_answers = models.IntegerField(default=0)
    consumption = models.IntegerField(default=0)


class HotelType(models.Model):
    '''宿泊施設テーブル'''
    hotl_id = models.IntegerField(default=0)
    hotel = models.IntegerField(default=0)
    ryokan = models.IntegerField(default=0)
    condominium = models.IntegerField(default=0)
    dorm = models.IntegerField(default=0)
    house = models.IntegerField(default=0)
    youth_hostel = models.IntegerField(default=0)
    other = models.IntegerField(default=0)


class WebSite(models.Model):
    '''サイトテーブル'''
    web_id = models.IntegerField(default=0)
    website = models.IntegerField(default=0)


class RegionSummary(models.Model):
    '''Airb情報テーブルサマリー'''
    region_id = models.IntegerField(default=0)
    listing = models.IntegerField(default=0)
    publish = models.IntegerField(default=0)
    suspend = models.IntegerField(default=0)
    on_review = models.IntegerField(default=0)
    no_review = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    sales = models.IntegerField(default=0)
    cp_listing_sgl = models.IntegerField(default=0)
    cp_price_sgl = models.IntegerField(default=0)
    cp_listing_dble = models.IntegerField(default=0)
    cp_price_dble = models.IntegerField(default=0)
    cp_listing_fmly = models.IntegerField(default=0)
    cp_price_fmly = models.IntegerField(default=0)
    cp_listing_grup = models.IntegerField(default=0)
    cp_price_grup = models.IntegerField(default=0)


class SummarySizeBreakdown(models.Model):
    '''Airb情報（物件詳細）テーブル'''
    region_summary_id = models.IntegerField(default=0)
    lt_apt = models.IntegerField(default=0)
    lt_hus = models.IntegerField(default=0)
    lt_gsh = models.IntegerField(default=0)
    rt_rsv = models.IntegerField(default=0)
    rt_ind = models.IntegerField(default=0)
    rt_shr = models.IntegerField(default=0)


class SummaryArticleBreakdown(models.Model):
    '''Airb情報（物件詳細）テーブル'''
    region_summary_id = models.IntegerField(default=0)
    rgst_trend_XII = models.IntegerField(default=0)
    rgst_trend_XI = models.IntegerField(default=0)
    rgst_trend_X = models.IntegerField(default=0)
    rgst_trend_IX = models.IntegerField(default=0)
    rgst_trend_VIII = models.IntegerField(default=0)
    rgst_trend_VII = models.IntegerField(default=0)
    rgst_trend_VI = models.IntegerField(default=0)
    rgst_trend_V = models.IntegerField(default=0)
    rgst_trend_IV = models.IntegerField(default=0)
    rgst_trend_III = models.IntegerField(default=0)
    rgst_trend_II = models.IntegerField(default=0)
    rgst_trend_I = models.IntegerField(default=0)
    suspnd_trend_VII = models.IntegerField(default=0)
    suspnd_trend_VI = models.IntegerField(default=0)
    suspnd_trend_V = models.IntegerField(default=0)
    suspnd_trend_IV = models.IntegerField(default=0)
    suspnd_trend_III = models.IntegerField(default=0)
    suspnd_trend_II = models.IntegerField(default=0)
    suspnd_trend_I = models.IntegerField(default=0)


class SummaryLanguageBreakdown(models.Model):
    '''Airb情報（言語別詳細）テーブル'''
    region_summary_id = models.IntegerField(default=0)
    lang_ndl = models.IntegerField(default=0)
    lang_deu = models.IntegerField(default=0)
    lang_tha = models.IntegerField(default=0)
    lang_ita = models.IntegerField(default=0)
    lang_fra = models.IntegerField(default=0)
    lang_kor = models.IntegerField(default=0)
    lang_chn = models.IntegerField(default=0)
    lang_esp = models.IntegerField(default=0)
    lang_gbr = models.IntegerField(default=0)
    lang_jpn = models.IntegerField(default=0)


class Region(models.Model):
    '''ID紐付け用中間テーブル'''
    region_id = models.IntegerField(default=0)
    pf_id = models.IntegerField(default=0)
    cty_id = models.IntegerField(default=0, null=True)
    foreign_id = models.IntegerField(default=0)
    foreignm_id = models.IntegerField(default=0)
    csm_id = models.IntegerField(default=0)
    hotl_id = models.IntegerField(default=0)
    web_id = models.IntegerField(default=0)
    region_summary_id = models.IntegerField(default=0)


class Region_Tresource(models.Model):
    '''観光資源ID紐付け用中間テーブル'''
    scr_id = models.IntegerField(default=0)
    region_id = models.IntegerField(default=0)


class Region_PriceofLand(models.Model):
    pol_id = models.IntegerField(default=0)
    region_id = models.IntegerField(default=0)


class Publsh_table(models.Model):
    '''更新テーブル'''
    pref = models.DateTimeField('date published')
    city = models.DateTimeField('date published')
    priceofland = models.DateTimeField('date published')
    tresource = models.DateTimeField('date published')
    fgnguest = models.DateTimeField('date published')
    fgnguestm = models.DateTimeField('date published')
    csmprice = models.DateTimeField('date published')
    hotltype = models.DateTimeField('date published')
    website = models.DateTimeField('date published')
    air = models.DateTimeField('date published')
    rating = models.DateTimeField('date published')


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
    position = models.CharField(max_length=15)
    member_flg = models.IntegerField(default=0)
    twitter_url = models.CharField(max_length=100, null=True)
    facebook_url = models.CharField(max_length=100, null=True)
    linkedin_url = models.CharField(max_length=100, null=True)


class MemberFlg_table(models.Model):
    '''メンバーフラグテーブル'''
    member_flg = models.IntegerField(default=0)
    role = models.CharField(max_length=60)
