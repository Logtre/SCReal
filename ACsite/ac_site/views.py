# -*- coding:utf-8 -*-
from django.views.generic import TemplateView

from django.http import Http404
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

import datetime

#from .models import Prefecture, Company_table, Member_table, RegionSummary, Region
from .models import Region, Prefecture, City, PriceofLand, TourResource, ForeignGuest, ForeignGuestM, Consumption, HotelType, WebSite, RegionSummary, SummaryArticleBreakdown, SummaryCapacityBreakdown, SummaryLanguageBreakdown, SummarySizeBreakdown, Company_table, Member_table, MemberFlg_table

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
        latest_region_list = RegionSummary.objects.select_related('prefecture_id_rgs').all().filter(region_id__endswith=000).order_by('prefecture_id_rgs')
        print(latest_region_list.query)
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
        # RegionSummary + Prefecture
        region_info = RegionSummary.objects.select_related('prefecture_id_rgs').all().get(region_id=self.kwargs['region_id'])
        # SummaryArticleBreakdownの最新レコード
        sum_artcl = region_info.region_summary_id_artcl.select_related().all().order_by('-created_at')[:1]
        # SummaryCapacityBreakdownの最新レコード
        sum_cap = region_info.region_summary_id_cap.select_related().all().order_by('-created_at')[:1]
        # SummaryLanguageBreakdownの最新レコード
        sum_lang = region_info.region_summary_id_lang.select_related().all().order_by('-created_at')[:1]
        # SummarySizeBreakdownの最新レコード
        sum_size = region_info.region_summary_id_size.select_related().all().order_by('-created_at')[:1]
        # PriceofLand
        priceofland_info = PriceofLand.objects.select_related().all().filter(prefecture_id_pol=region_info.prefecture_id_rgs.prefecture_id_pref)
        # TourResource
        tourresource_info = TourResource.objects.select_related().all().filter(prefecture_id_scr=region_info.prefecture_id_rgs.prefecture_id_pref)
        #prefecture_info = Prefecture.objects.select_related().all().filter(prefecture_id_pref=region_info.prefecture_id_rgs.prefecture_id_pref)

        #print(region_info)
        #print(sum_artcl.query)
        print(priceofland_info.query)
        print(tourresource_info.query)
        context = {
            'region_info': region_info,
            'sum_artcl': sum_artcl,
            'sum_cap': sum_cap,
            'sum_lang': sum_lang,
            'sum_size': sum_size,
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
