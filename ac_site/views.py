# -*- coding:utf-8 -*-
#for social login(これを指定すれば、相対パスで全てのファイルが読み込める)
from allauth.account.views import LoginView, SignupView, LogoutView

from django.views.generic import TemplateView

from django.http import Http404
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.db.models import Avg, Q, Sum

import datetime

#from .models import Company_table, Member_table
from .models import Region, Prefecture, City, PriceofLand, TourResource, ForeignGuestCount, AnnualSummary, RegionSummary, SummaryArticleBreakdown, SummaryCapacityBreakdown, SummaryLanguageBreakdown, SummarySizeBreakdown, Cost, GuestNationality, Nationality, Ranking, Company_table, Member_table, MemberFlg_table
from .rating import individual_rating, elemental_rating, cal_stdev, cal_beta, city_list

from django.http import HttpResponseRedirect
from django.shortcuts import redirect

today = datetime.date.today()


'''非ログインユーザーをログイン画面にリダイレクトする関数'''
def check_loginuser(request):
    if not request.user.is_authenticated():
        return HttpResponse('/signin/?next=%s' % request.path)
    else:
        pass


class SigninView(LoginView):
    '''サインイン(ログイン)'''
    template_name = "signin/index.html"

    def dispatch(self, request, *args, **kwargs):
        response = super(SigninView, self).dispatch(request, *args, **kwargs)
        return response

    def form_valid(self, form):
        return super(SigninView, self).form_valid(form)

signin_view = SigninView.as_view()


class SignupView(SignupView):
    '''サインアップ(会員登録)'''
    template_name = "signup/index.html"

    def get_context_data(self, **kwargs):
        context = super(SignupView, self).get_context_data(**kwargs)
        return context

signup_view = SignupView.as_view()


class SignoutView(LogoutView):
    '''ログアウト'''
    #template_name = "signout/index.html"

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            self.logout()
        return redirect('/')

signout_view = SignoutView.as_view()


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


class RankingView(TemplateView):
    '''民泊ランキングを表示する'''
    template_name = "ranking.html"

    def get(self, request, **kwargs):
        total_listing_ranking = Ranking.objects.select_related().all().filter(region__city_id__isnull=False).filter(created_at__month=today.month).order_by('total_listing_rank')[0:10]
        average_price_ranking = Ranking.objects.select_related().all().filter(region__city_id__isnull=False).filter(created_at__month=today.month).order_by('average_price_rank')[0:10]
        monthly_sales_ranking = Ranking.objects.select_related().all().filter(region__city_id__isnull=False).filter(created_at__month=today.month).order_by('monthly_sales_rank')[0:10]

        '''DEBUG用'''
        print(">>>>DEBUG>>>> total_listing_ranking is :")
        print(total_listing_ranking.query)
        print(">>>>DEBUG>>>> average_price_ranking is :")
        print(average_price_ranking.query)
        print(">>>>DEBUG>>>> monthly_sales_ranking is :")
        print(monthly_sales_ranking.query)
        ''''''

        context = {
            'total_listing_ranking': total_listing_ranking,
            'average_price_ranking': average_price_ranking,
            'monthly_sales_ranking': monthly_sales_ranking,
        }
        return self.render_to_response(context)


class PropertiesView(TemplateView):
    '''cityにひもづく物件一覧を取得する'''
    template_name="properties.html"

    def get(self, request, **kwargs):
        # ログイン有無のチェック
        check_loginuser(request)

        # ミクロ情報の取得2
        # RegionSummaryの対象レコード
        try:
            trg_region_sum_info = RegionSummary.objects.select_related().all().get(region_id=self.kwargs['region_city_id'], year=today.year, month=today.month)
        except RegionSummary.DoesNotExist:
            raise Http404("No MyModel matches the given query.")

        context = {
            'trg_region_sum_info': trg_region_sum_info,
        }
        return self.render_to_response(context)


class PropertyShowView(TemplateView):
    '''物件詳細を取得する'''
    template_name="property.html"

    def get(self, request, **kwargs):
        # ログイン有無の確認
        check_loginuser(request)

        # ミクロ情報の取得2
        # RegionSummaryの対象レコード
        try:
            trg_region_sum_info = RegionSummary.objects.select_related().all().get(region_id=self.kwargs['region_city_id'], year=today.year, month=today.month)
        except RegionSummary.DoesNotExist:
            raise Http404("No MyModel matches the given query.")

        context = {
            'trg_region_sum_info': trg_region_sum_info,
        }
        return self.render_to_response(context)


class PrefectureView(TemplateView):
    '''prefectureテーブルより都道府県一覧を取得する'''
    template_name = "prefectures.html"

    def get(self, request, **kwargs):
        #latest_city_id = City.objects.select_related().all().filter(city_code__in=city_list())
        latest_region_list = Region.objects.select_related().all().filter(city_id=None)

        '''DEBUG用
        print(">>>>DEBUG>>>> latest_region_list is :")
        print(latest_region_list.query)
        '''

        context = {
            'latest_region_list': latest_region_list,
        }
        return self.render_to_response(context)




