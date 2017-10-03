# -*- coding:utf-8 -*-
from django.views.generic import TemplateView

from django.http import Http404
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.db.models import Avg

import datetime

#from .models import Company_table, Member_table
from .models import Region, Prefecture, City, PriceofLand, TourResource, ForeignGuestCount, AnnualSummary, RegionSummary, SummaryArticleBreakdown, SummaryCapacityBreakdown, SummaryLanguageBreakdown, SummarySizeBreakdown, Company_table, Member_table, MemberFlg_table
from .rating import marketsize


today = datetime.date.today()

class TopView(TemplateView):
    template_name = "index.html"

    def get(self, request, **kwargs):
        company_info = Company_table.objects.order_by('-comp_id')[:1]
        member_info = Member_table.objects.order_by('member_id')[:1]
        context = {
            'company_info': company_info,
            'member_info': member_info,
        }
        return self.render_to_response(context)


class CompanyView(TemplateView):
    '''会社一覧'''
    template_name = "companies.html"

    def get(self, request, **kwargs):
        company_info = Company_table.objects.order_by('-comp_id')[:1]
        context = {
            'company_info': company_info,
        }
        return self.render_to_response(context)


class CompanyShowView(TemplateView):
    '''会社詳細'''
    template_name = "company_show.html"

    def get(self, request, **kwargs):
        company_info = Company_table.objects.order_by('-comp_id')[:1]
        context = {
            'company_info': company_info,
        }
        return self.render_to_response(context)


class ContactView(TemplateView):
    '''お問い合わせ時に表示する会社情報を取得する（静的）'''
    template_name = "contact.html"

    def get(self, request, **kwargs):
        company_info = Company_table.objects.order_by('-comp_id')[:1]
        context = {
            'company_info': company_info,
        }
        return self.render_to_response(context)


class RatingView(TemplateView):
    '''Airテーブルよりレーティング情報を取得する'''
    template_name = "rating.html"

    def get(self, request, **kwargs):
        #pref = int(request.GET.get('prefecture_id', None))
        #print(">>>DEBUG>>> prefecture_id is: %d" % prefecture_id)
        region_info = RegionSummary.objects.filter(prefecture_id_rgs=self.kwargs['rating_id'], region_id__endswith='000').select_related().all()
        print(region_info.query)
        context = {
            'region_info': region_info,
        }
        return self.render_to_response(context)


class PrefectureView(TemplateView):
    '''prefectureテーブルより都道府県一覧を取得する'''
    template_name = "prefectures.html"

    def get(self, request, **kwargs):
        #latest_region_list = Region.objects.select_related().all().filter(city_id = None).filter(prefecture__prefecture_code__isnull = False)
        latest_region_list = Region.objects.select_related().all().filter(city_id = None)
        #prefecture_list = latest_region_list.filter(link_prefecture__prefecture_code = prefecture_id)
        #prefecture_list = latest_region_list.link_prefecture.select_related().all().filter(prefecture__region_id)
        print(latest_region_list.query)
        #print(prefecture_list.query)
        context = {
            'latest_region_list': latest_region_list,
        }
        return self.render_to_response(context)


