# mysql数据库信息
mysql_host = "127.0.0.1"
mysql_port = 3306
mysql_user = "root"
mysql_password = "admin"
mysql_db = "zx"

# 钉钉配置
dingding_urL = "https://oapi.dingtalk.com/robot/send?access_token=31d756dc11a9fa23d850879416cb1e7c097a2def004f62d81b274a8970ae8638"
dingding_secret = "SECf495fcaaf44bfae5bb95eee177adf9545d3ac4ae670920bc607d46514ff6d274"

# 雪球token
xq_token = 'xq_a_token=d933d420989bdcbeaa2aec79b584f51be3446511;'
# 雪球实时数据
xq_list = 'https://xueqiu.com/service/v5/stock/screener/quote/list?page=1&size=6000&order=asc&order_by=current_year_percent&market=CN&type=sh_sz'
# 爬虫请求头
HEADERS = {'Host': 'xueqiu.com',
           'Accept': 'application/json',
           'User-Agent': 'Xueqiu iPhone 11.8',
           'Accept-Language': 'zh-Hans-CN;q=1, ja-JP;q=0.9',
           'Accept-Encoding': 'br, gzip, deflate',
           'Connection': 'keep-alive'}

# 文件下载地址
download_path = '/home/zx_temp/'

# table字体
table_font_path = 'C:\WINDOWS\Fonts\simsun.ttc'
# 词云字体
word_cloud_font_path = 'C:\Windows\Fonts\Sitka Banner\msyh.ttc'

# tushare token
tushare_pro_token = '2d905bef29e52fd1b0801bc0ab6ae906fc9ac2737be2f40b27b68391'

# 默认symbol
default_symbol = '000858'

# 策略
percent_pre = 2
percent_post = 10
volume_ratio_pre = 1.2
volume_ratio_post = 10
amount_pre = 1
amount_post = 20
turnover_rate_pre = 3
turnover_rate_post = 20
market_capital_pre = 50
market_capital_post = 1000
