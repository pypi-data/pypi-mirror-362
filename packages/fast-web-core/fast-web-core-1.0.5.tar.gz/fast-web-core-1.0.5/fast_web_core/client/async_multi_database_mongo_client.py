# encoding: utf-8
import threading
from typing import Optional
from ..client.async_mongo_client import AsyncMongo
from ..lib import cfg, logger

LOGGER = logger.get('AsyncMultiDBMongo')


class AsyncMultiDBMongo(AsyncMongo):
    """
    异步多库Mongo客户端简易封装
    """

    def __init__(self, mongo_url=None, mongo_db=None):
        if not mongo_url:
            mongo_url = cfg.get('MONGO_URL') or 'mongodb://localhost:27017'
        if not mongo_db:
            mongo_db = cfg.get('MONGO_DB')
            if not mongo_db:
                raise Exception('mongodb database not specified')

        super().__init__(mongo_url, mongo_db)
        LOGGER.info(f'[{mongo_db}] multi database mongodb inited~')


class AsyncMultiDBMongoHolder(object):
    """
    多库Mongo客户端持有器（租户数据库连接池）
    """
    _instance_lock = threading.Lock()
    _db_instance_dict = dict()

    def __new__(cls, *args, **kwargs):
        if not hasattr(AsyncMultiDBMongoHolder, "_instance"):
            with AsyncMultiDBMongoHolder._instance_lock:
                if not hasattr(AsyncMultiDBMongoHolder, "_instance"):
                    AsyncMultiDBMongoHolder._instance = object.__new__(cls)
        return AsyncMultiDBMongoHolder._instance

    @staticmethod
    def get_mongo(db_name) -> Optional[AsyncMultiDBMongo]:
        if not db_name:
            return None

        # 有实例则直接返回
        if db_name in AsyncMultiDBMongoHolder._db_instance_dict:
            return AsyncMultiDBMongoHolder._db_instance_dict.get(db_name)

        # 无实例则加锁创建
        AsyncMultiDBMongoHolder._instance_lock.acquire()
        try:
            # 双重锁校验
            if db_name not in AsyncMultiDBMongoHolder._db_instance_dict:
                # 初始化新实例
                inst = AsyncMultiDBMongo(mongo_db=db_name)
                AsyncMultiDBMongoHolder._db_instance_dict[db_name] = inst
            return AsyncMultiDBMongoHolder._db_instance_dict.get(db_name)
        finally:
            AsyncMultiDBMongoHolder._instance_lock.release()
