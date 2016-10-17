# -*- coding: utf-8 -*-
"""
Created on Sat Oct 15 17:33:40 2016

@author: tong
"""


import tushare as ts
import time
#import pandas as pd
#import numpy as np


#通过获取上证指数实时交易数据，得到最近的实时交易日期
transday = ts.get_realtime_quotes('sh').date[0]
print "The Latest Transday:"+transday
#获取当前日期
today = time.strftime('%Y-%m-%d')
print "Today:"+today
code = "399905"

#判断今日是否为交易日T
if today == transday:
    #计算实时个股价格
    xprice = float(ts.get_realtime_quotes(code).price[0])
    #取个股T－1日的历史交易数据
    predata = ts.get_hist_data(code).head(19)
    preday = predata.index[0]
    if xprice and len(predata) == 19:
        ma5_t = (predata.close[0:4].mean() + xprice)/2
        ma10_t = (predata.close[0:9].mean() + xprice)/2
        ma20_t = (predata.close[0:19].mean() + xprice)/2
        
        ma5_t1 = predata.loc[preday,'ma5']
        ma10_t1 = predata.loc[preday,'ma10']
        ma20_t1 = predata.loc[preday,'ma20']
        
        #前19日高点
        #maxclose = predata.close.max()
        if (ma5_t >= ma10_t and ma5_t1 <= ma10_t1):
            print "5日均线上穿10均线..."
            if (ma10_t >= ma20_t and ma10_t1 <= ma20_t1):
                print "10日均线上穿20均线..."       
        if ma5_t > ma10_t and ma10_t > ma20_t:
            print "均线多头排列..."


            
