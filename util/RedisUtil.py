import redis
from functools import wraps
import const.ZxConsts as const


def singleton(cls):
    instances = {}

    @wraps(cls)
    def getinstance(*args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return getinstance


@singleton
class zxRedis():

    def __init__(self):
        self.host = const.redis_host
        self.port = const.redis_port
        self.db = const.redis_db
        self.password = const.redis_password
        try:
            self.conn = redis.Redis(host=self.host, port=self.port, db=self.db, password=self.password)
        except Exception as e:
            pass

    # 保存数据
    # expire：过期时间，单位秒
    def r_set(self, key, value, expire=None):
        self.conn.set(key, value, ex=expire)

    # 获取数据
    def r_get(self, key):
        value = self.conn.get(key)
        if value is None:
            return None
        return value.decode("UTF-8")

    # 删除数据
    def r_del(self, key):
        self.conn.delete(key)

    # 向set集合中添加单个或多个元素
    def r_sadd(self, key, *values):
        self.conn.sadd(key, *values)

    # 获取set列表
    def r_smembers(self, key):
        res = []
        arr = self.conn.smembers(key)
        if arr is None:
            return None
        for i in arr:
            res.append(i.decode("UTF-8"))
        return res

    # 删除set成员
    def r_srem(self, key, *values):
        self.conn.srem(key, *values)


class RedisHelper(object):
    def __init__(self):
        self.db = zxRedis()