class PrefectureShowView(TemplateView):
    '''都道府県の詳細'''
    template_name = "prefecture_show.html"

    def get(self, request, **kwargs):
        ''' objects.getコマンド ----> オブジェクトを返す
            objects.filterコマンド ----> クエリセットを返す
            外部キーの逆引きはオブジェクトにしか使えないので注意
        '''
        # ミクロ情報の取得1
        # RegionSummaryの最新レコード（全都道府県分）
        region_sum_info = RegionSummary.objects.select_related().all().order_by('-created_at')[:47]
        # SummaryArticleBreakdownの最新レコード（全都道府県分）
        sum_articlebd_info = SummaryArticleBreakdown.objects.select_related().all().order_by('-created_at')[:141] # 3*47
        # SummaryCapacityBreakdownの最新レコード（全都道府県分）
        sum_capacitybd_info = SummaryCapacityBreakdown.objects.select_related().all().order_by('-created_at')[:188] # 4*47
        # SummaryLanguageBreakdownの最新レコード（全都道府県分）
        sum_languagebd_info = SummaryLanguageBreakdown.objects.select_related().all().order_by('-created_at')[:470] # 10*47
        # SummarySizeBreakdownの最新レコード（全都道府県分）
        sum_sizebd_info = SummarySizeBreakdown.objects.select_related().all().order_by('-created_at')[:141] # 3*47

        '''DEBUG用
        print(">>>>DEBUG>>>> region_sum_info is :")
        print(region_sum_info.values())
        print(">>>>DEBUG>>>> sum_articlebd_info is :")
        print(sum_articlebd_info.values())
        print(">>>>DEBUG>>>> sum_capacitybd_info is :")
        print(sum_capacitybd_info.values())
        print(">>>>DEBUG>>>> sum_languagebd_info is :")
        print(sum_languagebd_info.values())
        print(">>>>DEBUG>>>> sum_sizebd_info is :")
        print(sum_sizebd_info.values())
        '''


        # ミクロ情報の取得2
        # RegionSummaryの対象レコード
        trg_region_sum_info = RegionSummary.objects.get(region_id=self.kwargs['region_id'])
        # SummaryArticleBreakdownの対象レコード
        trg_sum_articlebd_info = trg_region_sum_info.article_breakdown
        # SummaryCapacityBreakdownの対象レコード
        trg_sum_capacitybd_info = trg_region_sum_info.capacity_breakdown
        # SummaryLanguageBreakdownの対象レコード
        trg_sum_languagebd_info = trg_region_sum_info.language_breakdown
        # SummarySizeBreakdownの対象レコード
        trg_sum_sizebd_info = trg_region_sum_info.size_breakdown

        '''DEBUG用
        print(">>>>DEBUG>>>> trg_region_sum_info is :")
        print(trg_region_sum_info)
        print(">>>>DEBUG>>>> trg_sum_articledb_info is :")
        print(trg_sum_articlebd_info.values())
        print(">>>>DEBUG>>>> trg_sum_languagebd_info is :")
        print(trg_sum_languagebd_info.values())
        print(">>>>DEBUG>>>> trg_sum_sizebd_info is :")
        print(trg_sum_sizebd_info.values())
        '''


        # マクロ情報
        # Prefecture + Consumption + HotelType + Website
        region_info = Region.objects.select_related().all().get(id=self.kwargs['region_id'])
        # PriceofLand（全地域分）
        #priceofland_info = region_info.link_priceofland.select_related().all()
        #priceofland_info = PriceofLand.objects.filter(region_id=self.kwargs['region_id'])
        priceofland_info = PriceofLand.objects.select_related().all().order_by('-created_at')[:556] # 全地域
        # TourResource（全地域分）
        #tourresource_info = region_info.link_tourresource.select_related().all()
        #tourresource_info = TourResource.objects.filter(region_id=self.kwargs['region_id'])
        tourresource_info = TourResource.objects.select_related().all().order_by('-created_at')[:2788] # 全地域
        # ForeignGuestCount（全地域分）
        #foreignguest_info = region_info.link_foreignguestcount.select_related().all()
        #foreignguest_info = ForeignGuestCount.objects.get(region_id=self.kwargs['region_id'])
        foreignguest_info = ForeignGuestCount.objects.select_related().all() # 全履歴
        # AnnualSummary（全地域分）
        #annualsummary_info = region_info.link_annualsummary.select_related().all()
        #annualsummary_info = AnnualSummary.objects.get(region_id=self.kwargs['region_id'])
        annualsummary_info = AnnualSummary.objects.select_related().all().order_by('-created_at')[:47] # 全都道府県

        ''' DEBUG用
        print(">>>>DEBUG>>>> region_info is :")
        print(region_info)
        print(">>>>DEBUG>>>> priceofland is :")
        print(priceofland_info.values())
        print(">>>>DEBUG>>>> tourresource_info is :")
        print(tourresource_info.values())
        print(">>>>DEBUG>>>> foreignguest_info is :")
        print(foreignguest_info.values())
        print(">>>>DEBUG>>>> annualsummary_info is :")
        print(annualsummary_info.values())
        '''


        # レーティング関連情報の取得

        # 市場規模
        # 平均観光客数(昨年度)
        avg_guest_count = foreignguest_info.filter(year=today.year-1).aggregate(Avg('guest_count'))["guest_count__avg"]
        # 対象都道府県の観光客数(昨年度)
        trg_guest_count = foreignguest_info.filter(year=today.year-1).filter(region_id=self.kwargs['region_id']).aggregate(Avg('guest_count'))["guest_count__avg"]
        # 平均消費金額(昨年度)
        avg_consumption_amount = annualsummary_info.aggregate(Avg('consumption_ammount'))["consumption_ammount__avg"]
        # 対象都道府県の消費金額(昨年度)
        trg_consumption_amount = AnnualSummary.objects.filter(year=today.year-1).get(region_id=self.kwargs['region_id']).consumption_ammount
        # 平均売上(今年度)
        avg_monthly_sales = region_sum_info.aggregate(Avg('monthly_sales'))["monthly_sales__avg"]
        # 都道府県の売上(最新月)
        trg_monthly_sales = trg_region_sum_info.monthly_sales
        # 市場規模レーティング
        mrktsize = marketsize(trg_guest_count, avg_guest_count, trg_consumption_amount, avg_consumption_amount, trg_monthly_sales, avg_monthly_sales)

        '''DEBUG用
        print(">>>>DEBUG>>>> avg_guest_count is :")
        print(avg_guest_count)
        print(">>>>DEBUG>>>> trg_guest_count is :")
        print(trg_guest_count)
        print(">>>>DEBUG>>>> avg_consumption_amount is :")
        print(avg_consumption_amount)
        print(">>>>DEBUG>>>> trg_consumption is :")
        print(trg_consumption_amount)
        print(">>>>DEBUG>>>> avg_monthly_sales is :")
        print(avg_monthly_sales)
        print(">>>>DEBUG>>>> trg_monthly_sales is :")
        print(trg_monthly_sales)
        print(">>>>DEBUG>>>> mrktsize is :")
        print(mrktsize)
        '''


        context = {
            'region_sum_info': region_sum_info,
            'region_info': region_info,
            'sum_articlebd_info': sum_articlebd_info,
            #'sum_cap': sum_cap,
            #'sum_lang': sum_lang,
            #'sum_size': sum_size,
        }
        return self.render_to_response(context)


def current_datetime(request):
    '''現在時刻を表示する'''
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)


def services(request):
    '''投稿一覧を取得する'''
    return render(request, 'static/services.html', {})


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'ac_site/detail.html', {'question': question})


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
