import const.ZxConsts as const
import util.HttpRequestUtil as http
from prettytable import PrettyTable

token = '_ga=GA1.2.324652658.1617156681;user="2|1:0|10:1631936155|4:user|12:MTQ2MTY0NA==|3c21ba3c70b91a68e4aef1a20a6e9e42a099f412bc65d38223ae10a89ae41855"; token="2|1:0|10:1631936155|5:token|76:MzYzYTRlZmU0ZWVlN2QwYmM4YTU3ZjY5MjFmZTIyYWVlOTc4NjMxZDdlMDcxZDAxZmQxOTg2NTY=|46d6ba870a1ec13d891d2d02d883e82c8a4a14f2fbe49f7d57391546b31ece7c";'

HEADERS = {'Host': 'guorn.com',
           'Accept': 'application/json',
           'Cookie': token,
           'User-Agent': 'GuoRenn iPhone 11.8',
           'Accept-Language': 'zh-Hans-CN;q=1, ja-JP;q=0.9',
           'Accept-Encoding': 'br, gzip, deflate',
           'Connection': 'keep-alive'}


def getGuoRenInfo(query='涨停'):
    data = http.get(const.guo_ren, params_obj={'query': query}, headers=HEADERS)
    table = PrettyTable(
        ['代码', '名称', '价格', '涨跌幅', '行业'])
    res = []
    price = data['data']['sheet_data']['meas_data'][0]
    increase = data['data']['sheet_data']['meas_data'][1]
    symbol = data['data']['sheet_data']['row'][0]['data'][1]
    name = data['data']['sheet_data']['row'][1]['data'][1]
    industry = data['data']['sheet_data']['row'][2]['data'][1]
    for i in range(len(symbol)):
        temp = [symbol[i], name[i], round(price[i], 2), round(increase[i] * 100, 2), industry[i]]
        table.add_row(temp)
        res.append(temp)
    return res, table.get_string(sortby='涨跌幅', reversesort=True)
