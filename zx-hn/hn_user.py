import requests
import json
from datetime import datetime
from prettytable import PrettyTable

userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
Authorization = 'Bearer A8B8420A6C95D7F1E5E87002F00287D0'
if __name__ == '__main__':
    url = 'https://api-gw.huonu.com/admin/v2/admin/suggest?fields=*&status=-1&page=-1'
    headers = {'Authorization': Authorization, 'User-Agent': userAgent}
    res = requests.get(url=url, headers=headers)
    res.encoding = 'utf-8'
    json = json.loads(res.text)
    res = json['data']['items']
    table = PrettyTable(
        ['id', '邮箱', '姓名', '部门id', '是否超管', '是否外部', '状态', 'createAt', 'updateUp', 'lastLogin',
         'lastLoginIp'])
    for data in res:
        id = data['id']
        loginName = data['login_name']
        realName = data['real_name']
        dept = data['dept_id']
        isSuper = data['is_super']
        isExternal = data['is_external']
        status = data['status']
        createAt = ''
        updateUp = ''
        lastLogin = ''
        if data['created_at'] is not None:
            createAt = datetime.fromtimestamp(data['created_at']).strftime('%Y-%m-%d %H:%M:%S')
        if data['updated_at'] is not None:
            updateUp = datetime.fromtimestamp(data['updated_at']).strftime('%Y-%m-%d %H:%M:%S')
        if data['last_login'] is not None:
            lastLogin = datetime.fromtimestamp(data['last_login']).strftime('%Y-%m-%d %H:%M:%S')
        lastLoginIp = data['last_login_ip']
        table.add_row(
            [id, loginName, realName, dept, isSuper, isExternal, status, createAt, updateUp, lastLogin,
             lastLoginIp])
        # print(id, loginName, realName, dept, isSuper, isExternal, status, createAt, updateUp, lastLogin,lastLoginIp)

    res = table.get_string(sortby="id", reversesort=False)
    print(res)
