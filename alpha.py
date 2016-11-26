# -*- coding: utf-8 -*-
"""
Created on Thu Oct 5 2016

@author: tong
"""

import tushare as ts
import time
import logging
#import pandas as pd
#import numpy as np

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='beta.log',
                filemode='w')

#通过获取上证指数实时交易数据，得到最近的实时交易日期
transday = ts.get_realtime_quotes('sh').date[0]
print "The Latest Transday:"+transday
#获取当前日期
today = time.strftime('%Y-%m-%d')
print "Today:"+today

#判断今日是否为交易日T
if today == transday:
    #获取T－1日
    #preday = ts.get_hist_data('sh').head(1).index[0]
    
    hs300 = ts.get_hs300s()
    zz500 = ts.get_zz500s()   
    hs300codes = list(hs300.iloc[:,0])
    zz500codes = list(zz500.iloc[:,0])    
    codes = hs300codes+zz500codes
    
    #寻找交易日ma5上穿ma10的个股
    for i in range(len(codes)):
        code = codes[i]
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
            maxclose = predata.close.max()
            
            if (ma5_t >= ma10_t and ma5_t1 <= ma10_t1) and xprice > maxclose:
                print code+"..." if (ma10_t >= ma20_t and ma10_t1 <= ma20_t1) else code
                logging.info(code) 
                #print code
                #if ma10_t >= ma20_t and ma10_t1 <= ma20_t1:
                    #print "........."
            
