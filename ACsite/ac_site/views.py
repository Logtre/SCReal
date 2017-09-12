# -*- coding:utf-8 -*-
from django.http import Http404
from django.shortcuts import render
from django.http import HttpResponse
#from django.template import loader

import datetime

from .models import Pref_table


def index(request):
    # HttpResponse()
    # 使い方：
    # 文字列を渡す：webページに文字列を表示させる
    # イテレータ（=yield）を渡す：イテレータの内容を保持する
    # ヘッダーフィールドをつける：response = HttpResponse()
    #                        response[20] = 120 など

    latest_pref_list = Pref_table.objects.order_by('-pf_id')[:5]
    context = {
        'latest_pref_list': latest_pref_list,
    }
    # render(arg1, arg2, arg3)
    # arg1: requestオブジェクト
    # arg2: テンプレート名
    # arg3: オプション辞書（= DB変数と.pyの変数の紐付け）
    return render(request, 'ac_site/index.html', context)
    #latest_pref_list = Pref_table.objects.order_by('-pf_id')[:5]
    #output = ', '.join([q.pref for q in latest_pref_list])
    #return HttpResponse(output)
    #return HttpResponse("You're looking at question1 ")


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
