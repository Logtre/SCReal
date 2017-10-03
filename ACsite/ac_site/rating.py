# -*- coding:utf-8 -*-

import analitic
#import numpy as np


def individual_rating(ls1, avg1, ls2, avg2, ls3, avg3):
    '''個別レーティングを計算する'''

    # 重み付けパラメータ
    weight_param1 = 0.5
    weight_param2 = 0.3
    weight_param3 = 0.2

    # 要素レーティング計算
    scr1 = elemental_rating(ls1, avg1)
    scr2 = elemental_rating(ls2, avg2)
    scr3 = elemental_rating(ls3, avg3)

    # 個別レーティング計算
    rating_score = (weight_param1 * scr1) + (weight_param2 * scr2) + (weight_param3 * scr3)

    '''DEBUG用
    print(">>>>DEBUG>>>> scr1 is :")
    print(scr1)
    print(">>>>DEBUG>>>> scr2 is :")
    print(scr2)
    print(">>>>DEBUG>>>> scr3 is :")
    print(scr3)
    print(">>>>DEBUG>>>> rating_score is :")
    print(rating_score)
    '''

    return rating_score


def elemental_rating(trg, avg):
    '''要素レーティングを計算する'''

    elmt_rating = 0

    # 成長期
    if avg > 0:
        # lsがave未満
        if trg < avg:
            elmt_rating = 1 + trg / avg
        # lsがave近傍
        elif avg <= trg < avg * 2:
            elmt_rating = 2 + (trg - avg) / (avg * 2) # 1単位が2avg
        # lsがave2倍近傍
        elif avg * 2 <= trg < avg * 3:
            elmt_rating = 3 + (trg - avg) / (avg * 1) # 1単位が1avg
        # lsがave3倍近傍
        elif avg * 3 <= trg < avg * 5:
            elmt_rating = 4 + (trg - avg) / (avg * 2) # 1単位が2avg
        # lsがave5倍近傍
        else:
            elmt_rating = 5
    # 衰退期
    elif avg < 0:
        # lsがプラス
        if trg > 0:
            elmt_rating = 5
        # lsがave未満の衰退
        elif avg < trg <= 0:
            elmt_rating = 4 - (abs(trg) - abs(avg)) / (abs(avg) * 1) # 1単位が1avg
        # lsがave2倍未満の衰退
        elif avg * 2 < trg <= avg:
            elmt_rating = 3 - (abs(trg) - abs(avg)) / (abs(avg) * 1) # 1単位が1avg
        # lsがave3倍未満の衰退
        elif avg * 3 < trg <= avg * 2:
            elmt_rating = 2 - (abs(trg) - abs(avg)) / (abs(avg) * 1) # 1単位が1avg
        # lsがave3倍以上の衰退
        else:
            elmt_rating = 1

    return elmt_rating
