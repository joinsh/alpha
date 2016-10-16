# -*- coding: utf-8 -*-
"""
Created on Thu Oct 5 2016
T日，日终计算ma5上穿ma10的股票
@author: tong
"""

import tushare as ts
import time


#获取当前日期
today = time.strftime('%Y-%m-%d')
print "Today:"+today
#通过获取上证指数实时交易数据，得到最近的实时交易日期
transday = ts.get_realtime_quotes('sh').date[0]
print "The Last Transday:"+transday

#判断今日是否为交易日T
if today == transday:
    #获取T－1日
    preday = ts.get_hist_data('sh').head(2).index[1]
    print "The Pre Transday:"+preday

    hs300 = ts.get_hs300s()
    zz500 = ts.get_zz500s()   
    hs300codes = list(hs300.iloc[:,0])
    zz500codes = list(zz500.iloc[:,0])    
    codes = hs300codes+zz500codes

    print "Checking Start..."
    #寻找交易日ma5上穿ma10的个股
    for i in range(len(codes)):
        code = codes[i]
        #取个股最近T日与T-1日的历史交易数据
        hist_data = ts.get_hist_data(code,start=preday,end=transday)
        if len(hist_data) == 2:
            ma5_t = hist_data.loc[transday,'ma5']
            ma5_t1 = hist_data.loc[preday,'ma5']
            ma10_t = hist_data.loc[transday,'ma10']
            ma10_t1 = hist_data.loc[preday,'ma10']
            ma20_t = hist_data.loc[transday,'ma20']
            ma20_t1 = hist_data.loc[preday,'ma20']
        
            if ma5_t >= ma10_t and ma5_t1 <= ma10_t1:
                print code+"..." if (ma10_t >= ma20_t and ma10_t1 <= ma20_t1) else code
    print "Checking End..."
            
