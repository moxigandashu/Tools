# -*- coding: utf-8 -*-
"""
Created on Sun Jun 17 10:21:46 2018

@author: wucong02
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Apr 27 10:06:21 2018

@author: wucong02
"""

import os
import pandas as pd
from numpy import nan as NA
import shutil

os.chdir(r'E:\结构化自提2.0\用户体验优化专项\全部商品\20180617商品')
fileList=os.listdir('data')

failList=[]
nullLIST=[]
pro_all=0
sum1_all=0
sum2_all=0
fileList2=[]
sum1List=[]
sum2List=[]
lowFillRate={'schema':[],'keys':[],'fillrate':[],'procount':[]}
for file in fileList:
    try: 
        data=pd.read_csv(file,engine='python')
        pro_data=data.drop(['商品录入时间','userid','feedid','productid'],axis=1).applymap(nareplace)#包含必填字段
        if pro_data.shape[0]==0:
            nullLIST.append(file)
        else:
            result,m,sum1,sum2=stastic_data(pro_data)
            fileList2.append(file);sum1List.append(sum1);sum2List.append(sum2)
            lowfillrate(result)
            lowFillRateD=pd.DataFrame(lowFillRate)[['schema','keys','fillrate','procount']]
            lowFillRateD.to_excel(r'E:\结构化自提2.0\用户体验优化专项\全部商品\industry_all\低填充率字段.xlsx')
            pro_all+=m;sum1_all+=sum1;sum2_all+=sum2
            #result.to_excel('%s/result/%s.xls'%(os.path.dirname(os.getcwd()),file.replace('.csv','')))
    except:
        print('%s fail'%file)
        failList.append(file)


#计数不计name，wiseUrl字段
failList=[]
nullLIST=[]
pro_all=0
sum1_all=0
sum2_all=0
for file in fileList:
    try: 
        data=pd.read_csv(file,engine='python')
        #pro_data=data.drop(['商品录入时间','userid','feedid','productid','name','wiseUrl'],axis=1).applymap(nareplace)#不含必填字段        
        #pro_data=data.drop(['商品录入时间','userid','feedid','productid','name','wiseUrl','pcUrl','wiseImage','pcImage'],axis=1).applymap(nareplace)#不包含必填、图片、链接
        pro_data=data.drop(['wiseImage','pcImage'],axis=1).applymap(nareplace)#图片
        if pro_data.shape[0]==0:
            nullLIST.append(file)
        else:
            result,m,sum1,sum2=stastic_data(pro_data)
            pro_all+=m;sum1_all+=sum1;sum2_all+=sum2
            #result.to_excel('%s/result/%s.xls'%(os.path.dirname(os.getcwd()),file.replace('.csv','')))
    except:
        print('%s fail'%file)
        failList.append(file)


#函数，将“-”替换成空值
def nareplace(x):
    if x=='-':
        return NA
    else:
        return x
def lenmeancal(ser):#函数，计算均值
    serdropna=ser.dropna().apply(lambda x:len(str(x)))
    lenmean=serdropna.mean()
    return lenmean
def stage1cal(ser):#计算字段长度<=6的字段数
    serdropna=ser.dropna().apply(lambda x:len(str(x)))
    stage1=serdropna[serdropna<=6].count()
    return stage1
def stage2cal(ser):#计算字段长度>6&<=10的字段数
    serdropna=ser.dropna().apply(lambda x:len(str(x)))
    stage2=serdropna[(serdropna>6)&(serdropna<=10)].count()
    return stage2
def stage3cal(ser):#计算字段长度>10&<=20的字段数
    serdropna=ser.dropna().apply(lambda x:len(str(x)))
    stage3=serdropna[(serdropna>10)&(serdropna<=20)].count()
    return stage3
def stage4cal(ser):#计算字符长度>20的字段数
    serdropna=ser.dropna().apply(lambda x:len(str(x)))
    stage4=serdropna[serdropna>20].count()
    return stage4

def stastic_data(data):#统计
    m,n=data.shape
    count=data.count()
    fillrate=count/m
    mean=data.apply(lenmeancal)
    stage1=data.apply(stage1cal)
    stage2=data.apply(stage2cal)
    stage3=data.apply(stage3cal)
    stage4=data.apply(stage4cal)
    result=pd.concat([count,fillrate,mean,stage1,stage2,stage3,stage4],axis=1)
    result.columns=['count','fillrate','mean','<=6','6<len<=10','10<len<=20','>20']
    sum1=count.sum()#填写有效字段数
    sum2=m*n#全部字段数
    return result,m,sum1,sum2
#移动文件
def filemove(files,dirname='nullList'):
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    while files:
        file=files.pop()
        shutil.move(file,dirname)
#str转化成日期，并且精确到天
def timeProcess(timestr):
    return pd.to_datetime(timestr).replace(hour=0,minute=0,second=0)        
#判断填充率是否低于20%
def lowfillrate(result):
    m=result.shape[0]
    for i in range(m):
        if result.iloc[i]['fillrate']<=0.2:
            lowFillRate['schema'].append(file)
            lowFillRate['keys'].append(result.index[i])
            lowFillRate['fillrate'].append(result.iloc[i]['fillrate'])
            lowFillRate['procount'].append(result.iloc[0]['count'])

#bmc商品信息维度
data_bmc=pd.DataFrame()   
for file in fileList:
    try:
        data=pd.read_excel('data/%s'%file)
        data_info=data[['time','userid','feedid','pruductid']]
        data_info['industry']=file
        data_bmc=pd.concat([data_bmc,data_info])
    except:
        print('%s fail'%file)
data_bmc.columns=['create_time','userid','feedid','productid','schema']
print(data_bmc.describe())
data_bmc.to_excel('%s/20180617商品/data_bmc.xlsx'%os.path.dirname(os.getcwd()),index=False)



data_bmc=pd.read_excel(r'E:\结构化自提2.0\用户体验优化专项\全部商品\20180617商品\data_bmc.xlsx')
data_bmc['create_time']=data_bmc['create_time'].map(timeProcess)
#商品维度
pro_time=data_bmc.pivot_table('productid','create_time',aggfunc='count')
pro_time['proCountSum']=pro_time['productid'].cumsum()
pro_time.columns=['proCount','proCountSum']
pro_time.plot()
pro_time.to_excel(r'E:\结构化自提2.0\用户体验优化专项\全部商品\industry_all\timePro.xlsx')

#用户维度
user_time=data_bmc.drop_duplicates('userid')
user_time=user_time.pivot_table('userid','create_time',aggfunc='count')
user_time['userCountSum']=user_time['userid'].cumsum()
user_time.columns=['userCount','userCountSum']
user_time.to_excel(r'E:\结构化自提2.0\用户体验优化专项\全部商品\industry_all\timeUser.xlsx')
#用户维度与商品维度的merge
timePU=pd.merge(pro_time,user_time,left_index=True,right_index=True,how='outer')
timePU['userCount']=timePU['userCount'].fillna(0)
timePU['userCountSum']=timePU['userCountSum'].fillna(method='ffill')
timePU.to_excel((r'E:\结构化自提2.0\用户体验优化专项\全部商品\industry_all\timeProUser.xlsx'))

#1月29日-2月11日的商品增长分析
proUp1=pro_bmc[(pro_bmc['create_time']>='2018-01-29 00:00:00')& (pro_bmc['create_time']<='2018-02-11 00:00:00')]
proUp1['schema'].value_counts()

#查看不同行业填充率
fileList2=os.listdir(r'E:\结构化自提2.0\用户体验优化专项\全部商品\result')
    