import json
import requests
import urllib.parse


# get请求
def get(url, token=None, headers={}, params_obj={}):
    if token is not None:
        headers['Authorization'] = 'Bearer ' + token
    if params_obj != {}:
        params = urllib.parse.urlencode(params_obj).encode('utf-8')
        response = requests.get(url + "?" + str(params, 'utf-8'), headers=headers)
    else:
        response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(response.content)

    return to_response(response)


# post请求 入参为application/json这种情况
def post(url, token=None,
         headers={'Content-type': 'application/json;charset=UTF-8', 'Accept': 'application/json, text/plain'},
         params={}):
    if token is not None:
        headers['Authorization'] = 'Bearer ' + token
    response = requests.post(url, data=json.dumps(params),
                             headers=headers)
    if response.status_code != 200:
        raise Exception(response.content)
    return to_response(response)


# 将get post请求的结果(byte[])转成对象
def to_response(response):
    # 得到的是byte[]
    byte_content = response.content
    # 转成字符串
    content = str(byte_content, 'utf-8')
    # 转成对象
    return json.loads(content)
