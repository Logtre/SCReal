# -*- coding:utf-8 -*-
from django.conf.urls import url, include

from . import views
from .views import (
    TopView,
    CompanyView,
    CompanyShowView,
    ContactView,
    PrefectureView,
    PrefectureShowView,
    RatingView,
    CityView,
    CityShowView,
    RankingView,
    PropertiesView,
    PropertyShowView
)

from django.contrib import admin
admin.autodiscover()

app_name = 'ac_site'
urlpatterns = [
    url(r'^$', TopView.as_view(), name='index'),
    url(r'^companies$', CompanyView.as_view(), name='companies'),
    url(r'^companies/(?P<company_id>[0-9]+)/$', CompanyShowView.as_view(), name='company_show'),
    url(r'^contacts$', ContactView.as_view(), name='contact'),
    url(r'^prefectures$', PrefectureView.as_view(), name='prefectures'),
    url(r'^prefectures/(?P<region_id>[0-9]+)/$', PrefectureShowView.as_view(), name='prefecture_show'),
    url(r'^prefectures/(?P<region_id>[0-9]+)/cities$', CityView.as_view(), name='cities'),
    url(r'^prefectures/(?P<region_id>[0-9]+)/cities/(?P<region_city_id>[0-9]+)/$', CityShowView.as_view(), name='city_show'),
    url(r'^ranking$', RankingView.as_view(), name='ranking'),
    url(r'^ratings', RatingView.as_view(), name='rating'),
    url(r'^prefectures/(?P<region_id>[0-9]+)/cities/(?P<region_city_id>[0-9]+)/properties$', PropertiesView.as_view(), name='properties'),
    url(r'^prefectures/(?P<region_id>[0-9]+)/cities/(?P<region_city_id>[0-9]+)/properties/(?P<property_id>[0-9]+)$', PropertyShowView.as_view(), name='property_show'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^signin/?$', views.signin_view),
    url(r'^signup/?$', views.signup_view),

    # ex: /ac_site/5/
    url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    # ex: /ac_site/5/results/
    url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    # ex: /ac_site/5/vote/
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),

    url(r'^admin/', include(admin.site.urls))
]
