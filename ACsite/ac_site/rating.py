# -*- coding:utf-8 -*-

import analitic
#import numpy as np


def marketsize(ls1, avg1, ls2, avg2, ls3, avg3):
    '''
        市場規模を計算する
        ・ls1: ForeignGuestCount.guest_count(最新年次)
        ・ls2: AnnualSummary.consumption_ammount
        ・ls3: RegionSummary.average_price
    '''

    # 重み付けパラメータ
    weight_param1 = 0.5
    weight_param2 = 0.3
    weight_param3 = 0.2

    # 要素レーティング計算
    mkt1 = basic_rating(ls1, avg1)
    mkt2 = basic_rating(ls2, avg2)
    mkt3 = basic_rating(ls3, avg3)

    # 個別レーティング計算
    mrktsize = (weight_param1 * mkt1) + (weight_param2 * mkt2) + (weight_param3 * mkt3)

    return mrktsize


def basic_rating(trg, avg):
    '''
        レーティングを計算する
        input: 数値で構成されるリストls
        output: レーティングリスト
    '''

    # 成長期
    if avg > 0:
        # lsがave未満
        if trg < avg:
            rating = 1 + trg / avg
        # lsがave近傍
        elif avg <= trg < avg * 2:
            rating = 2 + (trg - avg) / avg
        # lsがave2倍近傍
        elif avg * 2 <= trg < avg * 3:
            rating = 3 + (trg - avg) / avg
        # lsがave3倍近傍
        elif avg * 3 <= trg < avg * 5:
            rating = 4 + (trg - avg) / avg
        # lsがave5倍近傍
        else:
            rating = 5
    # 衰退期
    elif avg < 0:
        # lsがプラス
        if trg > 0:
            rating = 5
        # lsがave未満の衰退
        elif avg < trg <= 0:
            rating = 4 - (abs(trg) - abs(avg)) / abs(avg)
        # lsがave2倍未満の衰退
        elif avg * 2 < trg <= avg:
            rating = 3 - (abs(trg) - abs(avg)) / abs(avg)
        # lsがave3倍未満の衰退
        elif avg * 3 < trg <= avg * 2:
            rating = 2 - (abs(trg) - abs(avg)) / abs(avg)
        # lsがave3倍以上の衰退
        else:
            rating = 1

    return rating
