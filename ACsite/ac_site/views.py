# -*- coding:utf-8 -*-
from django.http import Http404
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

import datetime

from .models import Pref_table, Company_table, Member_table


def index(request):
    # HttpResponse()
    # 使い方：
    # 文字列を渡す：webページに文字列を表示させる
    # イテレータ（=yield）を渡す：イテレータの内容を保持する
    # ヘッダーフィールドをつける：response = HttpResponse()
    #                        response[20] = 120 など

    company_info = Company_table.objects.order_by('-comp_id')[:1]
    member_info = Member_table.objects.order_by('member_id')[:1]
    context = {
        'company_info': company_info,
        'member_info': member_info,
    }
    # render(arg1, arg2, arg3)
    # arg1: requestオブジェクト
    # arg2: テンプレート名
    # arg3: オプション辞書（= DB変数と.pyの変数の紐付け）
    return render(request, 'ac_site/index.html', context)


def company(request):
    '''会社情報を取得する（静的）'''
    company_info = Company_table.objects.order_by('-comp_id')[:1]
    context = {
        'company_info': company_info,
    }
    return render(request, 'ac_site/company.html', context)


def contact(request):
    '''お問い合わせ時に表示する会社情報を取得する（静的）'''
    company_info = Company_table.objects.order_by('-comp_id')[:1]
    context = {
        'company_info': company_info,
    }
    return render(request, 'ac_site/contact.html', context)


#def login(request):
#    '''ログイン情報を取得する（静的）'''
#    context = 0 # 仮置きで変数を定義
#    return render(request, 'ac_site/login.html', context)


#def minnpaku_news(request):
#    '''民泊日記情報を取得する（静的）'''
#    context = 0 # 仮置きで変数を定義
#    return render(request, 'ac_site/minnpaku_news.html', context)


#def news_release(request):
#    '''ニュースリリース情報を取得する（静的）'''
#    context = 0 # 仮置きで変数を定義
#    return render(request, 'ac_site/news_release.html', context)


def prefs(request):
    '''prefテーブルより都道府県一覧を取得する'''
    latest_pref_list = Pref_table.objects.order_by('pf_id')[0:47]
    context = {
        'latest_pref_list': latest_pref_list,
    }
    return render(request, 'ac_site/prefs.html', context)


#def registration(request):
#    '''サインイン情報を取得する（静的）'''
#    context = 0 # 仮置きで変数を定義
#    return render(request, 'ac_site/registration.html', context)


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
