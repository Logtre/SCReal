# -*- coding:utf-8 -*-

# Copyright 2015 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.conf.urls import include, url
from django.contrib import admin

from ac_site.views import index

# url(regex, view, kwargs=None, name=None)
# regex:    URLから引数に該当する文字列を探す。ヒットしたら処理開始
# view:     ヒットした場合の表示するview（view.pyに定義された関数）を定義
# kwargs:   追加的な処理を定義
# name:     urlパターンに名前をつける

urlpatterns = [
    url(r'^$', index),  # ac_site/view.pyのindex関数にリダイレクト（import文から）
    url(r'^ac_site/', include('ac_site.urls')), # ac_site/なら/ac_site/urls.pyを参照する
    url(r'^admin/', include(admin.site.urls)),
]
