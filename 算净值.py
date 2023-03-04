#!/usr/bin/env python
# coding: utf-8

# In[8]:


date_list = sorted(score_result['日期'].unique().tolist())
if style == 'top':
    asc = [True,False]
elif style == 'bot':
    asc = [True,True]
dict_res = {}

r_Top10 = pd.DataFrame(date_list, columns=['日期'])
r_Top20 = pd.DataFrame(date_list, columns=['日期'])
r_Top50 = pd.DataFrame(date_list, columns=['日期'])
r_Top100 = pd.DataFrame(date_list, columns=['日期'])
cols = ['Top10','Top20','Top50','Top100']
r_sharpe=pd.DataFrame(np.ones((len(fct_list), len(cols))), index=fct_list, columns=cols)


# In[9]:


fct = '总市值'


# In[10]:


score_result.sort_values(by=['日期',fct], ascending=asc, inplace=True)

data_num=score_result.groupby('日期').head(10)
temp = pd.DataFrame(data_num[['日期',ZF]].groupby('日期')[ZF].mean())
sharpe=np.mean(temp[ZF])/np.std(temp[ZF])*np.sqrt(12) # 如果非月频，要改
temp = temp[ZF] / 100 + 1
stats_num = temp.cumprod(axis=0, skipna = True)
r_sharpe.ix[fct,'Top10']=sharpe
r_Top10[fct] =stats_num.reset_index(drop=True)

data_num=score_result.groupby('日期').head(20)
temp = pd.DataFrame(data_num[['日期',ZF]].groupby('日期')[ZF].mean())
sharpe=np.mean(temp[ZF])/np.std(temp[ZF])*np.sqrt(12)
temp = temp[ZF] / 100 + 1
stats_num = temp.cumprod(axis=0, skipna = True)
r_sharpe.ix[fct,'Top20']=sharpe
r_Top20[fct] =stats_num.reset_index(drop=True)

data_num=score_result.groupby('日期').head(50)
temp = pd.DataFrame(data_num[['日期',ZF]].groupby('日期')[ZF].mean())
sharpe=np.mean(temp[ZF])/np.std(temp[ZF])*np.sqrt(12)
temp = temp[ZF] / 100 + 1
stats_num = temp.cumprod(axis=0, skipna = True)
r_sharpe.ix[fct,'Top50']=sharpe
r_Top50[fct] =stats_num.reset_index(drop=True)

data_num=score_result.groupby('日期').head(100)
temp = pd.DataFrame(data_num[['日期',ZF]].groupby('日期')[ZF].mean())
sharpe=np.mean(temp[ZF])/np.std(temp[ZF])*np.sqrt(12)
temp = temp[ZF] / 100 + 1
stats_num = temp.cumprod(axis=0, skipna = True)
r_sharpe.ix[fct,'Top100']=sharpe
r_Top100[fct] =stats_num.reset_index(drop=True)


# In[11]:


r_Top100[fct]


# In[2]:


# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 14:23:47 2019

@author: yjm
"""

import numpy as np
import pandas as pd


'''
计算净值
score_result: 有日期、代码、还有各个因子列
fct_list: 要算净值的因子名称列表
ZF: '未来均价涨幅'
style: top / bot
'''




def stats(score_result, fct_list, ZF, style):
    date_list = sorted(score_result['日期'].unique().tolist())
    if style == 'top':
        asc = [True,False]
    elif style == 'bot':
        asc = [True,True]
    dict_res = {}

    r_Top10 = pd.DataFrame(date_list, columns=['日期'])
    r_Top20 = pd.DataFrame(date_list, columns=['日期'])
    r_Top50 = pd.DataFrame(date_list, columns=['日期'])
    r_Top100 = pd.DataFrame(date_list, columns=['日期'])
    cols = ['Top10','Top20','Top50','Top100']
    r_sharpe=pd.DataFrame(np.ones((len(fct_list), len(cols))), index=fct_list, columns=cols)
    for fct in fct_list:

        score_result.sort_values(by=['日期',fct], ascending=asc, inplace=True)

        data_num=score_result.groupby('日期').head(10)
        temp = pd.DataFrame(data_num[['日期',ZF]].groupby('日期')[ZF].mean())
        sharpe=np.mean(temp[ZF])/np.std(temp[ZF])*np.sqrt(12) # 如果非月频，要改
        temp = temp[ZF] / 100 + 1
        stats_num = temp.cumprod(axis=0, skipna = True)
        r_sharpe.ix[fct,'Top10']=sharpe
        r_Top10[fct] =stats_num.reset_index(drop=True)

        data_num=score_result.groupby('日期').head(20)
        temp = pd.DataFrame(data_num[['日期',ZF]].groupby('日期')[ZF].mean())
        sharpe=np.mean(temp[ZF])/np.std(temp[ZF])*np.sqrt(12)
        temp = temp[ZF] / 100 + 1
        stats_num = temp.cumprod(axis=0, skipna = True)
        r_sharpe.ix[fct,'Top20']=sharpe
        r_Top20[fct] =stats_num.reset_index(drop=True)

        data_num=score_result.groupby('日期').head(50)
        temp = pd.DataFrame(data_num[['日期',ZF]].groupby('日期')[ZF].mean())
        sharpe=np.mean(temp[ZF])/np.std(temp[ZF])*np.sqrt(12)
        temp = temp[ZF] / 100 + 1
        stats_num = temp.cumprod(axis=0, skipna = True)
        r_sharpe.ix[fct,'Top50']=sharpe
        r_Top50[fct] =stats_num.reset_index(drop=True)

        data_num=score_result.groupby('日期').head(100)
        temp = pd.DataFrame(data_num[['日期',ZF]].groupby('日期')[ZF].mean())
        sharpe=np.mean(temp[ZF])/np.std(temp[ZF])*np.sqrt(12)
        temp = temp[ZF] / 100 + 1
        stats_num = temp.cumprod(axis=0, skipna = True)
        r_sharpe.ix[fct,'Top100']=sharpe
        r_Top100[fct] =stats_num.reset_index(drop=True)

    
    r_Top10 = r_Top10.set_index('日期')
    r_Top20 = r_Top20.set_index('日期')
    r_Top50 = r_Top50.set_index('日期')
    r_Top100 = r_Top100.set_index('日期')
    
    #
    dict_res['Top10'] = r_Top10 / r_Top10.iloc[0]
    dict_res['Top20'] = r_Top20 / r_Top20.iloc[0]
    dict_res['Top50'] = r_Top50 / r_Top50.iloc[0]
    dict_res['Top100'] = r_Top100 / r_Top100.iloc[0]
    dict_res['sharpe'] = r_sharpe.T

    return dict_res





data = pd.read_csv('C:\\Users\\ZIJUN LIU\\Desktop\\刘子隽_项目数据.csv')

datalist = list(data.columns)
datalist = [x for x in datalist if x not in ['日期','代码','名称','未来均价涨幅','中信行业代码']]

print(datalist)


# In[6]:


import matplotlib.pyplot as plt
import matplotlib as mpl
result['Top50'].plot()
plt.show()
mpl.rcParams['font.sans-serif'] = ['SimHei'] 
mpl.rcParams['axes.unicode_minus'] = False


# In[5]:


score_result, fct_list, ZF, style = data, datalist, '未来均价涨幅', 'top'


# In[4]:



result = stats(data, datalist, '未来均价涨幅', 'top')
result


# In[ ]:




