# -*- coding: utf-8 -*-     支持文件中出现中文字符
###################################################################################################################

"""
Created on Mon Nov 16 20:15:02 2020

@author: Huangjiyuan

代码功能描述: （1）读取处理后的数据
            （2）使用apyori完成关联规则算法的实现

"""
###################################################################################################################

import pandas as pd
import numpy as np
import math
from apyori import apriori

#1.读取文件并将两个文件合并
columns_name = ['mean','var','dwt_appro','dwt_detail','sampen','hurst','pfd']               #设置由各个属性组成的矩阵

dt113 = pd.read_excel(r'result_%d.xlsx'% (113))                                             #读取之前处理得到的result_113文件
dt113 = dt113.iloc[:,1:]                                                                    #去除掉第一列，也就是表格中的序列列
dt113.columns = ['label','mean','var','dwt_appro','dwt_detail','sampen','hurst','pfd']      #为每一列添加名称

dt114 = pd.read_excel(r'result_%d.xlsx'% (114))                                             #读取之前处理得到的result_114文件
dt114 = dt114.iloc[:,1:]
dt114.columns = ['label','mean','var','dwt_appro','dwt_detail','sampen','hurst','pfd']

dt = pd.concat([dt113,dt114],axis=0,ignore_index=True)                                      #将两个矩阵合并成一个矩阵

x = dt[columns_name]
y = dt['label']

#2.数据离散化
for i in columns_name:
    x_temp = pd.cut(x[i],3) #采用等宽离散化方法
    x[i] = x_temp

#3.关联规则算法
min_supp = 0.7      #定义最小支持度
min_conf = 0.8      #定义最小置信度
min_lift = 1        #定义最小提升度
data = np.array(x)
res = apriori(transactions=data, min_support=min_supp, min_confidence=min_conf, min_lift=min_lift)

#支持度（support），先输入空列表，再进行赋值
supports=[]
#置信度
confidences=[]
#提升度
lifts=[]
#基于项items_base
bases=[]
#推导项items_add
adds=[]

'''
这里用嵌套循环来读取，是因为关联规则运算结果res实际上是一个多维列表
r是从列表中取出频繁项集，而x是从频繁项集中取出关联规则。
'''
for r in res:
    for x in r.ordered_statistics:
        supports.append(r.support)
        confidences.append(x.confidence)
        lifts.append(x.lift)
        bases.append(list(x.items_base))
        adds.append(list(x.items_add))

#将结果存储为dataframe
result = pd.DataFrame({
    'support':supports,
    'confidence':confidences,
    'lift':lifts,
    'base':bases,
    'add':adds
})

#dataframe输出有时候会省略中间的变量，下面这行代码是为了让它能够全部显示
pd.set_option('display.max_columns',None)  
print(result)  #输出所有规则