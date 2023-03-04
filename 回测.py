# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np


'''
输入：
    df：本期数据集，要求有以下列：日期、代码、各因子
    FactorCol：各因子
输出：
    strategy: 字典，每个键代表一个因子，值为数据框，是该因子从高到低排列的代码、未来涨幅。
'''
def Backtest_strategy(df, FactorCol, NextZf):
    strategy = {}
    for i in range(len(FactorCol)):
        df_sub = df[[FactorCol[i], '代码', NextZf]].dropna(axis = 0, how = 'any')
        strategy[FactorCol[i]] = df_sub.sort_values([FactorCol[i]],ascending = False)[['代码', NextZf]]
    return strategy


'''
功能：选择股票
输入：
    strategy: 字典，因子及其对应的排序了的数据
    NS：固定比例的调整参数
    num：固定数量的参数
    parm：1采用固定比例计算，2采用固定数量计算
    topbot：1输出top股票池信息，2输出bottom股票池信息
输出：
    dict形式，策略选股后top和bottom股票池，储存以便之后计算。每个键值代表一个策略
'''
def Backtest_choosenum(strategy, NS, num, parm, topbot):
    top_num = {}
    bot_num = {}
    for k, v in strategy.items():
        len_item = len(v)
        if (len_item < NS or len_item < num):
            top_num[k] = pd.DataFrame()
            bot_num[k] = pd.DataFrame()
            print(k+'策略无法选出满足数量的股票')
        else:
            count_num = int(len_item / NS) if parm == 1 else num
            top_num[k] = v.iloc[0 : count_num :]
            bot_num[k] = v.iloc[(len_item - count_num) : len_item :]

    return top_num if topbot == 1 else bot_num

'''
功能：计算top、bottom策略收益平均值
输入：
    top_num: top股票池
    bot_num：bottom股票池
    NextZf：未来涨幅，以计算未来收益均值
输出：
    num_return: 各策略在本周期收益均值。每一列代表一个策略
'''
def Backtest_TopBotReturn(top_num, bot_num, NextZf):
    num_return = pd.DataFrame()
    for k, v in top_num.items():
       num_return[k + '_Top'] = pd.Series(v[NextZf].mean())
    for k, v in bot_num.items():
       num_return[k + '_Bot'] = pd.Series(v[NextZf].mean())
    return num_return


# DEMO
df = pd.read_csv('backtest_demo.csv') # 这里是因子数据
FactorCol = ['隔夜跳空_5', '隔夜跳空_10', '隔夜跳空_15']
NextZf = '未来涨幅'

strategy = Backtest_strategy(df, FactorCol, NextZf)

NS = 100 # 每NS个选1个
num = 10
parm = 1
topnum = Backtest_choosenum(strategy, NS, num, parm, 1)
botnum = Backtest_choosenum(strategy, NS, num, parm, 2)

num_return = Backtest_TopBotReturn(topnum, botnum, NextZf)
# 这样得到的 num_return 是个数据框，是这一期各组合的未来涨幅


# 对每一个月末交易日求出 num_return，拼在一起，就可以进一步计算净值曲线
