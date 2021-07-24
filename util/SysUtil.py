import time
import datetime
import base64
import pyttsx3
from util.DbUtil import DBHelper
import util.HttpRequestUtil as http
import const.ZxConsts as const

dbHelper = DBHelper()


# 判断当前时间是否在交易时间内
def is_trade_time():
    d_time1 = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '09:30', '%Y-%m-%d%H:%M')
    d_time2 = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '11:30', '%Y-%m-%d%H:%M')
    d_time3 = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '13:00', '%Y-%m-%d%H:%M')
    d_time4 = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '15:00', '%Y-%m-%d%H:%M')
    # 当前时间
    n_time = datetime.datetime.now()

    if (d_time1 <= n_time <= d_time2) or (d_time3 <= n_time <= d_time4):
        return True
    else:
        return False


# 补全代码
def complete_symbol(symbols):
    res = []
    arr = symbols.split(",")
    for symbol in arr:
        if symbol.startswith("S"):
            res.append(symbol)
        elif symbol.startswith("6"):
            res.append("SH" + symbol)
        else:
            res.append("SZ" + symbol)
    return ",".join(res)


# 获取本地图片流
def get_img_stream(img_local_path):
    with open(img_local_path, mode='rb') as img_f:
        img_stream = img_f.read()
        img_stream = base64.b64encode(img_stream).decode()
    return img_stream


# 根据代码获取名称
def get_name_by_symbol(symbol):
    if len(symbol) == 8:
        symbol = symbol[-6:]
    elif len(symbol) != 6 and len(symbol) != 8:
        raise Exception('代码传6位或8位')
    lists = dbHelper.db.select_list('select *from stock where symbol=%s', symbol[-6:])
    if len(lists) == 1:
        return lists[0][2]
    else:
        raise Exception(symbol + '查询异常')


# 语音播报
def playSymbols(symbols):
    engine = pyttsx3.init()
    engine.setProperty('rate', 250)
    for l in symbols:
        symbol = l['symbol']
        percent = l['percent']
        # 获取名称
        name = get_name_by_symbol(symbol)
        zd = ''
        if percent > 0:
            zd = "红"
        else:
            zd = "绿"
        engine.say(name + "," + zd + "百分之" + str(abs(percent)))
    engine.runAndWait()
    engine.stop()


# 判断当前时间是否是工作日 0上班 1周末 2节假日
def isWork():
    date = time.strftime("%Y-%m-%d", time.localtime())
    param = {'d': date}
    res = http.get(const.is_holiday, params_obj=param)
    if 0 == res:
        return True
    else:
        return False
