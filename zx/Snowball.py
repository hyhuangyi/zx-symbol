import time
import pysnowball as ball
import util.HttpRequestUtil as http
from prettytable import PrettyTable
import zx.SymbolStore as store
import const.ZxConsts as const
import util.SysUtil as sysUtil

# 雪球token
token = const.xq_token


# 获取雪球实时数据(全部symbol)
def getAllRealTimeSymbols():
    res = http.get(const.xq_list, headers=const.HEADERS)
    lists = res['data']['list']
    return lists


# 获取实时数据
def realTimeData(symbols=const.default_symbol):
    json_dic = ball.quotec(sysUtil.complete_symbol(symbols))
    stock_list = json_dic['data']
    res = []
    table = PrettyTable(["symbol", "percent", "avg_price", "current", "turnover_rate", "plv", "notify"])
    for l in stock_list:
        data = {}
        symbol = l['symbol']
        percent = l['percent']
        avg_price = l['avg_price']
        current = l['current']
        turnover_rate = l['turnover_rate']
        plv = round((current - avg_price) / avg_price * 100, 2)
        if abs(plv) < 1 and plv < 0:
            notify = 'warn'
        elif abs(plv) > 1 and plv < 0:
            notify = 'danger'
        else:
            notify = 'good'
        data['symbol'] = symbol
        data['percent'] = percent
        data['avg_price'] = avg_price
        data['current'] = current
        data['turnover_rate'] = turnover_rate
        data['plv'] = plv
        data['notify'] = notify
        res.append(data)
        table.add_row([symbol, percent, avg_price, current, turnover_rate, plv, notify])
    return res, table


# 资金流水
def capitalFlow(symbol=const.default_symbol, count=15, type=1):
    # 设置token
    ball.set_token(token)
    table = PrettyTable(["时间", "金额"])
    # 获取流水
    if type == 1:
        # 每分钟数据
        json_dic = ball.capital_flow(sysUtil.complete_symbol(symbol))
    else:
        # 每日数据
        json_dic = ball.capital_history(sysUtil.complete_symbol(symbol))

    # 流水列表
    flowArr = json_dic['data']['items']
    # 取后多少个
    res = flowArr[-count:]
    for r in res:
        if type == 1:
            r["timestamp"] = time.strftime("%H:%M", time.localtime(r['timestamp'] / 1000))
        else:
            r["timestamp"] = time.strftime("%Y-%m-%d", time.localtime(r['timestamp'] / 1000))
        r['amount'] = round(r['amount'] / 10000, 3)
        table.add_row([r['timestamp'], r['amount']])
    return res, table


# 获取实时分笔数据
def panKou(symbol=const.default_symbol):
    # 设置token
    ball.set_token(token)
    res = ball.pankou(sysUtil.complete_symbol(symbol))
    info = res['data']
    table = PrettyTable(["下标", "买盘", "买数量(手)", "卖盘", "卖数量(手)"])
    for da in [1, 2, 3, 4, 5]:
        bp = info['bp' + str(da)]
        bc = info['bc' + str(da)]
        sp = info['sp' + str(da)]
        sc = info['sc' + str(da)]
        if bc is not None:
            bc = round(bc / 100)
        if sc is not None:
            sc = round(sc / 100)
        table.add_row([da, bp, bc, sp, sc])
    return res, table


# 资金成交分布
def capitalAssort(symbol=const.default_symbol):
    # 设置token
    ball.set_token(token)
    res = ball.capital_assort(sysUtil.complete_symbol(symbol))
    info = res['data']
    table = PrettyTable(["标识", "大单", "中单", "小单", "总共", "时间"])
    sell_large = round(info['sell_large'] / 10000, 2) if info['sell_large'] is not None else None
    sell_medium = round(info['sell_medium'] / 10000, 2) if info['sell_medium'] is not None else None
    sell_small = round(info['sell_small'] / 10000, 2) if info['sell_small'] is not None else None
    sell_total = round(info['sell_total'] / 10000, 2) if info['sell_total'] is not None else None
    buy_large = round(info['buy_large'] / 10000, 2) if info['buy_large'] is not None else None
    buy_medium = round(info['buy_medium'] / 10000, 2) if info['buy_medium'] is not None else None
    buy_small = round(info['buy_small'] / 10000, 2) if info['buy_small'] is not None else None
    buy_total = round(info['buy_total'] / 10000, 2) if info['buy_total'] is not None else None
    day = time.localtime(info['timestamp'] / 1000)
    table.add_row(["卖单", sell_large, sell_medium, sell_small, sell_total,
                   time.strftime("%Y-%m-%d", day)])
    table.add_row(["买单", buy_large, buy_medium, buy_small, buy_total,
                   time.strftime("%Y-%m-%d", day)])
    return res, table


