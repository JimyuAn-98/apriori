# -*- coding: utf-8 -*-     支持文件中出现中文字符
###################################################################################################################

"""
Created on Thu Nov 5 20:15:02 2020

@author: Huangjiyuan

代码功能描述: （1）读取处理后的数据
            （2）使用KNN完成分类的运算

"""
###################################################################################################################

import pandas as pd
import numpy as np
import math
from apyori import apriori

#0.定义将文件保存的函数
def save_in_xlsx(data,name):    
    writer = pd.ExcelWriter(r'%s.xlsx'%(name))
    data.to_excel(writer,'page_1',float_format='%.6f')
    writer.save()
    writer.close()

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

for i in columns_name:
    x_temp = pd.cut(x[i],3)
    #print(x_temp.value_counts())
    x[i] = x_temp
    #print(x)
print(x)

min_supp = 0.6
min_conf = 0.8
min_lift = 0.0
data = np.array(x)
print(data)
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
这里用嵌套循环来读取，是因为关联规则运算结果ap实际上是一个多维列表
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

# 选择支持度大于0.5，自信度大于0.5，提升度大于1
re = result[(result.lift > 1) & (result.support > 0.5) & (result.confidence > 0.5)]
#dataframe输出有时候会省略中间的变量，下面这行代码是为了让它能够全部显示
pd.set_option('display.max_columns',None)  
print(re)  #输出前三个规则