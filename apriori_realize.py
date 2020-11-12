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
    x_temp = pd.qcut(x[i],3)
    print(x_temp.value_counts())
    x[i] = x_temp
    print(x)
print(x)