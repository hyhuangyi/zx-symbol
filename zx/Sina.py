import re
import json
import requests
import const.ZxConsts as const
from prettytable import PrettyTable


def getIndustryInfo():
    table = PrettyTable(
        ['板块', '公司家数', '平均价格', '涨跌幅', '领涨股代码', '领涨股名称', '涨幅', '当前价'])
    res = requests.get(const.sina_bk)
    res.encoding = 'gbk'
    table_text = re.findall('\{.*\}', res.text)[0]
    bk = json.loads(table_text)
    list_values = bk.values()
    for l in list_values:
        arr = l.split(",")
        table.add_row(
            [arr[1], arr[2], round(float(arr[3]), 2), round(float(arr[5]), 2),
             arr[8], arr[12],
             str(round(float(arr[9]), 2)) + ' %', round(float(arr[10]), 2), ])
    res = table.get_string(sortby="涨跌幅", reversesort=True)
    return res


if __name__ == '__main__':
    print(getIndustryInfo())
