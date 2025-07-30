import os
from typing import Optional, Any

import pymssql
import pymysql

from giga_auto.base_class import SingletonMeta
from giga_auto.constants import DBType
from giga_auto.logger import db_log
from giga_auto.conf.settings import settings


class RedisUtils():
    def __init__(self, db_config, db_type):
        self.db_config = db_config
        self.conn = None
        self.db_type = db_type

    def redis_connect(self):
        import redis
        """Redis 连接配置"""
        self.conn = redis.StrictRedis(
            host=self.db_config["db_host"],
            port=int(self.db_config["db_port"]),
            password=self.db_config.get("db_password", None),
            db=self.db_config.get("db_name", 0),  # 默认连接到 DB 0
            decode_responses=True  # 返回值自动解码为字符串
        )

    @db_log
    def set_key(self, key, value, ex=None):
        """
        插入 Redis 键值对
        :param key: 键
        :param value: 值
        :param ex: 设置过期时间，单位为秒（可选）
        :return:
        """
        return self.conn.set(name=key, value=value, ex=ex)

    @db_log
    def get_key(self, key, field=None, start=None, end=None, score_range=None):
        """
        查询 Redis 中的值，支持 string、hash、list、set、zset 等类型的键
        :param key: 键
        :param field: 如果查询的是哈希类型，需要提供字段名
        :param start: 如果查询的是 list 或 zset，提供开始索引
        :param end: 如果查询的是 list 或 zset，提供结束索引
        :param score_range: 如果查询的是 zset，提供分数范围 (min, max)
        :return: 键对应的值，若不存在则返回 None
        """

        # 获取键的数据类型
        key_type = self.conn.type(key)

        if key_type == 'string':  # 如果是字符串类型
            value = self.conn.get(key)
            return value

        elif key_type == 'hash':  # 如果是哈希类型
            if field:  # 查询哈希字段的值
                value = self.conn.hget(key, field)
            else:  # 查询整个哈希
                value = self.conn.hgetall(key)
            return value

        elif key_type == 'list':  # 如果是列表类型
            # 如果指定了 start 和 end，返回该区间的元素
            if start is not None and end is not None:
                value = self.conn.lrange(key, start, end)
            else:
                # 如果没有指定区间，默认返回整个列表
                value = self.conn.lrange(key, 0, -1)
            return value

        elif key_type == 'set':  # 如果是集合类型
            value = self.conn.smembers(key)  # 返回集合的所有成员
            return value

        elif key_type == 'zset':  # 如果是有序集合类型
            if score_range:  # 如果指定了分数范围，返回指定分数区间的成员
                min_score, max_score = score_range
                value = self.conn.zrangebyscore(key, min_score, max_score)
            elif start is not None and end is not None:  # 如果指定了区间，返回该区间的成员
                value = self.conn.zrange(key, start, end)
            else:  # 默认返回整个有序集合的成员
                value = self.conn.zrange(key, 0, -1)
            return value

    @db_log
    def delete_key(self, key):
        """
        删除 Redis 中的键
        :param key: 键
        :return:
        """
        return self.conn.delete(key)

    @db_log
    def exists_key(self, key):
        """
        检查 Redis 中是否存在某个键
        :param key: 键
        :return: 如果键存在返回 True，否则返回 False
        """
        try:
            return self.conn.exists(key)
        except:
            return False

    @db_log
    def ttl_key(self, key):
        """
        获取 Redis 中键的剩余生存时间（TTL）
        :param key: 键
        :return: 剩余过期时间，单位为秒，若键不存在返回 -2，若键无过期时间返回 -1
        """
        return self.conn.ttl(key)


