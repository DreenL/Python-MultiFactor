#!/usr/bin/env python
# coding: utf-8

# In[4]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import inv
import matplotlib as mpl

data = pd.read_csv('C:\\Users\\ZIJUN LIU\\Desktop\\刘子隽_项目数据.csv')


# In[ ]:


data2 = data.set_index(['日期','代码'])


# In[3]:


# IC

results = pd.DataFrame(index = data2.index, columns = data.columns[1:])
for i in range(2, len(data.columns) - 3):
    results.iloc[:,i] = data.groupby(['日期']).apply(lambda x: x.iloc[ :, i+1 ].corr(data['未来均价涨幅'])) 
results;


# In[4]:


#  IR

results2 = pd.DataFrame(index = results.index, columns = results.columns)

for i in range(2, len(data.columns) - 3):
    results2.iloc[:,i] = results.iloc[:, i]/results.iloc[:,i].std() * np.sqrt(12)
results2;


# In[5]:


'''

输入index的名称来得到一个包含日期的list

'''
def total_idx(choose_idx, data_input):
    final = [];
    for idx, kv in data_input.groupby([choose_idx]):
        final.append(idx)
    return final


# In[6]:


'''

n ----选择N只股票
choose_factor --- 选择某一单因子
choose_idx --- 选择需要的index来提取出某一indx中的股票
sequence --- 选择正序或者逆序 --- 逆序(选大) = True ； 正序（选小） = False

目的：在不同时期选择由特定单因子决定N只股票持有，并显示出所持有的股票。

'''
def choose_stock(n, choose_factor , choose_idx):
    data3 = 0;
    data4 = 0;
    data5 = 0;
    outs = pd.DataFrame(columns = data.columns)
    number = list(data2.columns).index(choose_factor);
    for i in range(0,len(total_idx(choose_idx,data2))):
        data3 = data2.iloc[data2.index.get_level_values(choose_idx) == total_idx(choose_idx,data2)[i]]
        data4 = data3.sort_values(choose_factor).iloc[-51:-1,:]
        data5 = data4.reset_index(['日期','代码'])
        for j in range(0,50):
            outs = outs.append(data5.loc[j,:], ignore_index=True)
    return outs


# In[7]:


answer = choose_stock(50, "归属于母公司所有者净利润" , "日期")
answer


# In[8]:




def data_list( choose_factor , choose_idx, choose_data):
    ans = [];
    choose_data2 = choose_data.set_index([choose_idx]);
    for i in range(0,len(total_idx(choose_idx,choose_data))):
        data3 = choose_data2.iloc[choose_data2.index.get_level_values(choose_idx) == total_idx(choose_idx,choose_data)[i]]
        data4 = data3[choose_factor]
        data5 = sum(data4)/len(data4)
        ans.append(data5)
    return ans
data_listans = data_list( "归属于母公司所有者净利润" , "日期" , answer)
data_listans;


# In[19]:


'''

choose_col --- 选择某一单因子
a_list --- 需要输入的list
choose_data --- 需要输入的数据（从文件中读取的数据）


建立dataframe,进行画图。

'''

def draw_1(choose_col, a_list, choose_data):
    outs = pd.DataFrame(index = choose_data.index.levels[0], columns = [choose_col])
    for i in range(0,len(choose_data.index.levels[0])):
        outs.iloc[i,0] = a_list[i]
    return outs

aka = draw_1("归属于母公司所有者净利润", data_listans, data2 )
aka.plot()
plt.show()


# In[10]:


mpl.rcParams['font.sans-serif'] = ['SimHei'] 
mpl.rcParams['axes.unicode_minus'] = False


# In[17]:



def return_ratelist(n, choose_factor , ZF , choose_idx ):
    data_rate = choose_stock(n, choose_factor , choose_idx);
    ans = [];
    data_rate = data_rate.set_index(['日期','代码']);
    for i in range(0,len(total_idx(choose_idx , data2 ))):
        data3 = data_rate.iloc[data_rate.index.get_level_values(choose_idx) == total_idx(choose_idx,data2)[i]]
        value_ZF = data3[ZF].mean()
        ans.append(value_ZF)
    return ans
             

bet = return_ratelist(50, '资产负债率' , '未来均价涨幅' , '日期')
draw_1('资产负债率', bet, data2 ).plot()
plt.show()


# In[20]:





bet = return_ratelist(50, '资产负债率' , '未来均价涨幅' , '日期')
bet2 = return_rate(bet)
draw_1('资产负债率', bet2, data2 ).plot()
plt.show()




# In[18]:


def return_rate(list_want):
    anw = 0;
    anw1 = 1;
    anw_list = [];
    for i in range(0,len(list_want)):
        anw = (100+list_want[i])/100
        anw1 = anw1 * anw
        anw_list.append(anw1)
    return anw_list



# In[ ]:


x = list(data.columns)
x.index("归属于母公司所有者净利润")


# In[ ]:


data3 = pd.read_csv('C:\\Users\\ZIJUN LIU\\Desktop\\刘子隽_项目数据.csv')

datalist2 = list(data3.columns)
datalist2 = [b for b in datalist2 if b not in ['日期','代码','名称','未来均价涨幅','中信行业代码']]

