import requests
import json

ab1 = []
n = 2  # 定义爬取的页面
daima = '000812'

if __name__ == '__main__':
    for a in range(1, n):
        url = 'http://guba.eastmoney.com/list,' + daima + '_' + str(a) + '.html'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'}
        res = requests.get(url=url, headers=headers)
        res.encoding = 'utf-8'
        data = res.text
        index = data.find("article_list=")
        data = data[index + 13:]

        data = data[0:data.find("};") + 1]
        json = json.loads(data)
        arr = json['re']
        for item in arr:
            print(item['post_title'])
