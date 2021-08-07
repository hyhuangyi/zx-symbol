import time
import random
import requests
import threading
from queue import Queue
import util.IpUtil as ipUtil
import const.ZxConsts as const
from util.RedisUtil import RedisHelper
import util.DingdingNotifyUtil as ding

redisHelper = RedisHelper()


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


# 检测是否有效
def is_enable(ip_port):
    proxies = {
        "http": "http://" + ip_port + "/",
        "https": "https://" + ip_port + "/"
    }
    try:
        requests.get(const.valid_url, headers=getheaders(),
                     proxies=proxies, timeout=2)
        print(threading.currentThread().name + "=====" + ip_port + ' 能用')
        return True
    except Exception as e:
        print(threading.currentThread().name + "=====" + ip_port + ' 不能用')
        return False


# 随机生成ip
def random_ip(num=const.random_num):
    arr = []
    while len(arr) < num:
        ip = ipUtil.get_ip()
        arr.append(ip)
        print(len(arr))
    return arr


# 从redis ip池获取ip列表
def redis_ip_list(key=const.ip_key):
    arr = redisHelper.db.r_smembers(key)
    return arr


# 生成队列
def get_ip_queue(ipList):
    ip_queue = Queue()
    for ip in ipList:
        ip_queue.put(ip)
    return ip_queue


# 检测ip
# type-->del: 检测库里的不合格出库  save: 生成ip 合格入库
def check_ip(ip_queue, key=const.ip_key, type=const.ip_default_type):
    while not ip_queue.empty():
        ip = ip_queue.get()
        print(ip_queue.qsize())
        if not is_enable(ip):
            if type == 'del':
                redisHelper.db.r_srem(key, ip)
        else:
            if type == 'save':
                redisHelper.db.r_sadd(key, ip)


# 多线程检测
def thread_check(thread_num=const.thread_num, random_num=const.random_num, key=const.ip_key,
                 type=const.ip_default_type):
    start_count = len(redisHelper.db.r_smembers(key))
    print(start_count)
    start = time.time()
    if type == 'save':
        ipList = random_ip(random_num)
    else:
        ipList = redis_ip_list(key)

    ip_queue = get_ip_queue(ipList)
    threads = []
    for i in range(thread_num):
        if type == 'save':
            thread = threading.Thread(target=check_ip, args=(ip_queue, key, type))
        else:
            thread = threading.Thread(target=check_ip, args=(ip_queue, key, type))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    end_count = len(redisHelper.db.r_smembers(key))
    last_count = abs(end_count - start_count)
    temp = "增加" if type == 'save' else '删除'
    msg = "多线程检测结束:用时" + str(round(time.time() - start, 2)) + "秒,共" + temp + str(last_count) + "个"
    ding.send_ding_message(msg, True)
    print(msg)


if __name__ == '__main__':
    thread_check(100,100,'ip','del')