# 获取龙虎榜
# date时间形如2021-08-08
def longHuBang(str_date=None):
    num_date = sysUtil.str_date_to_num(str_date)
    json_dic = http.get(const.xq_long_hu_bang, params_obj={'date': num_date}, headers=const.HEADERS)
    dataList = json_dic['data']['items']
    table = PrettyTable(['代码', '名称', '收盘价', '涨幅(%)', '成交量', '成交额', '上榜原因'])
    res = []
    for l in dataList:
        data = {}
        symbol = l['symbol']
        name = l['name']
        close = l['close']
        percent = l['percent']
        volume = l['volume']
        amount = l['amount']
        type_name = l['type_name']

        data['symbol'] = symbol
        data['name'] = name
        data['close'] = close
        data['percent'] = percent
        data['volume'] = volume
        data['amount'] = amount
        data['type_name'] = type_name
        res.append(data)
        table.add_row([symbol, name, close, percent, volume, amount, type_name])
    return res, table.get_string(sortby='涨幅(%)', reversesort=True)


# 选股: 涨幅 percent,量比 volume_ratio,量能 amount,换手 turnover_rate,市值 market_capital
def pickSymbols(percent_pre=const.percent_pre, percent_post=const.percent_post, volume_ratio_pre=const.volume_ratio_pre,
                volume_ratio_post=const.volume_ratio_post, amount_pre=const.amount_pre, amount_post=const.amount_post,
                turnover_rate_pre=const.turnover_rate_pre, turnover_rate_post=const.turnover_rate_post,
                market_capital_pre=const.market_capital_pre, market_capital_post=const.market_capital_post, sortBy=1):
    resList = getAllRealTimeSymbols()
    table = PrettyTable(['代码', '名称', '涨幅(%)', '量能(亿)', '换手率(%)', '量比', '现价',
                         '年初至今(%)', '振幅(%)', '市值(亿)'])
    arr = []
    for l in resList:
        symbol = l['symbol']
        name = l['name']
        current = l['current'] if l['current'] is not None else 0
        percent = l['percent'] if l['percent'] is not None else 0
        amplitude = l['amplitude'] if l['amplitude'] is not None else 0
        amount = round(l['amount'] / 100000000, 2) if l['amount'] is not None else 0
        volume_ratio = l['volume_ratio'] if l['volume_ratio'] is not None else 0
        current_year_percent = l['current_year_percent'] if l['current_year_percent'] is not None else 0
        turnover_rate = l['turnover_rate'] if l['turnover_rate'] is not None else 0
        market_capital = round(l['market_capital'] / 100000000, 2) if l['market_capital'] is not None else 0

        if '退' not in l['name'] or '*ST' not in l['name']:
            if percent_pre <= percent <= percent_post and volume_ratio_pre <= volume_ratio <= volume_ratio_post and amount_pre <= amount <= amount_post and turnover_rate_pre <= turnover_rate <= turnover_rate_post and market_capital_pre <= market_capital <= market_capital_post:
                arr.append(l)
                table.add_row(
                    [symbol, name, percent, amount, turnover_rate, volume_ratio, current, current_year_percent,
                     amplitude, market_capital])
    if sortBy == 1:
        sort = '涨幅(%)'
    elif sortBy == 2:
        sort = '年初至今(%)'
    elif sortBy == 3:
        sort = '量能(亿)'
    else:
        sort = '换手率(%)'
    res = table.get_string(sortby=sort, reversesort=True)
    return res


# 根据年初至今和今日涨幅选股
def pickSymbolByHistory(date=sysUtil.today(), current=5, cyp_pre=-10, cyp_post=10):
    arr = store.selectStockHistory(date, current, cyp_pre, cyp_post)
    table = PrettyTable(['时间', '代码', '名称', '涨幅(%)', '年初至今(%)', '量能(亿)', '换手率(%)', '市值(亿)'])
    for l in arr:
        table.add_row(
            [l[0], l[1], l[2], round(l[3], 2), round(l[4], 2), round(l[5], 2), round(l[6], 2), round(l[7], 2)])
    return table

