import time
import tushare as ts
import zx.Snowball as ball
import const.ZxConsts as const
from util.DbUtil import DBHelper

pro = ts.pro_api(const.tushare_pro_token)
dbHelper = DBHelper()


# 存储所有股票基础信息
def saveAllSymbol():
    insert_sql = "INSERT INTO stock(ts_code, symbol, name,area, industry,list_date) VALUES(%s, %s, %s, %s, %s, %s)"
    # 查询当前所有正常上市交易的股票列表
    data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    arr = []
    for d in data.values:
        arr.append(tuple(d))
    dbHelper.db.truncate('truncate table stock')
    dbHelper.db.batch_insert(insert_sql, arr)
    return arr


# 保存当日股票交易信息
def saveStockHistory():
    insert_sql = 'INSERT INTO stock_history(symbol,name,current,percent,amplitude,amount,volume_ratio,current_year_percent,turnover_rate,market_capital,date) VALUES(%s, %s, %s, %s, %s, %s,%s, %s, %s, %s,%s)'
    del_sql = 'delete from stock_history where date=%s'
    date = time.strftime("%Y-%m-%d", time.localtime())
    resList = ball.getAllRealTimeSymbols()
    arr = []
    for l in resList:
        symbol = l['symbol']
        name = l['name']
        current = l['current']
        percent = l['percent']
        amplitude = l['amplitude']
        amount = round(l['amount'] / 100000000, 2) if l['amount'] is not None else 0
        volume_ratio = l['volume_ratio']
        current_year_percent = l['current_year_percent']
        turnover_rate = l['turnover_rate']
        market_capital = round(l['market_capital'] / 100000000, 2) if l['market_capital'] is not None else 0
        arr.append(tuple(
            [symbol, name, current, percent, amplitude, amount, volume_ratio, current_year_percent, turnover_rate,
             market_capital, date]))
    dbHelper.db.delByCondition(del_sql, date)
    dbHelper.db.batch_insert(insert_sql, arr)
    return arr
