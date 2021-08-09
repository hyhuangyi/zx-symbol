import requests

url = 'https://httpbin.org/ip'

proxies = {'https': '203.91.121.212:3128'}
if __name__ == '__main__':
    response = requests.get(url, proxies=proxies, timeout=2)
    print(response.text)