def data_std(data_input):
    outs = pd.DataFrame(columns = data.columns)
    x = list(data_input.columns)
    num = len(total_idx('日期' , data2 ));
    for i in range(0, num):
        new_data1 = data2.iloc[data2.index.get_level_values('日期') == total_idx('日期',data2)[i]]
        new_data1 = new_data1.reset_index(['日期','代码'])
        num2 = len(new_data1.iloc[:,1]);
        for j in range(0,num2):
            for k in datalist2:
                need_col = x.index(k)
                need_mean = new_data1[k].mean()
                need_std = new_data1[k].std()
                need_value = (new_data1.iloc[j,:][k] - need_mean)/need_std;
                new_data1.iloc[j,need_col] = need_value
            new_data1.iloc[j,:].reset_index()
            outs = outs.append(new_data1.iloc[j,:],ignore_index=True)
    return outs


                
data_std(data3)    
    
    
    
    
    


# In[ ]:


def k():
    outs = pd.DataFrame(columns = data.columns)
    x = list(data3.columns)
    new_data1 = data2.iloc[data2.index.get_level_values('日期') == total_idx('日期',data2)[0]]
    new_data1 = new_data1.reset_index(['日期','代码'])
    num2 = len(new_data1.iloc[:,1]);
    for j in range(0,num2):
        for k in datalist2:
            need_col = x.index(k)
            need_mean = new_data1[k].mean()
            need_std = new_data1[k].std()
            need_value = (new_data1.iloc[j,:][k] - need_mean)/need_std;
            new_data1.iloc[j,need_col] = need_value
        new_data1.iloc[j,:].reset_index()
        outs = outs.append(new_data1.iloc[j,:])
    return outs
k()


# In[ ]:


data3 = pd.read_csv('C:\\Users\\ZIJUN LIU\\Desktop\\刘子隽_项目数据.csv')
datalist2 = list(data3.columns)
datalist2 = [b for b in datalist2 if b not in ['日期','代码','名称','未来均价涨幅','中信行业代码']]

def data_std2(data_input):
    num = len(total_idx('日期' , data2 ));
    outs = pd.DataFrame(columns = data_input.columns)
    for i in range(0, num):
        new_data1 = data2.iloc[data2.index.get_level_values('日期') == total_idx('日期',data2)[i]]
        for col in datalist2:
            new_data1[col] = new_data1.groupby(['日期'])[col].transform(lambda x: (x-x.mean())/x.std())
        outs = outs.append(new_data1)
    return outs
data_std2(data3)
            


# In[ ]:


data3 = pd.read_csv('C:\\Users\\ZIJUN LIU\\Desktop\\刘子隽_项目数据.csv')

datalist2 = list(data3.columns)
datalist2 = [b for b in datalist2 if b not in ['日期','代码','名称','未来均价涨幅','中信行业代码']]

new_data1 = data2.iloc[data2.index.get_level_values('日期') == total_idx('日期',data2)[0]]
new_data1 = new_data1.reset_index()
outs = pd.DataFrame(columns = data.columns)
for col in datalist2:
    new_data1[col] = new_data1.groupby(['日期'])[col].transform(lambda x: (x-x.mean())/x.std())
    
new_data1


# In[ ]:


new_data1 = data2.iloc[data2.index.get_level_values('日期') == total_idx('日期',data2)[0]]
new_data1 = new_data1.reset_index(['日期','代码'])
num2 = len(new_data1.iloc[:,1])
new_data1['归属于母公司所有者净利润'].std()


# In[66]:



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




# In[14]:




def choose_Multistock():
    data3 = 0;
    data4 = 0;
    data5 = 0;
    System_work = True
    ans = [];
    print('Please give the address of the csv file')
    file1 = input()
    file2 = pd.read_csv(file1);
    file3 = file2.set_index(['日期', '代码'])
    print('Please give the index to determine a given period')
    index1 = input()
    print('how many factors do you wanna choose!')
    while System_work:
        Command = input()
        if int(Command) == 1:
            print('Please choose a factor you want!')
            factor1 = input()
            print('Please tell how many stocks you wanna hold in a given period!')
            how_many1 = input()
            draw_fianl = draw_1(factor1, choose_stock(int(how_many1) , factor1 , index1), file3)
            draw_final.plot()
            plt.show()
            mpl.rcParams['font.sans-serif'] = ['SimHei'] 
            mpl.rcParams['axes.unicode_minus'] = False
            break
        elif int(Command) == 0 or int(Command) > len(file3.columns):
            print('Wrong! Invalid number!')
            continue
        else:
            print('Please give a list of factors you wanna choose')
            factor_list = input()
            new_flist = factor_list[1:-1];
            
    for i in range(0,len(total_idx(choose_idx))):
        data3 = data2.iloc[data2.index.get_level_values(choose_idx) == total_idx(choose_idx)[i]]
        data4 = sorted(data3[choose_factor],reverse = True)
        data5 = sum(data4[0:total])/len(data4[0:total])
        ans.append(data5)
    return ans
answer = choose_stock(50 , "归属于母公司所有者净利润" , "日期")

