import time
import requests
from lxml import etree
from util.RedisUtil import RedisHelper
import util.SysUtil as sysUtil

redisHelper = RedisHelper()

https_url = 'http://www.xiladaili.com/https/'
http_url = 'http://www.xiladaili.com/http/'


# 获取ip
def get_address(url):
    headers = sysUtil.getheaders()
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text


# 解析页面
def parse_data(html, xpath):
    html = etree.HTML(html)
    trs = html.xpath(xpath)
    data = []
    for tr in trs:
        data.append(tr.xpath('./td[1]/text()')[0].strip())
    return data


# 爬取数据任务
def ip_task(pages=20, http='https'):
    num = 0
    res = []
    while True:
        num += 1
        time.sleep(1)
        if http == 'https':
            url = https_url + str(num) + "/"
        else:
            url = http_url + str(num) + "/"
        xpath = './/table/tbody/*'
        html = get_address(url)
        arr = parse_data(html, xpath=xpath)
        res.extend(arr)
        if num == pages:
            break
    print("数据已存取完毕")
    return res


if __name__ == '__main__':
    print(ip_task(20, 'https'))
