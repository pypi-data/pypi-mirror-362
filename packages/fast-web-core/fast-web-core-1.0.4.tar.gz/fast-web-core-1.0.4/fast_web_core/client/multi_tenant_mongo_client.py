# -*- coding: utf-8 -*-
import threading
from ..client.mongo_client import Mongo
from ..lib import cfg, logger

LOGGER = logger.get('MultiTenantMongo')


class MultiTenantMongo(Mongo):
    """
    多租户Mongo客户端简易封装
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


class MultiTenantMongoHolder(object):
    """
    多租户Mongo客户端持有器（租户数据库连接池）
    """
    _instance_lock = threading.Lock()
    _tenant_instance_dict = dict()

    def __new__(cls, *args, **kwargs):
        if not hasattr(MultiTenantMongoHolder, "_instance"):
            with MultiTenantMongoHolder._instance_lock:
                if not hasattr(MultiTenantMongoHolder, "_instance"):
                    MultiTenantMongoHolder._instance = object.__new__(cls)
        return MultiTenantMongoHolder._instance

    @staticmethod
    def get_tenant_mongo(tenant_code) -> MultiTenantMongo:
        if not tenant_code:
            return None

        # 有实例则直接返回
        if tenant_code in MultiTenantMongoHolder._tenant_instance_dict:
            return MultiTenantMongoHolder._tenant_instance_dict.get(tenant_code)

        # 无实例则加锁创建
        MultiTenantMongoHolder._instance_lock.acquire()
        try:
            # 双重锁校验
            if tenant_code not in MultiTenantMongoHolder._tenant_instance_dict:
                # 初始化新实例
                inst = MultiTenantMongo(tenant_code=tenant_code)
                MultiTenantMongoHolder._tenant_instance_dict[tenant_code] = inst
            return MultiTenantMongoHolder._tenant_instance_dict.get(tenant_code)
        finally:
            MultiTenantMongoHolder._instance_lock.release()
