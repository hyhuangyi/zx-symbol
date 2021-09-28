import const.ZxConsts as const
import util.HttpRequestUtil as http
from prettytable import PrettyTable

token = '_ga=GA1.2.324652658.1617156681; _xsrf=2|34b6f85d|2bcb9c4b359e6da6e5cd8b536de3c2b1|1632469827; Hm_lvt_40ee94ccee2cf1051316f73e3fbcf8ac=1631936158,1632469838; uname="2|1:0|10:1632469843|5:uname|8:5a2Q6L2p|b93563306398323dbb3dc18e65ee83a9ae1910bcef4189edc201bff6ff5a4c4a"; account="2|1:0|10:1632469843|7:account|16:MTg3MDU2MjEyNDk=|f9e8fe3a092d273f31dc3e832b49a2a21927d25242774892553e0330c2f0b961"; user="2|1:0|10:1632469843|4:user|12:MTQ2MTY0NA==|3a9be5ba76a1cce7a9124c211e51868cbbba8013608503e82e6a595217edfb5f"; token="2|1:0|10:1632469843|5:token|76:MzYzYTRlZmU0ZWVlN2QwYmM4YTU3ZjY5MjFmZTIyYWVlOTc4NjMxZDdlMDcxZDAxZmQxOTg2NTY=|7fe8e09507927e108ba519e450b168c7796d352e89abd077c4af0ce35418782f"; Hm_lpvt_40ee94ccee2cf1051316f73e3fbcf8ac=1632721971; _gid=GA1.2.1070073270.1632721972; _gat=1'

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
