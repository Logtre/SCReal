# -*- coding:utf-8 -*-

import analitic
import numpy as np


def basic_rating(ls, ave):
    '''
        レーティングを計算する
        input: 数値で構成されるリストls
        output: レーティングリスト
    '''
    # 成長期
    if ave > 0:
        # lsがave未満
        if ls < ave:
            rating = 1 + ls / ave
        # lsがave近傍
        elif ave <= ls < ave * 2:
            rating = 2 + (ls - ave) / ave
        # lsがave2倍近傍
        elif ave * 2 <= ls < ave * 3:
            rating = 3 + (ls - ave) / ave
        # lsがave3倍近傍
        elif ave * 3 <= ls < ave * 5:
            rating = 4 + (ls - ave) / ave
        # lsがave5倍近傍
        else
            rating = 5
    # 衰退期
    elif ave < 0:
        # lsがプラス
        if ls > 0:
            rating = 5
        # lsがave未満の衰退
        elif ave < ls <= 0:
            rating = 4 - (abs(ls) - abs(ave)) / abs(ave)
        # lsがave2倍未満の衰退
        elif ave * 2 < ls <= ave:
            rating = 3 - (abs(ls) - abs(ave)) / abs(ave)
        # lsがave3倍未満の衰退
        elif ave * 3 < ls <= ave * 2:
            rating = 2 - (abs(ls) - abs(ave)) / abs(ave)
        # lsがave3倍以上の衰退
        else:
            rating = 1

    return rating
