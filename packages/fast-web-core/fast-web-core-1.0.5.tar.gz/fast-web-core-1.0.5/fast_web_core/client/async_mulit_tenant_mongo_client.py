# encoding: utf-8
import asyncio
import threading
from typing import Optional
from ..client.async_mongo_client import AsyncMongo
from ..lib import cfg, logger


LOGGER = logger.get('AsyncMultiTenantMongo')


class AsyncMultiTenantMongo(AsyncMongo):
    """
    异步多租户Mongo客户端简易封装
    """
    def __init__(self, tenant_code=None, mongo_url=None, mongo_db=None, db_prefix=None):
        if not mongo_url:
            mongo_url = cfg.get('MONGO_URL') or 'mongodb://localhost:27017'
        if not mongo_db:
            if tenant_code and (db_prefix or cfg.get('MONGO_DB_BIZ_PREFIX', None)):
                mongo_db = f"{db_prefix or cfg.get('MONGO_DB_BIZ_PREFIX', None)}{tenant_code}"
        if not mongo_db:
            raise Exception('mongodb database not specified')
        super().__init__(mongo_url, mongo_db)
        LOGGER.info(f'[{tenant_code}] tenant mongodb inited~')


class AsyncMultiTenantMongoHolder(object):
    """
    异步多租户Mongo客户端持有器（租户数据库连接池）
    """
    _instance_lock = threading.Lock()
    _instance_async_lock = asyncio.Lock()
    _tenant_instance_dict = dict()

    def __new__(cls, *args, **kwargs):
        if not hasattr(AsyncMultiTenantMongoHolder, "_instance"):

            if not hasattr(AsyncMultiTenantMongoHolder, "_instance"):
                AsyncMultiTenantMongoHolder._instance = object.__new__(cls)

        return AsyncMultiTenantMongoHolder._instance

    @staticmethod
    def get_tenant_mongo(tenant_code: str) -> Optional[AsyncMultiTenantMongo]:
        if not tenant_code:
            return None

        # 有实例则直接返回
        if tenant_code in AsyncMultiTenantMongoHolder._tenant_instance_dict:
            return AsyncMultiTenantMongoHolder._tenant_instance_dict.get(tenant_code)

        # 无实例则加锁创建
        AsyncMultiTenantMongoHolder._instance_lock.acquire()
        try:
            # 双重锁校验
            if tenant_code not in AsyncMultiTenantMongoHolder._tenant_instance_dict:
                # 初始化新实例
                inst = AsyncMultiTenantMongo(tenant_code=tenant_code)
                AsyncMultiTenantMongoHolder._tenant_instance_dict[tenant_code] = inst
            if AsyncMultiTenantMongoHolder._instance_lock.locked():
                AsyncMultiTenantMongoHolder._instance_lock.release()
            return AsyncMultiTenantMongoHolder._tenant_instance_dict.get(tenant_code)
        finally:
            try:
                if AsyncMultiTenantMongoHolder._instance_lock.locked():
                    AsyncMultiTenantMongoHolder._instance_lock.release()
            except Exception as e:
                LOGGER.info(e)