class CityView(TemplateView):
    '''Cityテーブルより市区町村一覧を取得する'''
    template_name = "cities.html"

    def get(self, request, **kwargs):
        #latest_city_id = City.objects.select_related().all().filter(city_code__in=city_list())
        focus_region_id = int(self.kwargs['region_id']) * 1000
        next_region_id = focus_region_id + 1000
        # 都道府県
        latest_prefecture = Region.objects.select_related().all().get(prefecture__prefecture_code=self.kwargs['region_id'], city_id=None)
        # 市区町村
        latest_region_list = Region.objects.select_related().all().filter(Q(city__city_code__gte=focus_region_id), Q(city__city_code__lt=next_region_id), Q(city_id=None) | Q(city__city_code__in=city_list()))

        '''DEBUG用
        #print(">>>>DEBUG>>>> latest_city_id is :")
        #print(latest_city_id.query)
        print(">>>>DEBUG>>>> latest_region_list is :")
        print(latest_region_list.query)
        for q in latest_region_list:
            print(q.id)
        '''

        context = {
            'latest_prefecture': latest_prefecture,
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
        #region_sum_info = RegionSummary.objects.select_related().all()
        # SummaryArticleBreakdownの最新レコード（全都道府県分）
        #sum_articlebd_info = SummaryArticleBreakdown.objects.select_related().all()
        # SummaryCapacityBreakdownの最新レコード（全都道府県分）
        #sum_capacitybd_info = SummaryCapacityBreakdown.objects.select_related().all()
        # SummaryLanguageBreakdownの最新レコード（全都道府県分）
        #sum_languagebd_info = SummaryLanguageBreakdown.objects.select_related().all()
        # SummarySizeBreakdownの最新レコード（全都道府県分）
        #sum_sizebd_info = SummarySizeBreakdown.objects.select_related().all()

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
        try:
            trg_region_sum_info = RegionSummary.objects.select_related().all().get(region_id=self.kwargs['region_id'], year=today.year, month=today.month)
        except RegionSummary.DoesNotExist:
            raise Http404("No MyModel matches the given query.")
        # SummaryArticleBreakdownの対象レコード
        #trg_sum_articlebd_info = trg_region_sum_info.article_breakdown
        # SummaryCapacityBreakdownの対象レコード
        #trg_sum_capacitybd_info = trg_region_sum_info.capacity_breakdown
        # SummaryLanguageBreakdownの対象レコード
        #trg_sum_languagebd_info = trg_region_sum_info.language_breakdown
        # SummarySizeBreakdownの対象レコード
        #trg_sum_sizebd_info = trg_region_sum_info.size_breakdown

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
        # Prefecture
        region_info = Region.objects.select_related().all().get(id=self.kwargs['region_id'])
        # PriceofLand（全地域分）
        #priceofland_info = PriceofLand.objects.select_related().all()
        # TourResource（全地域分）
        #tourresource_info = TourResource.objects.select_related().all()
        # ForeignGuestCount（全地域分）
        #foreignguest_info = ForeignGuestCount.objects.select_related().all()
        # AnnualSummary（全地域分）
        #annualsummary_info = AnnualSummary.objects.select_related().all()
        # GuestNationality（全地域分）
        #guestnationality_info = GuestNationality.objects.select_related().all()

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

        # 1.市場規模(訪問客の数)の計算
        # 1.1.観光客数(昨年度)
        # 1.1.1.対象都道府県単体の観光客数
        #trg_guest_count = foreignguest_info.filter(year=today.year-1).filter(region_id=self.kwargs['region_id']).aggregate(Avg('guest_count'))["guest_count__avg"]
        #trg_guest_count = ForeignGuestCount.objects.all().filter(year=today.year-1).filter(region_id=self.kwargs['region_id']).aggregate(Avg('guest_count'))["guest_count__avg"]
        trg_guest_count = 0
        # 1.1.2.平均観光客数(全都道府県)
        #avg_guest_count = foreignguest_info.filter(year=today.year-1).aggregate(Avg('guest_count'))["guest_count__avg"]
        #avg_guest_count = ForeignGuestCount.objects.all().filter(year=today.year-1).filter(region_id__lte=47).aggregate(Avg('guest_count'))["guest_count__avg"]
        avg_guest_count = 0

        # 1.2.消費金額(昨年度)
        # 1.2.1.対象都道府県単体の消費金額
        #trg_consumption_amount = annualsummary_info.filter(year=today.year-1).get(region_id=self.kwargs['region_id']).consumption_ammount
        #trg_consumption_amount = AnnualSummary.objects.all().filter(year=today.year-1).get(region_id=self.kwargs['region_id']).consumption_ammount
        trg_consumption_amount = 0
        # 1.2.2.平均消費金額(全都道府県)
        #avg_consumption_amount = annualsummary_info.filter(year=today.year-1).aggregate(Avg('consumption_ammount'))["consumption_ammount__avg"]
        #avg_consumption_amount = AnnualSummary.objects.all().filter(year=today.year-1).filter(region_id__lte=47).aggregate(Avg('consumption_ammount'))["consumption_ammount__avg"]
        avg_consumption_amount = 0

        # 1.3.民泊売上(最新月)
        # 1.3.1.対象都道府県単体の売上
        trg_monthly_sales = trg_region_sum_info.monthly_sales
        # 1.3.2.平均売上
        #avg_monthly_sales = region_sum_info.aggregate(Avg('monthly_sales'))["monthly_sales__avg"]
        avg_monthly_sales = RegionSummary.objects.all().filter(year__gte=2017).filter(month__gte=10).filter(city_code__isnull=True).aggregate(Avg('monthly_sales'))["monthly_sales__avg"]

        # 1.4.市場規模レーティング
        #marketsize = round(individual_rating(trg_guest_count, avg_guest_count, trg_consumption_amount, avg_consumption_amount, trg_monthly_sales, avg_monthly_sales), 2)
        marketsize = round(elemental_rating(trg_monthly_sales, avg_monthly_sales))

        '''DEBUG用
        print(">>>>DEBUG>>>> trg_guest_count is :")
        print(trg_guest_count)
        print(">>>>DEBUG>>>> avg_guest_count is :")
        print(avg_guest_count)
        print(">>>>DEBUG>>>> trg_consumption is :")
        print(trg_consumption_amount)
        print(">>>>DEBUG>>>> avg_consumption_amount is :")
        print(avg_consumption_amount)
        print(">>>>DEBUG>>>> trg_monthly_sales is :")
        print(trg_monthly_sales)
        print(">>>>DEBUG>>>> avg_monthly_sales is :")
        print(avg_monthly_sales)
        print(">>>>DEBUG>>>> marketsize is :")
        print(marketsize)
        '''


        # 2.将来性（将来の見込み売上）の計算
        # 2.1.観光客変化率(trg_guest_count - prv_guest_count)
        # 2.1.1.観光客数の変化率（対象都道府県分）
        # 2.1.1.1当年分
        #trg_guest_count = foreignguest_info.filter(year=today.year-1).filter(month=today.month).get(region_id=self.kwargs['region_id']).guest_count
        trg_guest_count = ForeignGuestCount.objects.all().filter(year=today.year-1).filter(month=today.month).get(region_id=self.kwargs['region_id']).guest_count
        # 2.1.1.2前年分
        #prv_guest_count = foreignguest_info.filter(year=today.year-2).filter(month=today.month).get(region_id=self.kwargs['region_id']).guest_count
        prv_guest_count = ForeignGuestCount.objects.all().filter(year=today.year-2).filter(month=today.month).get(region_id=self.kwargs['region_id']).guest_count
        # 2.1.1.3.差分
        trg_diff_guest_count = trg_guest_count - prv_guest_count
        # 2.1.2.観光客変化率の平均値
        # 2.1.2.1.当年分
        #avg_trg_guest_count = foreignguest_info.filter(year=today.year-1).filter(month=today.month).aggregate(Avg('guest_count'))["guest_count__avg"]
        avg_trg_guest_count = ForeignGuestCount.objects.all().filter(year=today.year-1).filter(month=today.month).filter(region_id__lte=47).aggregate(Avg('guest_count'))["guest_count__avg"]
        # 2.1.2.2.前年分
        #avg_prv_guest_count = foreignguest_info.filter(year=today.year-2).filter(month=today.month).aggregate(Avg('guest_count'))["guest_count__avg"]
        avg_prv_guest_count = ForeignGuestCount.objects.all().filter(year=today.year-2).filter(month=today.month).filter(region_id__lte=47).aggregate(Avg('guest_count'))["guest_count__avg"]
        # 2.1.2.3.差分
        avg_diff_guest_count = avg_trg_guest_count - avg_prv_guest_count

        # 2.2.観光資源のスコア
        # 2.2.1.対象地域のスコア
        #trg_tourresource_score = tourresource_info.filter(region_id=self.kwargs['region_id']).aggregate(Avg('scr_score'))["scr_score__avg"]
        #trg_tourresource_score = TourResource.objects.all().filter(region_id=self.kwargs['region_id']).aggregate(Avg('scr_score'))["scr_score__avg"]
        trg_tourresource_score = 0
        # 2.2.2.平均スコア(全都道府県)
        #avg_tourresource_score = tourresource_info.aggregate(Avg('scr_score'))["scr_score__avg"]
        #avg_tourresource_score = TourResource.objects.all().aggregate(Avg('scr_score'))["scr_score__avg"]
        avg_tourresource_score = 0

        # 2.3.リスティング数の変化率(Phase1では対象外)
        # 2.3.1.リスティング数の変化率（対象都道府県分）
        # 2.3.1.1.当月分
        #trg_total_listing = region_sum_info.filter(year=today.year).filter(month=today.month).get(region_id=self.kwargs['region_id']).total_listing
        # 2.3.1.2.前月分
        #prv_total_listing = region_sum_info.filter(year=today.year).filter(month=today.month-1).get(region_id=self.kwargs['region_id']).total_listing
        # 2.3.1.3.差分
        #trg_diff_total_listing = trg_total_listing - prv_total_listing
        trg_diff_total_listing = 0
        # 2.3.2.リスティング数の変化率の平均値
        # 2.3.2.1.当月分
        #avg_trg_total_listing = region_sum_info.filter(year=today.year).filter(month=today.month).aggregate(Avg('total_listing'))["total_listing__avg"]
        # 2.3.2.2.前月分
        #avg_prv_total_listing = region_sum_info.filter(year=today.year).filter(month=today.month-1).aggregate(Avg('total_listing'))["total_listing__avg"]
        # 2.3.2.3.差分
        #avg_diff_total_listing = avg_trg_total_listing - avg_prv_total_listing
        avg_diff_total_listing = 0

        # 2.4.将来性
        potential = round(individual_rating(trg_diff_guest_count, avg_diff_guest_count, trg_tourresource_score, avg_tourresource_score, trg_diff_total_listing, avg_diff_total_listing), 2)

        '''DEBUG用
        print(">>>>DEBUG>>>> trg_guest_count is :")
        print(trg_guest_count)
        print(">>>>DEBUG>>>> prv_guest_count is :")
        print(prv_guest_count)
        print(">>>>DEBUG>>>> trg_diff_guest_count is :")
        print(trg_diff_guest_count)
        print(">>>>DEBUG>>>> avg_trg_guest_count is :")
        print(avg_trg_guest_count)
        print(">>>>DEBUG>>>> avg_prv_guest_count is :")
        print(avg_prv_guest_count)
        print(">>>>DEBUG>>>> avg_diff_guest_cont is :")
        print(avg_diff_guest_count)
        print(">>>>DEBUG>>>> trg_tourresource_score is :")
        print(trg_tourresource_score)
        print(">>>>DEBUG>>>> avg_tourresource_score is :")
        print(avg_tourresource_score)
        #print(">>>>DEBUG>>>> trg_total_listing is :")
        #print(trg_total_listing)
        #print(">>>>DEBUG>>>> prv_total_listing is :")
        #print(prv_total_listing)
        print(">>>>DEBUG>>>> trg_diff_total_listing is :")
        print(trg_diff_total_listing)
        #print(">>>>DEBUG>>>> avg_trg_total_listing is :")
        #print(avg_trg_total_listing)
        #print(">>>>DEBUG>>>> avg_prv_total_listing is :")
        #print(avg_prv_total_listing)
        print(">>>>DEBUG>>>> avg_diff_total_listing is :")
        print(avg_diff_total_listing)
        print(">>>>DEBUG>>>> potential is :")
        print(potential)
        '''


        # 3.安定性(季節ごとの売上変動)
        # 3.1.観光客ボラティリティ
        # 3.1.1.観光客ボラティリティ（対象都道府県分）
        # 3.1.1.1.当月観光客数
        #trg_guest_count_for_volatility = foreignguest_info.filter(region_id=self.kwargs['region_id']).order_by('-id')[:12]
        trg_guest_count_for_volatility = ForeignGuestCount.objects.all().filter(region_id=self.kwargs['region_id']).order_by('-id')[:12]
        #trg_guest_count_for_volatility = 0
        # 3.1.1.2.前月観光客数
        #prv_guest_count_for_volatility = foreignguest_info.filter(region_id=self.kwargs['region_id']).order_by('-id')[1:13]
        prv_guest_count_for_volatility = ForeignGuestCount.objects.all().filter(region_id=self.kwargs['region_id']).order_by('-id')[1:13]
        #prv_guest_count_for_volatility = 0
        # 3.1.1.3.標準偏差
        trg_stdev = cal_stdev(trg_guest_count_for_volatility, prv_guest_count_for_volatility)
        #trg_stdev = 1
        # 3.1.2.観光客ボラティリティ（モデル都道府県分）
        # 3.1.2.1.モデル都道府県の当月平均観光客数
        #avg_guest_count_for_volatility = foreignguest_info.filter(region_id=22).order_by('-id')[:12]
        #avg_guest_count_for_volatility = ForeignGuestCount.objects.all().filter(region_id=22).order_by('-id')[:12]
        avg_guest_count_for_volatility = 0
        # 3.1.2.2.モデル都道府県の前月平均観光客数
        #avg_prv_guest_count_for_volatility = foreignguest_info.filter(region_id=22).order_by('-id')[1:13]
        #avg_prv_guest_count_for_volatility = ForeignGuestCount.objects.all().filter(region_id=22).order_by('-id')[1:13]
        avg_prv_guest_count_for_volatility = 0
        # 3.1.2.3.標準偏差
        #avg_stdev = cal_stdev(avg_guest_count_for_volatility, avg_prv_guest_count_for_volatility)
        avg_stdev = 1

        # 3.2.観光客の変化率の変化率（ベータ）
        # 3.2.1.観光客のベータ（対象都道府県分）
        # 3.2.1.1.当月観光客数
        trg_guest_count_for_beta = trg_guest_count_for_volatility
        # 3.2.1.2.前月観光客数
        prv_guest_count_for_beta = prv_guest_count_for_volatility
        # 3.2.1.3.前々月観光客数
        #prvprv_guest_count_for_beta = foreignguest_info.filter(region_id=self.kwargs['region_id']).order_by('-id')[2:14]
        #prvprv_guest_count_for_beta = ForeignGuestCount.objects.all().filter(region_id=self.kwargs['region_id']).order_by('-id')[2:14]
        prvprv_guest_count_for_beta = 0
        # 3.2.1.4.ベータ
        #trg_beta = cal_beta(trg_guest_count_for_beta, prv_guest_count_for_beta, prvprv_guest_count_for_beta)
        trg_beta = 1
        # 3.2.2.観光客のベータ（対象都道府県分）
        # 3.2.2.1.モデル都道府県の当月観光客数
        avg_guest_count_for_beta = avg_guest_count_for_volatility
        # 3.2.2.2.モデル都道府県の前月観光客数
        avg_prv_guest_count_for_beta = avg_prv_guest_count_for_volatility
        # 3.2.2.3.モデル都道府県の前々月観光客数
        #avg_prvprv_guest_count_for_beta = foreignguest_info.filter(region_id=22).order_by('-id')[2:14]
        #avg_prvprv_guest_count_for_beta = ForeignGuestCount.objects.all().filter(region_id=22).order_by('-id')[2:14]
        avg_prvprv_guest_count_for_beta = 0
        # 3.2.2.4.モデル都道府県のベータ
        #avg_beta = cal_beta(avg_guest_count_for_beta, avg_prv_guest_count_for_beta, avg_prvprv_guest_count_for_beta)
        avg_beta = 1

        # 3.3.リスティング数の変化率(Phase1では対象外)
        # 3.3.1.リスティング数の変化率(対象都道府県分)
        # 3.3.1.1.当月分
        #trg_total_listing = region_sum_info.filter(year=today.year).filter(month=today.month).get(region_id=self.kwargs['region_id']).total_listing
        # 3.3.1.2.前月分
        #prv_total_listing = region_sum_info.filter(year=today.year).filter(month=today.month-1).get(region_id=self.kwargs['region_id']).total_listing
        # 3.3.1.3.差分
        #trg_diff_total_listing = trg_total_listing - prv_total_listing
        trg_diff_total_listing_for_volatility = 0
        # 3.3.2.リスティング数の変化率の平均値
        # 3.3.2.1.当月分
        #avg_trg_total_listing = region_sum_info.filter(year=today.year).filter(month=today.month).aggregate(Avg('total_listing'))["total_listing__avg"]
        # 3.3.2.2.前月分
        #avg_prv_total_listing = region_sum_info.filter(year=today.year).filter(month=today.month-1).aggregate(Avg('total_listing'))["total_listing__avg"]
        # 3.3.2.3.差分
        #avg_diff_total_listing = avg_trg_total_listing - avg_prv_total_listing
        avg_diff_total_listing_for_volatility = 0

        # 3.4.安定性
        #stability = round(5 - individual_rating(trg_stdev, avg_stdev, trg_beta, avg_beta, trg_diff_total_listing_for_volatility, avg_diff_total_listing_for_volatility), 2)
        stability = 2

        '''DEBUG用
        print(">>>>DEBUG>>>> trg_guest_count_for_volatility is :")
        print(trg_guest_count_for_volatility.values())
        print(">>>>DEBUG>>>> prv_guest_count_for_volatility is :")
        print(prv_guest_count_for_volatility.values())
        print(">>>>DEBUG>>>> trg_stdev is :")
        print(trg_stdev)
        print(">>>>DEBUG>>>> avg_guest_count_for_volatility is :")
        print(avg_guest_count_for_volatility.values())
        print(">>>>DEBUG>>>> avg_prv_guest_count_for_volatility is :")
        print(avg_prv_guest_count_for_volatility.values())
        print(">>>>DEBUG>>>> avg_stdev is :")
        print(avg_stdev)
        print(">>>>DEBUG>>>> trg_guest_count_for_beta is :")
        print(trg_guest_count_for_beta.values())
        print(">>>>DEBUG>>>> prv_guest_count_for_beta is :")
        print(prv_guest_count_for_beta.values())
        print(">>>>DEBUG>>>> prvprv_guest_count_for_beta is :")
        print(prvprv_guest_count_for_beta.values())
        print(">>>>DEBUG>>>> trg_beta is :")
        print(trg_beta)
        print(">>>>DEBUG>>>> avg_guest_count_for_beta is :")
        print(avg_guest_count_for_beta.values())
        print(">>>>DEBUG>>>> avg_prv_guest_count_for_beta is :")
        print(avg_prv_guest_count_for_beta.values())
        print(">>>>DEBUG>>>> avg_prvprv_guest_count_for_beta is :")
        print(avg_prvprv_guest_count_for_beta.values())
        print(">>>>DEBUG>>>> avg_beta is :")
        print(avg_beta)
        print(">>>>DEBUG>>>> trg_diff_total_listing_for_volatility is :")
        print(trg_diff_total_listing_for_volatility)
        print(">>>>DEBUG>>>> avg_diff_total_listing_for_volatility is :")
        print(avg_diff_total_listing_for_volatility)
        print(">>>>DEBUG>>>> stability is :")
        print(stability)
        '''


        # 4.競争率(競争相手の数)
        # 4.1.リスティング数
        # 4.1.1.対象都道府県のリスティング数
        #trg_total_listing_for_competition = region_sum_info.filter(year=today.year).filter(month=today.month).get(region_id=self.kwargs['region_city_id']).total_listing
        #trg_total_listing_for_competition = RegionSummary.objects.all().filter(year=today.year).filter(month=today.month).get(region_id=self.kwargs['region_city_id']).total_listing
        trg_total_listing_for_competition = 0
        # 4.1.2.平均リスティング数
        #avg_total_listing_for_competition = region_sum_info.filter(year=today.year).filter(month=today.month).aggregate(Avg('total_listing'))["total_listing__avg"]
        #avg_total_listing_for_competition = RegionSummary.objects.all().filter(year=today.year).filter(month=today.month).filter(region_id__lte=47).aggregate(Avg('total_listing'))["total_listing__avg"]
        avg_total_listing_for_competition = 0

        # 4.2.停止中リスティング数
        # 4.2.1.対象都道府県の停止中リスティング数
        #trg_suspend_count_for_competition = region_sum_info.filter(year=today.year).filter(month=today.month).get(region_id=self.kwargs['region_city_id']).suspend_count
        #trg_suspend_count_for_competition = RegionSummary.objects.all().filter(year=today.year).filter(month=today.month).get(region_id=self.kwargs['region_city_id']).suspend_count
        trg_suspend_count_for_competition = 0
        # 4.2.2.平均停止中リスティング数
        #avg_suspend_count_for_competition = region_sum_info.filter(year=today.year).filter(month=today.month).aggregate(Avg('suspend_count'))["suspend_count__avg"]
        #avg_suspend_count_for_competition = RegionSummary.objects.all().filter(year=today.year).filter(month=today.month).filter(region_id__lte=47).aggregate(Avg('suspend_count'))["suspend_count__avg"]
        avg_suspend_count_for_competition = 0

        # 4.3.webサイト数
        # 4.3.1.対象都道府県のwebサイト数
        #trg_website_count = annualsummary_info.filter(year=today.year-1).get(region_id=self.kwargs['region_id']).website_count
        #trg_website_count = AnnualSummary.objects.all().filter(year=today.year-1).get(region_id=self.kwargs['region_id']).website_count
        trg_website_count = 0
        # 4.3.2.平均webサイト数
        #avg_website_count = annualsummary_info.filter(year=today.year-1).aggregate(Avg('website_count'))['website_count__avg']
        #avg_website_count = AnnualSummary.objects.all().filter(year=today.year-1).aggregate(Avg('website_count'))['website_count__avg']
        avg_website_count = 0

        # 4.4.競争率
        #competition = round(5 - individual_rating(trg_total_listing_for_competition, avg_total_listing_for_competition, trg_suspend_count_for_competition, avg_suspend_count_for_competition, trg_website_count, avg_website_count), 2)
        competition = 2

        '''DEBUG用
        print(">>>>DEBUG>>>> trg_total_listing_for_competition is :")
        print(trg_total_listing_for_competition)
        print(">>>>DEBUG>>>> avg_total_listing_for_competition is :")
        print(avg_total_listing_for_competition)
        print(">>>>DEBUG>>>> trg_suspend_count_for_competition is :")
        print(trg_suspend_count_for_competition)
        print(">>>>DEBUG>>>> avg_suspend_count_for_competition is :")
        print(avg_suspend_count_for_competition)
        print(">>>>DEBUG>>>> trg_website_count is :")
        print(trg_website_count)
        print(">>>>DEBUG>>>> avg_website_count is :")
        print(avg_website_count)
        print(">>>>DEBUG>>>> competition is :")
        print(competition)
        '''


        # 5.価格（物件購入に必要な費用）
        # 5.1.公示価格
        # 5.1.1公示価格（対象都道府県分）
        #trg_priceofland = priceofland_info.filter(region_id=self.kwargs['region_city_id']).aggregate(Avg('avg_price'))["avg_price__avg"]
        trg_priceofland = PriceofLand.objects.all().filter(region_id=self.kwargs['region_id']).aggregate(Avg('avg_price'))["avg_price__avg"]
        #trg_priceofland_bkup = priceofland_info.filter(region_id=self.kwargs['region_id']).aggregate(Avg('avg_price'))["avg_price__avg"]
        trg_priceofland_bkup = PriceofLand.objects.all().filter(region_id=self.kwargs['region_id']).aggregate(Avg('avg_price'))["avg_price__avg"]
        # 対象市区町村の地価が存在しない場合、都道府県の地価を代用する
        '''DEBUG用
        print(">>>>DEBUG>>>> trg_priceofland is #1:")
        print(trg_priceofland)
        '''

        if trg_priceofland is None:
            print(">>>>DEBUG>>>> USE ALTER PriceofLand!!")
            trg_priceofland = trg_priceofland_bkup
        else:
            pass

        '''DEBUG用
        print(">>>>DEBUG>>>> trg_priceofland is #1:")
        print(trg_priceofland)
        '''
        # 5.1.2.公示価格（平均）
        #avg_priceofland = priceofland_info.aggregate(Avg('avg_price'))["avg_price__avg"]
        avg_priceofland = PriceofLand.objects.all().filter(region_id__lte=47).aggregate(Avg('avg_price'))["avg_price__avg"]

        '''DEBUG用
        print(">>>>DEBUG>>>> avg_priceofland is #1:")
        print(avg_priceofland)
        '''

        # 5.2.家賃
        # Cost（全地域分）
        cost_info = Cost.objects.select_related().all()
        # 5.2.1.家賃（対象地域）
        trg_rent = cost_info.filter(prefecture_code=self.kwargs['region_id'], year=today.year-1, month=today.month-1).aggregate(Avg('rent'))['rent__avg']

        # 5.2.2.家賃（平均）
        avg_rent = cost_info.filter(year=today.year-1, month=today.month-1).aggregate(Avg('rent'))['rent__avg']

        # 5.3.リフォーム費用
        # 5.3.1.リフォーム費用（対象地域）
        trg_restroom_facility_cost = cost_info.filter(region_id=self.kwargs['region_id'], year=today.year-1, month=today.month-1).aggregate(Avg('restroom_facility_cost'))['restroom_facility_cost__avg']
        trg_restroom_facility_cost = cost_info.filter(prefecture_code=self.kwargs['region_id'],year=today.year-1, month=today.month-1).aggregate(Avg('restroom_facility_cost'))['restroom_facility_cost__avg']
        trg_bathroom_facility_cost = cost_info.filter(prefecture_code=self.kwargs['region_id'],year=today.year-1, month=today.month-1).aggregate(Avg('bathroom_facility_cost'))['bathroom_facility_cost__avg']
        trg_kitchen_facility_cost = cost_info.filter(prefecture_code=self.kwargs['region_id'],year=today.year-1, month=today.month-1).aggregate(Avg('kitchen_facility_cost'))['kitchen_facility_cost__avg']
        trg_reform_fee = cost_info.filter(prefecture_code=self.kwargs['region_id'],year=today.year-1, month=today.month-1).aggregate(Avg('reform_fee'))['reform_fee__avg']
        trg_repainting_fee = cost_info.filter(prefecture_code=self.kwargs['region_id'],year=today.year-1, month=today.month-1).aggregate(Avg('repainting_fee'))['repainting_fee__avg']
        trg_sum_reform_cost = trg_restroom_facility_cost + trg_bathroom_facility_cost + trg_kitchen_facility_cost + trg_reform_fee + trg_repainting_fee

        #5.3.2.リフォーム費用（平均）
        avg_restroom_facility_cost = cost_info.filter(year=today.year-1, month=today.month-1).aggregate(Avg('restroom_facility_cost'))['restroom_facility_cost__avg']
        avg_bathroom_facility_cost = cost_info.filter(year=today.year-1, month=today.month-1).aggregate(Avg('bathroom_facility_cost'))['bathroom_facility_cost__avg']
        avg_kitchen_facility_cost = cost_info.filter(year=today.year-1, month=today.month-1).aggregate(Avg('kitchen_facility_cost'))['kitchen_facility_cost__avg']
        avg_reform_fee = cost_info.filter(year=today.year-1, month=today.month-1).aggregate(Avg('reform_fee'))['reform_fee__avg']
        avg_repainting_fee = cost_info.filter(year=today.year-1, month=today.month-1).aggregate(Avg('repainting_fee'))['repainting_fee__avg']
        avg_sum_reform_cost = avg_restroom_facility_cost + avg_bathroom_facility_cost + avg_kitchen_facility_cost + avg_reform_fee + avg_repainting_fee

        #5.4 価格（Phase1は公示価格のみで計算する）
        cost = round(5 - individual_rating(trg_priceofland, avg_priceofland, trg_rent, avg_rent, trg_sum_reform_cost, avg_sum_reform_cost), 2)

        '''DEBUG用'''
        print(">>>>DEBUG>>>> trg_priceofland is :")
        print(trg_priceofland)
        print(">>>>DEBUG>>>> avg_priceofland is :")
        print(avg_priceofland)
        print(">>>>DEBUG>>>> trg_rent is :")
        print(trg_rent)
        print(">>>>DEBUG>>>> avg_rent is :")
        print(avg_rent)
        print(">>>>DEBUG>>>> trg_sum_reform_cost is :")
        print(trg_sum_reform_cost)
        print(">>>>DEBUG>>>> avg_sum_reform_cost is :")
        print(avg_sum_reform_cost)
        print(">>>>DEBUG>>>> cost is :")
        print(cost)
        ''''''


        # 6.リターン（予想収益）
        # 6.1.月次売上
        # 6.1.1.売上（対象都道府県）
        #trg_monthly_sales_for_return = trg_monthly_sales
        trg_monthly_sales_for_return = 1
        # 6.1.2.公示価格（対象都道府県）
        #trg_priceofland_for_return = trg_priceofland
        trg_priceofland_for_return = 1
        # 6.1.3.コスパ（対象都道府県）
        trg_performance = trg_monthly_sales_for_return / trg_priceofland_for_return
        # 6.1.4.売上（平均）
        avg_monthly_sales_for_return = avg_monthly_sales
        # 6.1.5.公示価格（平均）
        avg_priceofland_for_return = avg_priceofland
        # 6.1.6.コスパ（対象都道府県）
        avg_performance = avg_monthly_sales_for_return / avg_priceofland_for_return

        # 6.2.リターン
        #ex_return = round(elemental_rating(trg_performance, avg_performance), 2)
        ex_return = 2

        # 7.総合レーティング
        general_rating = round((marketsize + potential + cost) / 3, 2)
        # marketsizeが小さいと特別減算
        if marketsize < 1:
            general_rating -= 1
        else:
            pass

        # 星レーティング用の数値
        general_rating_for_star = general_rating * 25

        '''DEBUG
        print(">>>>DEBUG>>>> marketsize is :")
        print(marketsize)
        print(">>>>DEBUG>>>> potential is :")
        print(potential)
        print(">>>>DEBUG>>>> cost is :")
        print(cost)
        print(">>>>DEBUG>>>> general_rating is :")
        print(general_rating)
        '''

        # 8.付加価値情報（ゲストの国籍）
        #trg_guestnationality_info = guestnationality_info.filter(prefecture_code=self.kwargs['region_id'])
        trg_guestnationality_info = GuestNationality.objects.all().filter(prefecture_code=self.kwargs['region_id']).order_by('-answer_count')
        # 9.付加価値情報（リスティングチャート）
        listing_legend = RegionSummary.objects.all().filter(prefecture_code=self.kwargs['region_id'], city_code__isnull=True).order_by('-year', '-month')[:12]
        # 10.付加価値情報（ゲスト数チャート）
        guest_legend = ForeignGuestCount.objects.all().filter(region_id=self.kwargs['region_id']).order_by('-year', '-month')[:12]
        # 11.付加価値情報（ランキング情報）
        ranking_info = Ranking.objects.all().get(region_id=self.kwargs['region_id'])
        # 12.付加価値情報（利回り情報）
        # 12.1清掃費（単価5000円、宿泊1組あたり2人の前提）
        cleaning_fee = trg_region_sum_info.monthly_sales / (trg_region_sum_info.average_price * 3) * 5000
        # 12.2運営費（売上の20%の前提）
        operation_fee = trg_region_sum_info.monthly_sales * 0.2
        # 12.3建物代（築20年以上でゼロ円の前提）
        property_price = 0
        # 12.4家賃（延べ床面積63平米の前提）
        average_rent = trg_rent / 3.3 * 63

        '''DEBUG用'''
        print(">>>>DEBUG>>>> listing_legend is :")
        print(listing_legend.values())
        print(">>>>DEBUG>>>> listing_legend_I is :")
        print(listing_legend[0].total_listing)
        print(">>>>DEBUG>>>> trg_guestnationality_info is :")
        print(trg_guestnationality_info.values())
        print(">>>>DEBUG>>>> ranking_info is :")
        print(ranking_info)
        ''''''


        context = {
            'trg_region_sum_info': trg_region_sum_info,
            #'region_info': region_info,
            #'trg_sum_articlebd_info': trg_sum_articlebd_info,
            'marketsize': marketsize,
            'trg_diff_guest_count': trg_diff_guest_count,
            'potential': potential,
            #'stability': stability,
            #'competition': competition,
            'trg_priceofland': round(trg_priceofland,0),
            #'cost': cost,
            #'ex_return': ex_return,
            'general_rating': general_rating,
            'general_rating_for_star': general_rating_for_star,
            'trg_guest_count': trg_guest_count,
            'trg_guestnationality_info': trg_guestnationality_info,
            'trg_diff_guest_count': trg_diff_guest_count,
            #'trg_stdev': trg_stdev,
            'listing_legend_I': listing_legend[11],
            'listing_legend_II': listing_legend[10],
            'listing_legend_III': listing_legend[9],
            'listing_legend_IV': listing_legend[8],
            'listing_legend_V': listing_legend[7],
            'listing_legend_VI': listing_legend[6],
            'listing_legend_VII': listing_legend[5],
            'listing_legend_VIII': listing_legend[4],
            'listing_legend_IX': listing_legend[3],
            'listing_legend_X': listing_legend[2],
            'listing_legend_XI': listing_legend[1],
            'listing_legend_XII': listing_legend[0],
            'trg_guestnationality_info_I': trg_guestnationality_info[0],
            'trg_guestnationality_info_II': trg_guestnationality_info[1],
            'trg_guestnationality_info_III': trg_guestnationality_info[2],
            'trg_guestnationality_info_IV': trg_guestnationality_info[3],
            'trg_guestnationality_info_V': trg_guestnationality_info[4],
            'trg_guestnationality_info_VI': trg_guestnationality_info[5],
            'trg_guestnationality_info_VII': trg_guestnationality_info[6],
            'guest_legend_I': guest_legend[11],
            'guest_legend_II': guest_legend[10],
            'guest_legend_III': guest_legend[9],
            'guest_legend_IV': guest_legend[8],
            'guest_legend_V': guest_legend[7],
            'guest_legend_VI': guest_legend[6],
            'guest_legend_VII': guest_legend[5],
            'guest_legend_VIII': guest_legend[4],
            'guest_legend_IX': guest_legend[3],
            'guest_legend_X': guest_legend[2],
            'guest_legend_XI': guest_legend[1],
            'guest_legend_XII': guest_legend[0],
            'ranking_info': ranking_info,
            'trg_rent': round(trg_rent/3.3,0),
            'trg_restroom_facility_cost': trg_restroom_facility_cost,
            'trg_bathroom_facility_cost': trg_bathroom_facility_cost,
            'trg_kitchen_facility_cost':trg_kitchen_facility_cost,
            'trg_reform_fee': trg_reform_fee,
            'trg_repainting_fee': trg_repainting_fee,
            'roi1': round((trg_region_sum_info.monthly_sales - cleaning_fee - operation_fee - average_rent) * 100 / average_rent, 2), # 転貸した場合の利回り
            'roi2': round((trg_region_sum_info.monthly_sales - cleaning_fee - operation_fee) / (trg_priceofland * 1.1), 2), # 購入した場合の利回り
        }
        return self.render_to_response(context)


class CityShowView(TemplateView):
    '''市区町村の詳細'''
    template_name = "city_show.html"

    def get(self, request, **kwargs):
        ''' objects.getコマンド ----> オブジェクトを返す
            objects.filterコマンド ----> クエリセットを返す
            外部キーの逆引きはオブジェクトにしか使えないので注意
        '''
        # ミクロ情報の取得1
        # RegionSummaryの最新レコード（全都道府県分）
        #region_sum_info = RegionSummary.objects.select_related().all()
        # SummaryArticleBreakdownの最新レコード（全都道府県分）
        #sum_articlebd_info = SummaryArticleBreakdown.objects.select_related().all()
        # SummaryCapacityBreakdownの最新レコード（全都道府県分）
        #sum_capacitybd_info = SummaryCapacityBreakdown.objects.select_related().all()
        # SummaryLanguageBreakdownの最新レコード（全都道府県分）
        #sum_languagebd_info = SummaryLanguageBreakdown.objects.select_related().all()
        # SummarySizeBreakdownの最新レコード（全都道府県分）
        #sum_sizebd_info = SummarySizeBreakdown.objects.select_related().all()

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
        try:
            trg_region_sum_info = RegionSummary.objects.select_related().all().get(region_id=self.kwargs['region_city_id'], year=today.year, month=today.month)
        except RegionSummary.DoesNotExist:
            raise Http404("No MyModel matches the given query.")
        # SummaryArticleBreakdownの対象レコード
        #trg_sum_articlebd_info = trg_region_sum_info.article_breakdown
        # SummaryCapacityBreakdownの対象レコード
        #trg_sum_capacitybd_info = trg_region_sum_info.capacity_breakdown
        # SummaryLanguageBreakdownの対象レコード
        #trg_sum_languagebd_info = trg_region_sum_info.language_breakdown
        # SummarySizeBreakdownの対象レコード
        #trg_sum_sizebd_info = trg_region_sum_info.size_breakdown

        '''DEBUG用
        print(">>>>DEBUG>>>> trg_region_sum_info is :")
        print(trg_region_sum_info.average_price)
        print(">>>>DEBUG>>>> trg_sum_articledb_info is :")
        print(trg_sum_articlebd_info.values())
        print(">>>>DEBUG>>>> trg_sum_languagebd_info is :")
        print(trg_sum_languagebd_info.values())
        print(">>>>DEBUG>>>> trg_sum_sizebd_info is :")
        print(trg_sum_sizebd_info.values())
        '''


        # マクロ情報
        # Prefecture
        region_info = Region.objects.select_related().all().get(id=self.kwargs['region_city_id'])
        # PriceofLand（全地域分）
        #priceofland_info = PriceofLand.objects.select_related().all()
        # TourResource（全地域分）
        #tourresource_info = TourResource.objects.select_related().all()
        # ForeignGuestCount（全地域分）
        #foreignguest_info = ForeignGuestCount.objects.select_related().all()
        # AnnualSummary（全地域分）
        #annualsummary_info = AnnualSummary.objects.select_related().all()
        # GuestNationality（全地域分）
        #guestnationality_info = GuestNationality.objects.select_related().all()

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

        # 1.市場規模(訪問客の数)の計算
        # 1.1.観光客数(昨年度)
        # 1.1.1.対象都道府県単体の観光客数
        #trg_guest_count = foreignguest_info.filter(year=today.year-1).filter(region_id=self.kwargs['region_id']).aggregate(Avg('guest_count'))["guest_count__avg"]
        #trg_guest_count = ForeignGuestCount.objects.all().filter(year=today.year-1).filter(region_id=self.kwargs['region_id']).aggregate(Avg('guest_count'))["guest_count__avg"]
        trg_guest_count = 0
        # 1.1.2.平均観光客数(全都道府県)
        #avg_guest_count = foreignguest_info.filter(year=today.year-1).aggregate(Avg('guest_count'))["guest_count__avg"]
        #avg_guest_count = ForeignGuestCount.objects.all().filter(year=today.year-1).filter(region_id__lte=47).aggregate(Avg('guest_count'))["guest_count__avg"]
        avg_guest_count = 0

        # 1.2.消費金額(昨年度)
        # 1.2.1.対象都道府県単体の消費金額
        #trg_consumption_amount = annualsummary_info.filter(year=today.year-1).get(region_id=self.kwargs['region_id']).consumption_ammount
        #trg_consumption_amount = AnnualSummary.objects.all().filter(year=today.year-1).get(region_id=self.kwargs['region_id']).consumption_ammount
        trg_consumption_amount = 0
        # 1.2.2.平均消費金額(全都道府県)
        #avg_consumption_amount = annualsummary_info.filter(year=today.year-1).aggregate(Avg('consumption_ammount'))["consumption_ammount__avg"]
        #avg_consumption_amount = AnnualSummary.objects.all().filter(year=today.year-1).filter(region_id__lte=47).aggregate(Avg('consumption_ammount'))["consumption_ammount__avg"]
        avg_consumption_amount = 0

        # 1.3.民泊売上(最新月)
        # 1.3.1.対象都道府県単体の売上
        trg_monthly_sales = trg_region_sum_info.monthly_sales
        # 1.3.2.平均売上
        #avg_monthly_sales = region_sum_info.aggregate(Avg('monthly_sales'))["monthly_sales__avg"]
        avg_monthly_sales = RegionSummary.objects.all().filter(year__gte=2017).filter(month__gte=10).filter(city_code__isnull=True).aggregate(Avg('monthly_sales'))["monthly_sales__avg"]

        # 1.4.市場規模レーティング
        #marketsize = round(individual_rating(trg_guest_count, avg_guest_count, trg_consumption_amount, avg_consumption_amount, trg_monthly_sales, avg_monthly_sales), 2)
        marketsize = round(elemental_rating(trg_monthly_sales, avg_monthly_sales))

        '''DEBUG用
        print(">>>>DEBUG>>>> trg_guest_count is :")
        print(trg_guest_count)
        print(">>>>DEBUG>>>> avg_guest_count is :")
        print(avg_guest_count)
        print(">>>>DEBUG>>>> trg_consumption is :")
        print(trg_consumption_amount)
        print(">>>>DEBUG>>>> avg_consumption_amount is :")
        print(avg_consumption_amount)
        print(">>>>DEBUG>>>> trg_monthly_sales is :")
        print(trg_monthly_sales)
        print(">>>>DEBUG>>>> avg_monthly_sales is :")
        print(avg_monthly_sales)
        print(">>>>DEBUG>>>> marketsize is :")
        print(marketsize)
        '''


        # 2.将来性（将来の見込み売上）の計算
        # 2.1.観光客変化率(trg_guest_count - prv_guest_count)
        # 2.1.1.観光客数の変化率（対象都道府県分）
        # 2.1.1.1当年分
        #trg_guest_count = foreignguest_info.filter(year=today.year-1).filter(month=today.month).get(region_id=self.kwargs['region_id']).guest_count
        trg_guest_count = ForeignGuestCount.objects.all().filter(year=today.year-1).filter(month=today.month).get(region_id=self.kwargs['region_id']).guest_count
        # 2.1.1.2前年分
        #prv_guest_count = foreignguest_info.filter(year=today.year-2).filter(month=today.month).get(region_id=self.kwargs['region_id']).guest_count
        prv_guest_count = ForeignGuestCount.objects.all().filter(year=today.year-2).filter(month=today.month).get(region_id=self.kwargs['region_id']).guest_count
        # 2.1.1.3.差分
        trg_diff_guest_count = trg_guest_count - prv_guest_count
        # 2.1.2.観光客変化率の平均値
        # 2.1.2.1.当年分
        #avg_trg_guest_count = foreignguest_info.filter(year=today.year-1).filter(month=today.month).aggregate(Avg('guest_count'))["guest_count__avg"]
        avg_trg_guest_count = ForeignGuestCount.objects.all().filter(year=today.year-1).filter(month=today.month).filter(region_id__lte=47).aggregate(Avg('guest_count'))["guest_count__avg"]
        # 2.1.2.2.前年分
        #avg_prv_guest_count = foreignguest_info.filter(year=today.year-2).filter(month=today.month).aggregate(Avg('guest_count'))["guest_count__avg"]
        avg_prv_guest_count = ForeignGuestCount.objects.all().filter(year=today.year-2).filter(month=today.month).filter(region_id__lte=47).aggregate(Avg('guest_count'))["guest_count__avg"]
        # 2.1.2.3.差分
        avg_diff_guest_count = avg_trg_guest_count - avg_prv_guest_count

        # 2.2.観光資源のスコア
        # 2.2.1.対象地域のスコア
        #trg_tourresource_score = tourresource_info.filter(region_id=self.kwargs['region_id']).aggregate(Avg('scr_score'))["scr_score__avg"]
        #trg_tourresource_score = TourResource.objects.all().filter(region_id=self.kwargs['region_id']).aggregate(Avg('scr_score'))["scr_score__avg"]
        trg_tourresource_score = 0
        # 2.2.2.平均スコア(全都道府県)
        #avg_tourresource_score = tourresource_info.aggregate(Avg('scr_score'))["scr_score__avg"]
        #avg_tourresource_score = TourResource.objects.all().aggregate(Avg('scr_score'))["scr_score__avg"]
        avg_tourresource_score = 0

        # 2.3.リスティング数の変化率(Phase1では対象外)
        # 2.3.1.リスティング数の変化率（対象都道府県分）
        # 2.3.1.1.当月分
        #trg_total_listing = region_sum_info.filter(year=today.year).filter(month=today.month).get(region_id=self.kwargs['region_id']).total_listing
        # 2.3.1.2.前月分
        #prv_total_listing = region_sum_info.filter(year=today.year).filter(month=today.month-1).get(region_id=self.kwargs['region_id']).total_listing
        # 2.3.1.3.差分
        #trg_diff_total_listing = trg_total_listing - prv_total_listing
        trg_diff_total_listing = 0
        # 2.3.2.リスティング数の変化率の平均値
        # 2.3.2.1.当月分
        #avg_trg_total_listing = region_sum_info.filter(year=today.year).filter(month=today.month).aggregate(Avg('total_listing'))["total_listing__avg"]
        # 2.3.2.2.前月分
        #avg_prv_total_listing = region_sum_info.filter(year=today.year).filter(month=today.month-1).aggregate(Avg('total_listing'))["total_listing__avg"]
        # 2.3.2.3.差分
        #avg_diff_total_listing = avg_trg_total_listing - avg_prv_total_listing
        avg_diff_total_listing = 0

        # 2.4.将来性
        potential = round(individual_rating(trg_diff_guest_count, avg_diff_guest_count, trg_tourresource_score, avg_tourresource_score, trg_diff_total_listing, avg_diff_total_listing), 2)

        '''DEBUG用
        print(">>>>DEBUG>>>> trg_guest_count is :")
        print(trg_guest_count)
        print(">>>>DEBUG>>>> prv_guest_count is :")
        print(prv_guest_count)
        print(">>>>DEBUG>>>> trg_diff_guest_count is :")
        print(trg_diff_guest_count)
        print(">>>>DEBUG>>>> avg_trg_guest_count is :")
        print(avg_trg_guest_count)
        print(">>>>DEBUG>>>> avg_prv_guest_count is :")
        print(avg_prv_guest_count)
        print(">>>>DEBUG>>>> avg_diff_guest_cont is :")
        print(avg_diff_guest_count)
        print(">>>>DEBUG>>>> trg_tourresource_score is :")
        print(trg_tourresource_score)
        print(">>>>DEBUG>>>> avg_tourresource_score is :")
        print(avg_tourresource_score)
        #print(">>>>DEBUG>>>> trg_total_listing is :")
        #print(trg_total_listing)
        #print(">>>>DEBUG>>>> prv_total_listing is :")
        #print(prv_total_listing)
        print(">>>>DEBUG>>>> trg_diff_total_listing is :")
        print(trg_diff_total_listing)
        #print(">>>>DEBUG>>>> avg_trg_total_listing is :")
        #print(avg_trg_total_listing)
        #print(">>>>DEBUG>>>> avg_prv_total_listing is :")
        #print(avg_prv_total_listing)
        print(">>>>DEBUG>>>> avg_diff_total_listing is :")
        print(avg_diff_total_listing)
        print(">>>>DEBUG>>>> potential is :")
        print(potential)
        '''


        # 3.安定性(季節ごとの売上変動)
        # 3.1.観光客ボラティリティ
        # 3.1.1.観光客ボラティリティ（対象都道府県分）
        # 3.1.1.1.当月観光客数
        #trg_guest_count_for_volatility = foreignguest_info.filter(region_id=self.kwargs['region_id']).order_by('-id')[:12]
        trg_guest_count_for_volatility = ForeignGuestCount.objects.all().filter(region_id=self.kwargs['region_id']).order_by('-id')[:12]
        #trg_guest_count_for_volatility = 0
        # 3.1.1.2.前月観光客数
        #prv_guest_count_for_volatility = foreignguest_info.filter(region_id=self.kwargs['region_id']).order_by('-id')[1:13]
        prv_guest_count_for_volatility = ForeignGuestCount.objects.all().filter(region_id=self.kwargs['region_id']).order_by('-id')[1:13]
        #prv_guest_count_for_volatility = 0
        # 3.1.1.3.標準偏差
        trg_stdev = cal_stdev(trg_guest_count_for_volatility, prv_guest_count_for_volatility)
        #trg_stdev = 1
        # 3.1.2.観光客ボラティリティ（モデル都道府県分）
        # 3.1.2.1.モデル都道府県の当月平均観光客数
        #avg_guest_count_for_volatility = foreignguest_info.filter(region_id=22).order_by('-id')[:12]
        #avg_guest_count_for_volatility = ForeignGuestCount.objects.all().filter(region_id=22).order_by('-id')[:12]
        avg_guest_count_for_volatility = 0
        # 3.1.2.2.モデル都道府県の前月平均観光客数
        #avg_prv_guest_count_for_volatility = foreignguest_info.filter(region_id=22).order_by('-id')[1:13]
        #avg_prv_guest_count_for_volatility = ForeignGuestCount.objects.all().filter(region_id=22).order_by('-id')[1:13]
        avg_prv_guest_count_for_volatility = 0
        # 3.1.2.3.標準偏差
        #avg_stdev = cal_stdev(avg_guest_count_for_volatility, avg_prv_guest_count_for_volatility)
        avg_stdev = 1

        # 3.2.観光客の変化率の変化率（ベータ）
        # 3.2.1.観光客のベータ（対象都道府県分）
        # 3.2.1.1.当月観光客数
        trg_guest_count_for_beta = trg_guest_count_for_volatility
        # 3.2.1.2.前月観光客数
        prv_guest_count_for_beta = prv_guest_count_for_volatility
        # 3.2.1.3.前々月観光客数
        #prvprv_guest_count_for_beta = foreignguest_info.filter(region_id=self.kwargs['region_id']).order_by('-id')[2:14]
        #prvprv_guest_count_for_beta = ForeignGuestCount.objects.all().filter(region_id=self.kwargs['region_id']).order_by('-id')[2:14]
        prvprv_guest_count_for_beta = 0
        # 3.2.1.4.ベータ
        #trg_beta = cal_beta(trg_guest_count_for_beta, prv_guest_count_for_beta, prvprv_guest_count_for_beta)
        trg_beta = 1
        # 3.2.2.観光客のベータ（対象都道府県分）
        # 3.2.2.1.モデル都道府県の当月観光客数
        avg_guest_count_for_beta = avg_guest_count_for_volatility
        # 3.2.2.2.モデル都道府県の前月観光客数
        avg_prv_guest_count_for_beta = avg_prv_guest_count_for_volatility
        # 3.2.2.3.モデル都道府県の前々月観光客数
        #avg_prvprv_guest_count_for_beta = foreignguest_info.filter(region_id=22).order_by('-id')[2:14]
        #avg_prvprv_guest_count_for_beta = ForeignGuestCount.objects.all().filter(region_id=22).order_by('-id')[2:14]
        avg_prvprv_guest_count_for_beta = 0
        # 3.2.2.4.モデル都道府県のベータ
        #avg_beta = cal_beta(avg_guest_count_for_beta, avg_prv_guest_count_for_beta, avg_prvprv_guest_count_for_beta)
        avg_beta = 1

        # 3.3.リスティング数の変化率(Phase1では対象外)
        # 3.3.1.リスティング数の変化率(対象都道府県分)
        # 3.3.1.1.当月分
        #trg_total_listing = region_sum_info.filter(year=today.year).filter(month=today.month).get(region_id=self.kwargs['region_id']).total_listing
        # 3.3.1.2.前月分
        #prv_total_listing = region_sum_info.filter(year=today.year).filter(month=today.month-1).get(region_id=self.kwargs['region_id']).total_listing
        # 3.3.1.3.差分
        #trg_diff_total_listing = trg_total_listing - prv_total_listing
        trg_diff_total_listing_for_volatility = 0
        # 3.3.2.リスティング数の変化率の平均値
        # 3.3.2.1.当月分
        #avg_trg_total_listing = region_sum_info.filter(year=today.year).filter(month=today.month).aggregate(Avg('total_listing'))["total_listing__avg"]
        # 3.3.2.2.前月分
        #avg_prv_total_listing = region_sum_info.filter(year=today.year).filter(month=today.month-1).aggregate(Avg('total_listing'))["total_listing__avg"]
        # 3.3.2.3.差分
        #avg_diff_total_listing = avg_trg_total_listing - avg_prv_total_listing
        avg_diff_total_listing_for_volatility = 0

        # 3.4.安定性
        #stability = round(5 - individual_rating(trg_stdev, avg_stdev, trg_beta, avg_beta, trg_diff_total_listing_for_volatility, avg_diff_total_listing_for_volatility), 2)
        stability = 2

        '''DEBUG用
        print(">>>>DEBUG>>>> trg_guest_count_for_volatility is :")
        print(trg_guest_count_for_volatility.values())
        print(">>>>DEBUG>>>> prv_guest_count_for_volatility is :")
        print(prv_guest_count_for_volatility.values())
        print(">>>>DEBUG>>>> trg_stdev is :")
        print(trg_stdev)
        print(">>>>DEBUG>>>> avg_guest_count_for_volatility is :")
        print(avg_guest_count_for_volatility.values())
        print(">>>>DEBUG>>>> avg_prv_guest_count_for_volatility is :")
        print(avg_prv_guest_count_for_volatility.values())
        print(">>>>DEBUG>>>> avg_stdev is :")
        print(avg_stdev)
        print(">>>>DEBUG>>>> trg_guest_count_for_beta is :")
        print(trg_guest_count_for_beta.values())
        print(">>>>DEBUG>>>> prv_guest_count_for_beta is :")
        print(prv_guest_count_for_beta.values())
        print(">>>>DEBUG>>>> prvprv_guest_count_for_beta is :")
        print(prvprv_guest_count_for_beta.values())
        print(">>>>DEBUG>>>> trg_beta is :")
        print(trg_beta)
        print(">>>>DEBUG>>>> avg_guest_count_for_beta is :")
        print(avg_guest_count_for_beta.values())
        print(">>>>DEBUG>>>> avg_prv_guest_count_for_beta is :")
        print(avg_prv_guest_count_for_beta.values())
        print(">>>>DEBUG>>>> avg_prvprv_guest_count_for_beta is :")
        print(avg_prvprv_guest_count_for_beta.values())
        print(">>>>DEBUG>>>> avg_beta is :")
        print(avg_beta)
        print(">>>>DEBUG>>>> trg_diff_total_listing_for_volatility is :")
        print(trg_diff_total_listing_for_volatility)
        print(">>>>DEBUG>>>> avg_diff_total_listing_for_volatility is :")
        print(avg_diff_total_listing_for_volatility)
        print(">>>>DEBUG>>>> stability is :")
        print(stability)
        '''


        # 4.競争率(競争相手の数)
        # 4.1.リスティング数
        # 4.1.1.対象都道府県のリスティング数
        #trg_total_listing_for_competition = region_sum_info.filter(year=today.year).filter(month=today.month).get(region_id=self.kwargs['region_city_id']).total_listing
        #trg_total_listing_for_competition = RegionSummary.objects.all().filter(year=today.year).filter(month=today.month).get(region_id=self.kwargs['region_city_id']).total_listing
        trg_total_listing_for_competition = 0
        # 4.1.2.平均リスティング数
        #avg_total_listing_for_competition = region_sum_info.filter(year=today.year).filter(month=today.month).aggregate(Avg('total_listing'))["total_listing__avg"]
        #avg_total_listing_for_competition = RegionSummary.objects.all().filter(year=today.year).filter(month=today.month).filter(region_id__lte=47).aggregate(Avg('total_listing'))["total_listing__avg"]
        avg_total_listing_for_competition = 0

        # 4.2.停止中リスティング数
        # 4.2.1.対象都道府県の停止中リスティング数
        #trg_suspend_count_for_competition = region_sum_info.filter(year=today.year).filter(month=today.month).get(region_id=self.kwargs['region_city_id']).suspend_count
        #trg_suspend_count_for_competition = RegionSummary.objects.all().filter(year=today.year).filter(month=today.month).get(region_id=self.kwargs['region_city_id']).suspend_count
        trg_suspend_count_for_competition = 0
        # 4.2.2.平均停止中リスティング数
        #avg_suspend_count_for_competition = region_sum_info.filter(year=today.year).filter(month=today.month).aggregate(Avg('suspend_count'))["suspend_count__avg"]
        #avg_suspend_count_for_competition = RegionSummary.objects.all().filter(year=today.year).filter(month=today.month).filter(region_id__lte=47).aggregate(Avg('suspend_count'))["suspend_count__avg"]
        avg_suspend_count_for_competition = 0

        # 4.3.webサイト数
        # 4.3.1.対象都道府県のwebサイト数
        #trg_website_count = annualsummary_info.filter(year=today.year-1).get(region_id=self.kwargs['region_id']).website_count
        #trg_website_count = AnnualSummary.objects.all().filter(year=today.year-1).get(region_id=self.kwargs['region_id']).website_count
        trg_website_count = 0
        # 4.3.2.平均webサイト数
        #avg_website_count = annualsummary_info.filter(year=today.year-1).aggregate(Avg('website_count'))['website_count__avg']
        #avg_website_count = AnnualSummary.objects.all().filter(year=today.year-1).aggregate(Avg('website_count'))['website_count__avg']
        avg_website_count = 0

        # 4.4.競争率
        #competition = round(5 - individual_rating(trg_total_listing_for_competition, avg_total_listing_for_competition, trg_suspend_count_for_competition, avg_suspend_count_for_competition, trg_website_count, avg_website_count), 2)
        competition = 2

        '''DEBUG用
        print(">>>>DEBUG>>>> trg_total_listing_for_competition is :")
        print(trg_total_listing_for_competition)
        print(">>>>DEBUG>>>> avg_total_listing_for_competition is :")
        print(avg_total_listing_for_competition)
        print(">>>>DEBUG>>>> trg_suspend_count_for_competition is :")
        print(trg_suspend_count_for_competition)
        print(">>>>DEBUG>>>> avg_suspend_count_for_competition is :")
        print(avg_suspend_count_for_competition)
        print(">>>>DEBUG>>>> trg_website_count is :")
        print(trg_website_count)
        print(">>>>DEBUG>>>> avg_website_count is :")
        print(avg_website_count)
        print(">>>>DEBUG>>>> competition is :")
        print(competition)
        '''


        # 5.価格（物件購入に必要な費用）
        # 5.1.公示価格
        # 5.1.1公示価格（対象都道府県分）
        #trg_priceofland = priceofland_info.filter(region_id=self.kwargs['region_city_id']).aggregate(Avg('avg_price'))["avg_price__avg"]
        trg_priceofland = PriceofLand.objects.all().filter(region_id=self.kwargs['region_city_id']).aggregate(Avg('avg_price'))["avg_price__avg"]
        #trg_priceofland_bkup = priceofland_info.filter(region_id=self.kwargs['region_id']).aggregate(Avg('avg_price'))["avg_price__avg"]
        trg_priceofland_bkup = PriceofLand.objects.all().filter(region_id=self.kwargs['region_id']).aggregate(Avg('avg_price'))["avg_price__avg"]
        # 対象市区町村の地価が存在しない場合、都道府県の地価を代用する
        '''DEBUG用
        print(">>>>DEBUG>>>> trg_priceofland is #1:")
        print(trg_priceofland)
        '''

        if trg_priceofland is None:
            print(">>>>DEBUG>>>> USE ALTER PriceofLand!!")
            trg_priceofland = trg_priceofland_bkup
        else:
            pass

        '''DEBUG用
        print(">>>>DEBUG>>>> trg_priceofland is #1:")
        print(trg_priceofland)
        '''
        # 5.1.2.公示価格（平均）
        #avg_priceofland = priceofland_info.aggregate(Avg('avg_price'))["avg_price__avg"]
        avg_priceofland = PriceofLand.objects.all().filter(region_id__lte=47).aggregate(Avg('avg_price'))["avg_price__avg"]

        '''DEBUG用
        print(">>>>DEBUG>>>> avg_priceofland is #1:")
        print(avg_priceofland)
        '''

        # 5.2.家賃
        # Cost（全地域分）
        cost_info = Cost.objects.select_related().all()
        # 5.2.1.家賃（対象地域）
        trg_rent = cost_info.filter(region_id=self.kwargs['region_city_id'], year=today.year-1, month=today.month-1).aggregate(Avg('rent'))['rent__avg']
        # 対象地域の情報がなかった時の処理
        if trg_rent is None:
            print(">>>>DEBUG>>>> USE ALTER Rent!!")
            trg_rent = cost_info.filter(prefecture_code=self.kwargs['region_id'],year=today.year-1, month=today.month-1).aggregate(Avg('rent'))['rent__avg']
        else:
            pass

        # 5.2.2.家賃（平均）
        avg_rent = cost_info.filter(year=today.year-1, month=today.month-1).aggregate(Avg('rent'))['rent__avg']

        # 5.3.リフォーム費用
        # 5.3.1.リフォーム費用（対象地域）
        trg_restroom_facility_cost = cost_info.filter(region_id=self.kwargs['region_city_id'], year=today.year-1, month=today.month-1).aggregate(Avg('restroom_facility_cost'))['restroom_facility_cost__avg']
        # 対象地域の情報がなかった時の処理
        if trg_restroom_facility_cost is None:
            print(">>>>DEBUG>>>> USE ALTER Rent!!")
            # 都道府県の平均値で代用
            trg_restroom_facility_cost = cost_info.filter(prefecture_code=self.kwargs['region_id'],year=today.year-1, month=today.month-1).aggregate(Avg('restroom_facility_cost'))['restroom_facility_cost__avg']
            trg_bathroom_facility_cost = cost_info.filter(prefecture_code=self.kwargs['region_id'],year=today.year-1, month=today.month-1).aggregate(Avg('bathroom_facility_cost'))['bathroom_facility_cost__avg']
            trg_kitchen_facility_cost = cost_info.filter(prefecture_code=self.kwargs['region_id'],year=today.year-1, month=today.month-1).aggregate(Avg('kitchen_facility_cost'))['kitchen_facility_cost__avg']
            trg_reform_fee = cost_info.filter(prefecture_code=self.kwargs['region_id'],year=today.year-1, month=today.month-1).aggregate(Avg('reform_fee'))['reform_fee__avg']
            trg_repainting_fee = cost_info.filter(prefecture_code=self.kwargs['region_id'],year=today.year-1, month=today.month-1).aggregate(Avg('repainting_fee'))['repainting_fee__avg']
            trg_sum_reform_cost = trg_restroom_facility_cost + trg_bathroom_facility_cost + trg_kitchen_facility_cost + trg_reform_fee + trg_repainting_fee
        else:
            # そのまま計算を続行
            trg_bathroom_facility_cost = cost_info.filter(region_id=self.kwargs['region_city_id'], year=today.year-1, month=today.month-1).aggregate(Avg('bathroom_facility_cost'))['bathroom_facility_cost__avg']
            trg_kitchen_facility_cost = cost_info.filter(region_id=self.kwargs['region_city_id'], year=today.year-1, month=today.month-1).aggregate(Avg('kitchen_facility_cost'))['kitchen_facility_cost__avg']
            trg_reform_fee = cost_info.filter(region_id=self.kwargs['region_city_id'], year=today.year-1, month=today.month-1).aggregate(Avg('reform_fee'))['reform_fee__avg']
            trg_repainting_fee = cost_info.filter(region_id=self.kwargs['region_city_id'], year=today.year-1, month=today.month-1).aggregate(Avg('repainting_fee'))['repainting_fee__avg']
            trg_sum_reform_cost = trg_restroom_facility_cost + trg_bathroom_facility_cost + trg_kitchen_facility_cost + trg_reform_fee + trg_repainting_fee

        #5.3.2.リフォーム費用（平均）
        avg_restroom_facility_cost = cost_info.filter(year=today.year-1, month=today.month-1).aggregate(Avg('restroom_facility_cost'))['restroom_facility_cost__avg']
        avg_bathroom_facility_cost = cost_info.filter(year=today.year-1, month=today.month-1).aggregate(Avg('bathroom_facility_cost'))['bathroom_facility_cost__avg']
        avg_kitchen_facility_cost = cost_info.filter(year=today.year-1, month=today.month-1).aggregate(Avg('kitchen_facility_cost'))['kitchen_facility_cost__avg']
        avg_reform_fee = cost_info.filter(year=today.year-1, month=today.month-1).aggregate(Avg('reform_fee'))['reform_fee__avg']
        avg_repainting_fee = cost_info.filter(year=today.year-1, month=today.month-1).aggregate(Avg('repainting_fee'))['repainting_fee__avg']
        avg_sum_reform_cost = avg_restroom_facility_cost + avg_bathroom_facility_cost + avg_kitchen_facility_cost + avg_reform_fee + avg_repainting_fee

        #5.4 価格（Phase1は公示価格のみで計算する）
        cost = round(5 - individual_rating(trg_priceofland, avg_priceofland, trg_rent, avg_rent, trg_sum_reform_cost, avg_sum_reform_cost), 2)

        '''DEBUG用'''
        print(">>>>DEBUG>>>> trg_priceofland is :")
        print(trg_priceofland)
        print(">>>>DEBUG>>>> avg_priceofland is :")
        print(avg_priceofland)
        print(">>>>DEBUG>>>> trg_rent is :")
        print(trg_rent)
        print(">>>>DEBUG>>>> avg_rent is :")
        print(avg_rent)
        print(">>>>DEBUG>>>> trg_sum_reform_cost is :")
        print(trg_sum_reform_cost)
        print(">>>>DEBUG>>>> avg_sum_reform_cost is :")
        print(avg_sum_reform_cost)
        print(">>>>DEBUG>>>> cost is :")
        print(cost)
        ''''''


        # 6.リターン（予想収益）
        # 6.1.月次売上
        # 6.1.1.売上（対象都道府県）
        #trg_monthly_sales_for_return = trg_monthly_sales
        trg_monthly_sales_for_return = 1
        # 6.1.2.公示価格（対象都道府県）
        #trg_priceofland_for_return = trg_priceofland
        trg_priceofland_for_return = 1
        # 6.1.3.コスパ（対象都道府県）
        trg_performance = trg_monthly_sales_for_return / trg_priceofland_for_return
        # 6.1.4.売上（平均）
        avg_monthly_sales_for_return = avg_monthly_sales
        # 6.1.5.公示価格（平均）
        avg_priceofland_for_return = avg_priceofland
        # 6.1.6.コスパ（対象都道府県）
        avg_performance = avg_monthly_sales_for_return / avg_priceofland_for_return

        # 6.2.リターン
        #ex_return = round(elemental_rating(trg_performance, avg_performance), 2)
        ex_return = 2

        # 7.総合レーティング
        general_rating = round((marketsize + potential + cost) / 3, 2)
        # marketsizeが小さいと特別減算
        if marketsize < 1:
            general_rating -= 1
        else:
            pass

        # 星レーティング用の数値
        general_rating_for_star = general_rating * 25

        '''DEBUG
        print(">>>>DEBUG>>>> marketsize is :")
        print(marketsize)
        print(">>>>DEBUG>>>> potential is :")
        print(potential)
        print(">>>>DEBUG>>>> cost is :")
        print(cost)
        print(">>>>DEBUG>>>> general_rating is :")
        print(general_rating)
        '''

        # 8.付加価値情報（ゲストの国籍）
        #trg_guestnationality_info = guestnationality_info.filter(prefecture_code=self.kwargs['region_id'])
        trg_guestnationality_info = GuestNationality.objects.all().filter(prefecture_code=self.kwargs['region_id']).order_by('-answer_count')
        # 9.付加価値情報（リスティングチャート）
        listing_legend = RegionSummary.objects.all().filter(region_id=self.kwargs['region_city_id']).order_by('-year', '-month')[:12]
        # 10.付加価値情報（ゲスト数チャート）
        guest_legend = ForeignGuestCount.objects.all().filter(region_id=self.kwargs['region_id']).order_by('-year', '-month')[:12]
        # 11.付加価値情報（ランキング情報）
        try:
            ranking_info = Ranking.objects.all().filter(region_id=self.kwargs['region_city_id']).order_by('-created_at')
        except Ranking.DoesNotExist:
            raise Http404("No MyModel matches the given query.")

        # 12.付加価値情報（利回り情報）
        if trg_region_sum_info.monthly_sales <> 0:
            # 12.1清掃費（単価5000円、宿泊1組あたり2人の前提）
            cleaning_fee = trg_region_sum_info.monthly_sales / (trg_region_sum_info.average_price * 2.3) * 5000
            # 12.2運営費（売上の20%の前提）
            operation_fee = trg_region_sum_info.monthly_sales * 0.2
        else:
            cleaning_fee = 0
            operation_fee = 0

        # 12.3建物代（築20年以上でゼロ円の前提）
        property_price = 0
        # 12.4延べ床面積
        trg_total_floor_area = AnnualSummary.objects.all().get(prefecture_code=self.kwargs['region_id']).total_floor_area
        # 12.4家賃（延べ床面積63平米の前提）
        average_rent = trg_rent / 3.3 * int(trg_total_floor_area)
        # 12.5観光資源情報
        trg_tourresource = TourResource.objects.select_related().all().filter(prefecture_code=self.kwargs['region_id']).order_by('-scr_score')[:10]
        # 12.6部屋サイズ情報
        #trg_capacity_info = RegionSummary.objects.all().filter(capacity_breakdown__link_city_code=self.kwargs['region_city_id']).order_by('capacity_type')
        #trg_capacity_info = trg_region_sum_info.capacity_breakdown
        trg_capacity_info = SummaryCapacityBreakdown.objects.all().filter(region_summary__region_id=self.kwargs['region_city_id']).order_by('capacity_type','-created_at')[:4]

        '''DEBUG用'''
        print(">>>>DEBUG>>>> listing_legend is :")
        print(listing_legend.values())
        print(">>>>DEBUG>>>> listing_legend_I is :")
        print(listing_legend[0].total_listing)
        print(">>>>DEBUG>>>> trg_guestnationality_info is :")
        print(trg_guestnationality_info.values())
        print(">>>>DEBUG>>>> ranking_info is :")
        print(ranking_info)
        print(">>>>DEBUG>>>> trg_capacity_info is :")
        print(trg_capacity_info.values())
        ''''''


        context = {
            'trg_region_sum_info': trg_region_sum_info,
            #'region_info': region_info,
            #'trg_sum_articlebd_info': trg_sum_articlebd_info,
            'marketsize': marketsize,
            'trg_diff_guest_count': trg_diff_guest_count,
            'potential': potential,
            #'stability': stability,
            #'competition': competition,
            'trg_priceofland': round(trg_priceofland,0),
            #'cost': cost,
            #'ex_return': ex_return,
            'general_rating': general_rating,
            'general_rating_for_star': general_rating_for_star,
            'trg_guest_count': trg_guest_count,
            'trg_guestnationality_info': trg_guestnationality_info,
            'trg_diff_guest_count': trg_diff_guest_count,
            #'trg_stdev': trg_stdev,
            'listing_legend_I': listing_legend[11],
            'listing_legend_II': listing_legend[10],
            'listing_legend_III': listing_legend[9],
            'listing_legend_IV': listing_legend[8],
            'listing_legend_V': listing_legend[7],
            'listing_legend_VI': listing_legend[6],
            'listing_legend_VII': listing_legend[5],
            'listing_legend_VIII': listing_legend[4],
            'listing_legend_IX': listing_legend[3],
            'listing_legend_X': listing_legend[2],
            'listing_legend_XI': listing_legend[1],
            'listing_legend_XII': listing_legend[0],
            'trg_guestnationality_info_I': trg_guestnationality_info[0],
            'trg_guestnationality_info_II': trg_guestnationality_info[1],
            'trg_guestnationality_info_III': trg_guestnationality_info[2],
            'trg_guestnationality_info_IV': trg_guestnationality_info[3],
            'trg_guestnationality_info_V': trg_guestnationality_info[4],
            'trg_guestnationality_info_VI': trg_guestnationality_info[5],
            'trg_guestnationality_info_VII': trg_guestnationality_info[6],
            'guest_legend_I': guest_legend[11],
            'guest_legend_II': guest_legend[10],
            'guest_legend_III': guest_legend[9],
            'guest_legend_IV': guest_legend[8],
            'guest_legend_V': guest_legend[7],
            'guest_legend_VI': guest_legend[6],
            'guest_legend_VII': guest_legend[5],
            'guest_legend_VIII': guest_legend[4],
            'guest_legend_IX': guest_legend[3],
            'guest_legend_X': guest_legend[2],
            'guest_legend_XI': guest_legend[1],
            'guest_legend_XII': guest_legend[0],
            'ranking_info': ranking_info[0],
            'trg_rent': round(trg_rent / 3.3 * int(trg_total_floor_area),0),
            'trg_restroom_facility_cost': round(trg_restroom_facility_cost,0),
            'trg_bathroom_facility_cost': round(trg_bathroom_facility_cost,0),
            'trg_kitchen_facility_cost': round(trg_kitchen_facility_cost,0),
            'trg_reform_fee': round(trg_reform_fee / 3.3 * int(trg_total_floor_area),0),
            'trg_repainting_fee': round(trg_repainting_fee / 3.3 * int(trg_total_floor_area),0),
            'roi1': round((trg_region_sum_info.monthly_sales - cleaning_fee - operation_fee - average_rent) * 100 * 0.8/ average_rent, 2), # 転貸した場合の利回り
            'roi2': round((trg_region_sum_info.monthly_sales - cleaning_fee - operation_fee) * 100 * 0.8 / (trg_priceofland * int(trg_total_floor_area)), 2), # 購入した場合の利回り
            'trg_tourresource': trg_tourresource,
            'trg_capacity_info_I': trg_capacity_info[0],
            'trg_capacity_info_II': trg_capacity_info[1],
            'trg_capacity_info_III': trg_capacity_info[2],
            'trg_capacity_info_IV': trg_capacity_info[3],
            'ranking_last_month': int(ranking_info[0].created_at.month) - 1
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
