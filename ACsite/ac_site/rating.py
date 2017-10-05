# -*- coding:utf-8 -*-

import analitic
import math
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
            elmt_rating = 3 + (trg - avg) / (avg * 3) # 1単位が1avg
        # lsがave3倍近傍
        elif avg * 3 <= trg < avg * 5:
            elmt_rating = 4 + (trg - avg) / (avg * 5) # 1単位が2avg
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
            elmt_rating = 3 - (abs(trg) - abs(avg)) / (abs(avg) * 2) # 1単位が1avg
        # lsがave3倍未満の衰退
        elif avg * 3 < trg <= avg * 2:
            elmt_rating = 2 - (abs(trg) - abs(avg)) / (abs(avg) * 3) # 1単位が1avg
        # lsがave3倍以上の衰退
        else:
            elmt_rating = 1

    return elmt_rating


def cal_stdev(ls1, ls2):
    '''
        月次データから年次のヒストリカルボラティリティを計算する
        ※通常はnumpyを活用すればHVは計算できるが、
         google app engineではnumpyを利用できないため、
         標準ライブラリを活用して計算している。
    '''

    # 結果格納用リストの初期化
    trg_diff_list = [0] * 12
    sum_diff = 0
    avg_diff = 0
    trg_var = 1

    for p in range(0,12):
        trg_diff_list[p] = float(ls1[p].guest_count) / float(ls2[p].guest_count)
        sum_diff += trg_diff_list[p]

    # 平均値の計算
    avg_diff = sum_diff / 12

    for q in range(0,12):
        # 分散の計算
        trg_var = trg_var * (trg_diff_list[p] - avg_diff)

    # 標準偏差の計算
    trg_stdev = math.sqrt(trg_var)

    return trg_stdev


def cal_beta(ls1, ls2, ls3):
    '''月次データから顧客数増加割合（ベータ）を計算する'''

    # 変数初期化
    alpha_list1 = [0] * 12
    alpha_list2 = [0] * 12
    beta_sum = 0

    for p in range(0,12):
        # アルファの計算１
        alpha_list1[p] = float(ls1[p].guest_count) / float(ls2[p].guest_count)
        # アルファの計算２
        alpha_list2[p] = float(ls2[p].guest_count) / float(ls3[p].guest_count)
        # ベータの計算
        beta_sum += alpha_list1[p] / alpha_list2[p]

    # ベータの計算
    beta = beta_sum / 12

    return beta
