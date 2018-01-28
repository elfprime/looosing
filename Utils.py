# coding=utf-8
import tushare as ts
import pandas as pd

# 获得当日股票市值排序
def getMarketValue(type='all'):
    data = ts.get_today_all()
    '''
    code：代码
    name:名称
    changepercent:涨跌幅
    trade:现价,收盘后即为收盘价
    open:开盘价
    high:最高价
    low:最低价
    settlement:昨日收盘价
    volume:成交量
    turnoverratio:换手率
    amount:成交量
    per:市盈率
    pb:市净率
    mktcap:总市值，单位为万
    nmc:流通市值
    '''
    # 市值转化为亿
    data['mktcap'] = data['mktcap'] / 10000
    # 返回降序排列
    # 上海市场
    if type == 'sh':
        return data[data.code >= '600000'].sort_values(['mktcap'], ascending=False)
    elif type == 'sz':
        return data[data.code < '300000'].sort_values(['mktcap'], ascending=False)
    elif type == 'cyb':
        return data [ ('600000' > data.code) * (data.code >= '300000')].sort_values(['mktcap'], ascending=False)
    elif type == 'all':
        return data.sort_values(['mktcap'], ascending=False)
    else:
        print 'Invalid type, please double check!'

def getPerf(startDate=['2017-01-03'], type='all'):
    '''
    based on getMarketValue()
    '''
    data = getMarketValue(type).head(100)
    for date in startDate:
        priceDict = {}
        for code in data.code:
            # 暂时不考虑停牌
            # 传入日期必须为交易日
            # 前复权数据
            try:
                p = ts.get_k_data(code, start=date, end=date)['close'][0]
            except Exception as e:
                print e
            finally:
                priceDict[code] = p
        perf = pd.concat([data.set_index('code'), pd.Series(priceDict, name=date)], axis=1)
        perf['chg' + date] = perf['trade']/perf[date] - 1
    return perf






