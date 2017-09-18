# -*- coding:utf-8 -*-
from django.views.generic import TemplateView

from django.http import Http404
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

import datetime

from .models import Pref_table, Company_table, Member_table, Air_table

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
        pref_id = int(request.GET.get('pf_id', None))
        print(">>>DEBUG>>> pf_id is: %d" % pref_id)
        Pref_info = Pref_table.objects.filter(pf_id=pref_id)
        Air_info = Air_table.objects.filter(pf_id=pref_id)
        context = {
            'Air_info': Air_info,
            'Pref_info': Pref_info,
        }
        return self.render_to_response(context)


class PrefectureView(TemplateView):
    '''prefテーブルより都道府県一覧を取得する'''
    template_name = "prefectures.html"

    def get(self, request, **kwargs):
        latest_pref_list = Pref_table.objects.order_by('pf_id')[0:47]
        context = {
            'latest_pref_list': latest_pref_list,
        }
        return self.render_to_response(context)


class PrefectureShowView(TemplateView):
    '''都道府県の詳細'''
    template_name = "prefecture_show.html"

    def get(self, request, **kwargs):
        prefecture = Pref_table.objects.get(pf_id=self.kwargs['prefecture_id'])
        context = {
            'prefecture': prefecture,
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
