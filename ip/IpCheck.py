import time
import requests
import threading
from queue import Queue
import const.ZxConsts as const
import util.SysUtil as sysUtil
from util.RedisUtil import RedisHelper
import util.DingdingNotifyUtil as ding
import ip.xiciip  as xc

redisHelper = RedisHelper()


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


# 检测是否有效
# 请求的ip是https类型的，但代理ip是只支持http的 那么还是使用本机的ip
# 请求的ip是http类型的，那么代理ip一定要是http的 前面不能写成https
def is_enable(ip_port, http='https'):
    if http == 'https':
        proxies = {
            "https": ip_port
        }
        v_url = const.valid_https
    else:
        proxies = {
            "http": ip_port
        }
        v_url = const.valid_http
    try:
        requests.get(v_url, headers=sysUtil.getheaders(),
                     proxies=proxies, timeout=2)
        print(threading.currentThread().name + "=====" + ip_port + ' 能用')
        return True
    except Exception as e:
        print(threading.currentThread().name + "=====" + ip_port + ' 不能用')
        return False


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
def thread_check(thread_num=const.thread_num, key=const.ip_key,
                 type=const.ip_default_type, ip_list=None):
    start_count = len(redisHelper.db.r_smembers(key))
    print(start_count)
    start = time.time()
    if type == 'save':
        ipList = ip_list
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
    msg = "多线程检测结束:用时" + str(round(time.time() - start, 2)) + "秒,共" + temp + str(last_count) + "个，池中还有" + str(
        end_count) + "个"
    ding.send_ding_message(msg, True)
    print(msg)


if __name__ == '__main__':
    # thread_check(ip_list=xc.ip_task(20))
    thread_check(type='del')
