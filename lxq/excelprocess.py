# -*- coding: utf-8 -*-
"""
Created on Sat Apr 28 12:34:13 2018

@author: wucong02
"""

import os
import pandas as pd

#需求：1.对每个表格的数据进行去重；2.按照发行人评级排序； 3.控制填充为“-”；4.保留两位小数
os.chdir(r'C:\Users\wucong02\Desktop\lxq')
data_all=pd.read_excel('各省平台数据汇总2.xlsx',None)
provinces=data_all.keys()
writer=pd.ExcelWriter('result2.xlsx')
for province in provinces:
    data=data_all[province]
    data_du=data.drop_duplicates()
    data_du_sort=data_du.sort_values(by='发行人最新评级',ascending=False)
    data_du_sort=data_du_sort.fillna('-')
    #data_du_sort=data_du_sort.applymap(float2)
    data_du_sort.to_excel(writer,province,index=False)
writer.save()

def float2(x):
    if isinstance(x,float):
        return ('%.2f' % x)
    else:
        return x
    
    
#需求：1.分省份处理，每个省份保存为一个sheet 2.空值填充为“-”；3.保留两位小数
os.chdir(r'C:\Users\wucong02\Desktop\lxq')
data_all=pd.read_excel('各省发债企业数据汇总0429.xlsx')
data_all=data_all.fillna('-')
provinces=data_all['省份'].unique()
writer=pd.ExcelWriter('result0429.xlsx')
for province in provinces:
    data=data_all[data_all['省份']==province]
    data_f2=data.applymap(float2)
    data_f2.to_excel(writer,str(province),index=False)
writer.save()


