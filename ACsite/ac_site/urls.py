# -*- coding:utf-8 -*-
from django.conf.urls import url

from . import views

app_name = 'ac_site'
urlpatterns = [
    # ex: /ac_site/
    url(r'^$', views.index, name='index'),  # view.pyのindex関数を呼ぶ
    # ex: /ac_site/5/
    url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    # ex: /ac_site/5/results/
    url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    # ex: /ac_site/5/vote/
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]