class DBUtils(RedisUtils):
    oracle_client_initialized = False

    def __init__(self, db_config, db_type=None):
        super().__init__(db_config, db_type)
        self.cursor = None
        self.db_type = db_type or DBType.mysql
        if db_type==DBType.redis:
            self.redis_connect()

    def _connect(self):
        if self.db_type == DBType.redis:
            self.redis_connect()
            return
        if self.db_type == DBType.sqlserver:
            self.sqlserver_connection()
        elif self.db_type == DBType.mysql:
            self.mysql_connect()
        elif self.db_type == DBType.oracle:
            self.oracle_connect()
        self.cursor = self.conn.cursor()

    def sqlserver_connection(self):
        self.conn = pymssql.connect(
            server=self.db_config["db_host"],
            port=int(self.db_config["db_port"]),
            user=self.db_config["db_user"],
            password=self.db_config["db_password"],
            database=self.db_config["db_name"]
        )

    def mysql_connect(self):
        self.conn = pymysql.connect(
            host=self.db_config["db_host"],
            port=int(self.db_config["db_port"]),
            user=self.db_config["db_user"],
            password=self.db_config["db_password"],
            database=self.db_config["db_name"],
            charset=self.db_config["db_charset"]
        )
        return self.conn

    def oracle_connect(self):
        import oracledb
        self.conn = oracledb.connect(
            user=self.db_config["db_user"],
            password=self.db_config["db_password"],
            dsn=f"{self.db_config['db_host']}:{self.db_config['db_port']}/{self.db_config['db_name']}"
        )
        self.cursor = self.conn.cursor()

    def mongodb_connect(self):
        from pymongo import MongoClient
        self.conn = MongoClient(
            host=self.db_config["db_host"],
            username=self.db_config["db_user"],
            password=self.db_config["db_password"],
            authSource=self.db_config["db_name"],
            replicaSet=self.db_config.get("replica_set")
        )
        self.db = self.conn[self.db_config["db_name"]]

    def get_cursor(self, dict_cursor):
        cursor = self.cursor
        if self.conn is None:
            self._connect()
        if self.db_type == DBType.mysql:
            cursor = self.conn.cursor(pymysql.cursors.DictCursor) if dict_cursor else self.conn.cursor()
        elif self.db_type == DBType.sqlserver:
            cursor = self.conn.cursor(
                as_dict=True) if dict_cursor else self.conn.cursor()  # SQL Server supports `as_dict`
        return cursor

    @db_log
    def _execute(self, sql, params=None):
        """

        :param sql:
        :param params: [()] or [[]]
        :return:
        """
        if self.cursor is None:
            self._connect()
        many = params and len(params) > 1
        if many:
            self.cursor.executemany(sql, params)
        else:
            self.cursor.execute(sql, params[0] if params else None)
        self.conn.commit()
        return self.cursor.rowcount

    @db_log
    def _fetchone(self, sql, args=None, dict_cursor=True):
        cursor = self.get_cursor(dict_cursor)
        if args:
            cursor.execute(sql, args)
        else:
            cursor.execute(sql)

        row = cursor.fetchone()
        if self.db_type == DBType.oracle:
            return self.fetch_as_dict(cursor, row)
        return row

    @db_log
    def _fetchall(self, sql, args=None, dict_cursor=True):
        cursor = self.get_cursor(dict_cursor)
        if args:
            cursor.execute(sql, args)
        else:
            cursor.execute(sql)
        rows = cursor.fetchall()
        if self.db_type == DBType.oracle:
            return self.fetch_as_dict(cursor, rows)
        return rows

    @db_log
    def _mongo_find_one(self, collection, query, projection=None):
        return self.db[collection].find_one(query, projection)

    @db_log
    def _mongo_find_all(self, collection, query, projection=None):
        return list(self.db[collection].find(query, projection))

    @db_log
    def _mongo_insert(self, collection, data):
        if isinstance(data, list):
            result = self.db[collection].insert_many(data)
        else:
            result = self.db[collection].insert_one(data)
        return result.inserted_ids if isinstance(data, list) else result.inserted_id

    @db_log
    def _mongo_update(self, collection, query, update_data):
        return self.db[collection].update_many(query, {'$set': update_data}).modified_count

    @db_log
    def _mongo_delete(self, collection, query):
        return self.db[collection].delete_many(query).deleted_count

    def fetch_as_dict(self, cursor, rows):
        """
        将 cx_Oracle cursor 的 fetchone() 或 fetchall() 结果转换为字典
        :param cursor: cx_Oracle cursor 对象
        :param rows: cursor.fetchone() 或 cursor.fetchall() 结果
        :return: 单条数据（字典）或多条数据（字典列表）
        """
        if not rows:
            return None if isinstance(rows, tuple) else []  # 返回 None 或 空列表

        columns = [col[0] for col in cursor.description]  # 获取列名并转换为小写

        if isinstance(rows, tuple):  # 处理 fetchone() 结果
            return dict(zip(columns, rows))

        return [dict(zip(columns, row)) for row in rows]  # 处理 fetchall() 结果


class DBOperation(metaclass=SingletonMeta):
    _data = {}

    def set(self, key: str, db_info: dict):
        if key not in self._data:
            if 'db_host' in db_info:
                db_utils = DBUtils(db_info, db_info.pop('db_type', None))
                self._data[key] = db_utils
            else:  # 适配同一server存在多个数据库的情况
                self._data[key] = {}
                for db_key in db_info:
                    self._data[key][db_key] = DBUtils(db_info[db_key], db_info[db_key].pop('db_type', None))

    def setup(self):
        for serv in settings.db_info:
            self.set(serv, settings.db_info[serv])

    def get(self, key: str, db_key=None) -> DBUtils:
        """
        美国drp一个系统用了两个数据库，需要二级key,其余的不用管一个service key就够了
        """
        if isinstance(self._data.get(key), DBUtils):
            return self._data.get(key)
        elif isinstance(self._data.get(key), dict):  # 处理二级key
            return self._data.get(key).get(db_key or 'default')
        raise Exception('%s not found in settings db_info' % key)

    def has(self, key: str, db_type=None) -> bool:
        return key in self._data if db_type is None else db_type in self._data.get(key)

    def clear(self):
        for k, v in self._data.items():
            if isinstance(v, dict):
                for k1, v1 in v.items():
                    v1.conn.close() if v1.conn is not None else None
            else:
                v.conn.close() if v.conn is not None else None
        self._data.clear()

    def __repr__(self):
        return f"<DB: {self._data}>"


if __name__ == '__main__':
    os.environ['GIGA_SETTINGS_MODULE'] = 'configs.settings'
    db_operation = DBOperation()
    db_operation.setup()
    a1 = db_operation.get('wms_us_web')
    a2 = db_operation.get('drp')
    a3 = db_operation.get('drp', 'origin')
    db_operation.clear()
