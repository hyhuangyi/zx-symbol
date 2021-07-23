import pymysql
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
class db():  # 类名和模块名一致，robot导入时不用写类名@@@@@

    def __init__(self):
        self.host = const.mysql_host
        self.port = const.mysql_port
        self.user = const.mysql_user
        self.password = const.mysql_password
        self.db = const.mysql_db
        try:
            self.conn = pymysql.connect(host=self.host,
                                        port=self.port,
                                        user=self.user,
                                        password=self.password,
                                        db=self.db,
                                        charset='utf8mb4')
        except pymysql.err.OperationalError as e:
            pass

    def truncate(self, truncate_sql):
        # 使用cursor()方法获取操作游标
        cur = self.conn.cursor()
        try:
            # 示例
            # sql = 'truncate table user '
            cur.execute(truncate_sql)
            # 提交
            self.conn.commit()
        except Exception as e:
            # 错误回滚
            self.conn.rollback()

    def insert_one(self, insert_sql, record):
        cur = self.conn.cursor()
        try:
            # 示例
            # sql = 'INSERT INTO users(username, userpass, nickname) VALUES(%s, %s, %s) '
            # rows = cur.execute(insertSql, ("shuke", "123", "舒克"))
            cur.execute(insert_sql, record)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()

    def update_one(self, update_sql, record):
        cur = self.conn.cursor()
        try:
            # 示例
            # sql="update user set name=%s,url=%s where id=%s"
            # params=("update","update","1")
            cur.execute(update_sql, record)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()

    def batch_insert(self, insertSql, records):
        # 每次插入的最大长度
        MAX_LEN = 1000
        cur = self.conn.cursor()
        try:
            # 示例
            # sql = 'INSERT INTO users(username, userpass, nickname, age) VALUES(%s, %s, %s, %s)'
            # param = [("member1", "123", "会员1", 12),("member2", "123", "会员2", 34)]
            for i in range(0, len(records), MAX_LEN):
                cur.executemany(insertSql, records[i:i + MAX_LEN])
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()

    def select_list(self, select_sql, condition=None):
        cur = self.conn.cursor()
        try:
            # 示例
            # sql = 'select *from user where name= %s and age=%s'
            # param = ("shuke", "13")
            cur.execute(select_sql, condition)
            results = cur.fetchall()
            return results
        except Exception as e:
            self.conn.rollback()


class DBHelper(object):
    def __init__(self):
        self.db = db()
