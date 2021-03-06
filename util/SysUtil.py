import os
import re
import time
import datetime
import base64
import random
from util.MsyqlUtil import MysqlHelper
import util.HttpRequestUtil as http
import const.ZxConsts as const

mysqlHelper = MysqlHelper()


# 获取今日日期
def today():
    return time.strftime("%Y-%m-%d", time.localtime())


# 获取昨日日期
def yesterday():
    now = datetime.date.today()
    yesterdayDay = now + datetime.timedelta(days=-1)
    return yesterdayDay.strftime("%Y-%m-%d")


# 获取明日日期
def tomorrow():
    now = datetime.date.today()
    tomorrowDay = now + datetime.timedelta(days=1)
    return tomorrowDay.strftime("%Y-%m-%d")


# 获取当前时间
def now_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


# 日期转成毫秒
def str_date_to_num(str_data=None):
    if str_data is None:
        str_data = today()
    # 格式时间成毫秒
    datetime_obj = datetime.datetime.strptime(str_data, "%Y-%m-%d")
    ret_stamp = int(time.mktime(datetime_obj.timetuple()) * 1000.0 + datetime_obj.microsecond / 1000.0)
    return ret_stamp


# 获取排序字段
def symbol_sort(sortBy=1):
    if sortBy == 1:
        sort = '涨幅(%)'
    elif sortBy == 2:
        sort = '年初至今(%)'
    elif sortBy == 3:
        sort = '量能(亿)'
    else:
        sort = '换手率(%)'
    return sort


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


# 判断文件是否存在 不存在创建
def create_dir_not_exist(path):
    if not os.path.exists(path):
        os.makedirs(path)


# 获取存储位置
def download_path():
    day = today()
    basePath = const.download_path
    create_dir_not_exist(basePath + day)
    return basePath + day + "/"


# 判断当前时间是否是工作日 0上班 1周末 2节假日
def is_work():
    date = today()
    param = {'d': date}
    res = http.get(const.is_holiday, params_obj=param)
    if 0 == res:
        return True
    else:
        return False


# 过滤HTML中的标签
# 将HTML中标签等信息去掉
# @param htmlStr HTML字符串.
def filter_tags(htmlStr):
    # 先过滤CDATA
    re_cdata = re.compile("//<!\[CDATA\[[^>]*//\]\]>", re.I)  # 匹配CDATA
    re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', re.I)  # Script
    re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.I)  # style
    re_br = re.compile('<br\s*?/?>')  # 处理换行
    re_h = re.compile('</?\w+[^>]*>')  # HTML标签
    re_comment = re.compile('<!--[^>]*-->')  # HTML注释
    s = re_cdata.sub('', htmlStr)  # 去掉CDATA
    s = re_script.sub('', s)  # 去掉SCRIPT
    s = re_style.sub('', s)  # 去掉style
    s = re_br.sub('\n', s)  # 将br转换为换行
    s = re_h.sub('', s)  # 去掉HTML 标签
    s = re_comment.sub('', s)  # 去掉HTML注释
    # 去掉多余的空行
    blank_line = re.compile('\n+')
    s = blank_line.sub('\n', s)
    s = replace_charEntity(s)  # 替换实体
    return s


# 替换常用HTML字符实体.
# 使用正常的字符替换HTML中特殊的字符实体.
# 你可以添加新的实体字符到CHAR_ENTITIES中,处理更多HTML字符实体.
# @param htmlStr HTML字符串.
def replace_charEntity(htmlStr):
    CHAR_ENTITIES = {'nbsp': ' ', '160': ' ',
                     'lt': '<', '60': '<',
                     'gt': '>', '62': '>',
                     'amp': '&', '38': '&',
                     'quot': '"', '34': '"', }

    re_charEntity = re.compile(r'&#?(?P<name>\w+);')
    sz = re_charEntity.search(htmlStr)
    while sz:
        entity = sz.group()  # entity全称，如>
        key = sz.group('name')  # 去除&;后entity,如>为gt
        try:
            htmlStr = re_charEntity.sub(CHAR_ENTITIES[key], htmlStr, 1)
            sz = re_charEntity.search(htmlStr)
        except KeyError:
            # 以空串代替
            htmlstr = re_charEntity.sub('', htmlStr, 1)
            sz = re_charEntity.search(htmlstr)
    return htmlStr


# 获取请求头
def getheaders():
    user_agent_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1"
    ]
    UserAgent = random.choice(user_agent_list)
    headers = {"User-Agent": UserAgent}
    return headers
