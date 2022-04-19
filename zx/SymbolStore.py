import tushare as ts
import const.SqlConsts as sql
import const.ZxConsts as const
import util.SysUtil as sysUtil
from util.MsyqlUtil import MysqlHelper

pro = ts.pro_api(const.tushare_pro_token)
mysqlHelper = MysqlHelper()


# 存储所有股票基础信息
def saveAllSymbol():
    # 查询当前所有正常上市交易的股票列表
    data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    arr = []
    for d in data.values:
        arr.append(tuple(d))
    mysqlHelper.db.truncate(sql.truncate_stock)
    mysqlHelper.db.batch_insert(sql.stock_insert_sql, arr)
    return arr


# 保存当日股票交易信息
def saveStockHistory(date=None):
    import zx.Snowball as ball
    if date is None:
        date = sysUtil.today()
    resList = ball.getAllRealTimeSymbols()
    now_time = sysUtil.now_time()
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
             market_capital, date, now_time]))
    mysqlHelper.db.delByCondition(sql.del_stock_history_by_date, tuple([date]))
    mysqlHelper.db.batch_insert(sql.stock_history_insert_sql, arr)
    return arr


# 查询历史 根据年初至今和今日涨幅
# date 日期,current 当前日期涨幅, cyp 年初至今涨幅
def selectStockHistory(date=sysUtil.today(), current=5, cyp_pre=-10, cyp_post=10):
    arr = mysqlHelper.db.select_list(sql.stock_history_select, tuple([date, current, cyp_pre, cyp_post]))
    return arr


# 根据代码获取名称
def get_name_by_symbol(symbol):
    if len(symbol) == 8:
        symbol = symbol[-6:]
    elif len(symbol) != 6 and len(symbol) != 8:
        raise Exception('代码传6位或8位')
    lists = mysqlHelper.db.select_list(sql.select_by_symbol, symbol)
    if len(lists) == 1:
        return lists[0][2]
    else:
        raise None


# 根据名称获取代码
def get_symbol_by_name(name):
    lists = mysqlHelper.db.select_list(sql.select_by_name, name)
    if len(lists) == 1:
        return lists[0][1]
    else:
        return None
if __name__ == '__main__':
    print(saveAllSymbol())
