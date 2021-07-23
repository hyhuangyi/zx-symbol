import time
import tushare as ts
import pysnowball as ball
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import util.HttpRequestUtil as httpUtil
from prettytable import PrettyTable
from util.DbUtil import DBHelper
from PIL import Image, ImageDraw, ImageFont
import util.ZxConsts as const
import util.SysUtil as sysUtil

# 雪球token
token = 'xq_a_token=d933d420989bdcbeaa2aec79b584f51be3446511;'
pro = ts.pro_api('2d905bef29e52fd1b0801bc0ab6ae906fc9ac2737be2f40b27b68391')
dbHelper = DBHelper()


# 获取实时数据
def realTimeData(symbols='000858'):
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
def capitalFlow(symbol='000858', count=15, type=1):
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
def panKou(symbol='000858'):
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
def capitalAssort(symbol='000858'):
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


# 获取雪球实时数据(全部symbol)
def getAllRealTimeSymbols():
    res = httpUtil.get(const.xq_list, headers=const.HEADERS)
    lists = res['data']['list']
    return lists


# 选股 涨幅2-5,量比1.2-10,量能1-20亿,换手3-10,市值 100-1000亿
def pickSymbols(percent_pre=2, percent_post=5, volume_ratio_pre=1.2, volume_ratio_post=10, amount_pre=1, amount_post=20,
                turnover_rate_pre=3, turnover_rate_post=10, market_capital_pre=100, market_capital_post=1000):
    resList = getAllRealTimeSymbols()
    table = PrettyTable(["代码", "名称", "涨幅(%)", "量能(亿)", '换手率(%)', '量比', '现价',
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
            if percent_pre < percent < percent_post and volume_ratio_pre < volume_ratio < volume_ratio_post and amount_pre < amount < amount_post and turnover_rate_pre < turnover_rate < turnover_rate_post and market_capital_pre < market_capital < market_capital_post:
                arr.append(l)
                table.add_row(
                    [symbol, name, percent, amount, turnover_rate, volume_ratio, current, current_year_percent,
                     amplitude, market_capital])
    res = table.get_string(sortby="涨幅(%)", reversesort=True)
    return res


# 获取所有symbol
def getAllSymbol():
    # 查询当前所有正常上市交易的股票列表
    data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    # arr = []
    # for d in data.values:
    #     arr.append(tuple(d))
    # dbHelper.db.truncate('truncate table stock')
    # dbHelper.db.batch_insert(
    #     'INSERT INTO stock(ts_code, symbol, name,area, industry,list_date) VALUES(%s, %s, %s, %s, %s, %s)', arr)
    return data.values


# 词云图 type 1：大涨 2：大跌
def draw_word_cloud(type=1):
    basePath = const.download_path
    resList = getAllRealTimeSymbols()
    day = time.strftime("%Y-%m-%d", time.localtime())
    arr = ''
    for l in resList:
        name = l['name']
        percent = l['percent'] if l['percent'] is not None else 0
        if '退' not in l['name'] or '*ST' not in l['name']:
            if 9.8 < percent and type == 1:
                arr += ' ' + name
            elif percent < -9.8 and type == 2:
                arr += ' ' + name
            elif type != 1 and type != 2:
                raise Exception("type请传1-2")
    wordCloud = WordCloud(width=1000,  # 图片的宽度
                          height=860,  # 高度
                          margin=2,  # 边距
                          background_color='black',  # 指定背景颜色
                          font_path=const.word_cloud_font_path
                          # 指定字体文件，要有这个字体文件，自己随便想用什么字体，就下载一个，然后指定路径就ok了
                          )
    wordCloud.generate(arr)
    if type == 1:
        fName = basePath + day + '_up.png'
    else:
        fName = basePath + day + '_down.png'
    wordCloud.to_file(fName)  # 保存到图片
    return fName


# pretty table表格转化成图片
def draw_table(tab_info, name):
    basePath = const.download_path
    space = 5
    # PIL模块中，确定写入到图片中的文本字体
    # ubuntu
    # font = ImageFont.truetype('/home/doge/YaHeiConsolas.ttf', 15, encoding='utf-8')
    # windows
    font = ImageFont.truetype(const.table_font_path, 15, encoding='utf-8')
    # Image模块创建一个图片对象
    im = Image.new('RGB', (10, 10), (0, 0, 0, 0))
    # ImageDraw向图片中进行操作，写入文字或者插入线条都可以
    draw = ImageDraw.Draw(im, "RGB")
    # 根据插入图片中的文字内容和字体信息，来确定图片的最终大小
    img_size = draw.multiline_textsize(tab_info, font=font)
    # 图片初始化的大小为10-10，现在根据图片内容要重新设置图片的大小
    im_new = im.resize((img_size[0] + space * 2, img_size[1] + space * 2))
    del draw
    del im
    draw = ImageDraw.Draw(im_new, 'RGB')
    # 批量写入到图片中，这里的multiline_text会自动识别换行符
    # python2
    # draw.multiline_text((space,space), unicode(tab_info, 'utf-8'), fill=(255,255,255), font=font)
    # python3
    draw.multiline_text((space, space), tab_info, fill=(255, 255, 255), font=font)
    fName = basePath + name + ".png"
    im_new.save(fName, "PNG")
    del draw
    return fName


# 画折线图 tick_spacing 密度  count 取数数量 type 1分钟级别 2日级别
def draw_flow(symbol='000858', tick_spacing=10, count=15, type=1):
    basePath = const.download_path
    arr = capitalFlow(symbol, count, type)[0]
    x = []
    y = []
    for r in arr:
        y.append(r['amount'])
        x.append(r['timestamp'])
    # 创建绘图对象
    fig = plt.figure(figsize=(25, 15))
    ax = fig.add_subplot(111)
    # 在当前绘图对象绘图（X轴，Y轴，蓝色虚线，线宽度）
    plt.plot(x, y, "c--", linewidth=3)
    # x轴密度
    ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    # X轴标签
    plt.xlabel("time", fontsize=40)
    # Y轴标签
    plt.ylabel("amount", fontsize=40)
    # 图标题
    plt.title("flow")
    # 设置刻度的大小,both代表xy同时设置
    plt.tick_params(axis='both', labelsize=36)
    # y轴画0刻度线
    plt.axhline(0.00, color='r', linestyle='--', label='plane')
    plt.legend(loc='upper left')
    # 保存
    day = time.strftime("%Y-%m-%d", time.localtime())
    fName = basePath + day + '_' + symbol + ".png"
    plt.savefig(fName)
    # 显示图
    plt.show()
    return fName
