# -*- coding:utf-8 -*-

class Analitic:
    '''算術計算を行う'''

    def __init__(self):
        pass

    def average(self, ls):
        '''平均値'''
        return(sum(ls)/len(ls))

    def dispersion(self, ls):
        '''分散'''
        ave = self.average(ls)

        return(sum([(x-ave)**2 for x in ls]) / len(ls))

    def stddev(self, ls):
        '''標準偏差'''
        return(self.dispersion(ls)**0.5)


def cal_deviation_value(ls):
    '''標準偏差を計算する
       input: 数値で構成されるリストls
       output: 標準偏差(1-5)で構成されるリストdiv_ls
    '''

    div_ls = []         # 空リストを定義

    a = Analitic()
    ave = a.average(ls)   # 平均を計算
    stddev = a.stddev(ls) # 標準偏差を計算

    for fct in ls:
        div = (int(fct) - ave) / stddev * 10 + 50   # 偏差値の計算
        div = div / 20                              # 1~5の指標に直す
        div_ls.append(div)

    return div_ls
