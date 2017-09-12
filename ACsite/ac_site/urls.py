# -*- coding:utf-8 -*-
from django.conf.urls import url

from . import views

app_name = 'ac_site'
urlpatterns = [
    # ex: /ac_site/ or / (/はACsiteのurlsで定義)
    url(r'^$', views.index, name='index'),  # view.pyのindex関数を呼ぶ
    # ex: /ac_site/company
    url(r'^company.html$', views.company, name='company'),
    # ex: /ac_site/contact
    url(r'^contact.html$', views.contact, name='contact'),
    # ex: /ac_site/login.html
    url(r'^login.html$', views.login, name='login'),
    # ex: /ac_site/minnpaku_news.html
    url(r'^minnpaku_news.html$', views.minnpaku_news, name='minnpaku_news'),
    # ex: /ac_site/news_release.html
    url(r'^news_release.html$', views.news_release, name='news_release'),
    # ex: /ac_site/prefs.html
    url(r'^prefs.html$', views.prefs, name='prefs'), # view.pyのpref関数を呼ぶ
    # ex: /ac_site/sign_up.html
    url(r'^sign_up.html$', views.registration, name='sign_up'),




    # ex: /ac_site/5/
    url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    # ex: /ac_site/5/results/
    url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    # ex: /ac_site/5/vote/
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),

]
