# encoding: utf-8
# version: pymongo==4.7.3, motor==3.5.0

from ..exception.exceptions import BizException
from ..exception.exceptions import NoConfigException
from ..lib import cfg, logger

LOGGER = logger.get('AsyncMongoClient')


class AsyncMongo(object):
    def __init__(self, mongo_uri: str = None, mongo_db: str = None):
        import motor.motor_asyncio
        self.mongo_uri = mongo_uri or cfg.get('MONGO_URL')
        self.mongo_db = mongo_db or cfg.get('MONGO_DB')
        if not self.mongo_uri:
            raise NoConfigException('mongodb uri not config!')
        if not self.mongo_db:
            raise NoConfigException('mongodb database not config!')

        self.client = motor.motor_asyncio.AsyncIOMotorClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

        LOGGER.info(self.client)

    # 获取集合
    def get_collection(self, coll):
        # 非异步
        return self.db.get_collection(coll)

    # 查询对象
    async def get(self, collection, query={}):
        return await self.db[collection].find_one(query)

    # 统计数量
    async def count(self, collection, query={}):
        return await self.db[collection].count_documents(query)

    # 查询列表
    async def list(self, collection, query={}, fields=None, sort=[], batch_size: int = 2000):
        result = []
        cursor = self.db[collection].find(filter=query, projection=fields, sort=sort)
        cursor.batch_size(batch_size)
        async for document in cursor:
            result.append(document)
        await cursor.close()

        return result

    async def list_with_cursor(self, collection, query={}, fields=None, sort=[], batch_size: int = 2000):
        """
        样例:
            cursor = await aio_mongo.list_with_cursor(collection)
            async for document in cursor:
                print("document =", document)
            await cursor.close()
        注意：应该在使用完毕后主动关闭 cursor
        """
        cursor = self.db[collection].find(filter=query, projection=fields, sort=sort)
        cursor.batch_size(batch_size)

        return cursor

    # 分页查询
    async def page(self, collection, query={}, page_no=1, page_size=20, fields=None, sort=[], batch_size: int = 2000):
        total = await self.db[collection].count_documents(query) or 0
        cursor = self.db[collection].find(query, fields, sort=sort).skip(page_size * (page_no - 1)).limit(page_size)
        cursor.batch_size(batch_size)
        rows = []
        async for document in cursor:
            rows.append(document)
        await cursor.close()

        return rows, total

    # 查询列表前N个
    async def top(self, collection, query={}, sort=[], limit=1, fields=None, batch_size: int = 2000):
        cursor = self.db[collection].find(filter=query, projection=fields, sort=sort, limit=limit)
        cursor.batch_size(batch_size)
        rows = []
        async for document in cursor:
            if limit == 1:
                return document
            rows.append(document)
        await cursor.close()

        return rows

    # 查询去重列表
    async def distinct(self, collection, dist_key, query={}, fields=None):
        return await self.db[collection].find(query, fields).distinct(dist_key)

    # 含分页聚合查询
    async def aggregate_page(self, collection, pipelines, page_no=1, page_size=20):
        skip = page_size * (page_no - 1)
        if pipelines:
            pipelines.append({'$facet': {'total': [{'$count': 'count'}], 'rows': [{'$skip': skip}, {'$limit': page_size}]}})
            pipelines.append({'$project': {'data': '$rows', 'total': {'$arrayElemAt': ['$total.count', 0]}}})

            cursor = self.db[collection].aggregate(pipelines, session=None, allowDiskUse=True)
            cursor.batch_size(page_size)
            async for rs in cursor:
                # rs: dict as {"data": [], "total": int}
                if rs and 'data' in rs and 'total' in rs:
                    await cursor.close()
                    return rs.get('data'), rs.get('total')
            await cursor.close()
        return [], 0

    # 聚合查询
    async def aggregate(self, collection, pipelines=[], batch_size: int = 2000):
        """
        样例:
            cursor = await aio_mongo.aggregate(collection="collection_name", pipelines=[])
            async for row in cursor:
                print(row)

            await cursor.close()
        注意：应该在使用完毕后主动关闭 cursor
        """
        cursor = self.db[collection].aggregate(pipelines, session=None, allowDiskUse=True)
        cursor.batch_size(batch_size)
        return cursor

    # 查询分页列表,还没找到实际应用
    async def list_with_page(self, collection, query={}, page_size=10000, fields=None):
        # 没有用到
        rows = list()
        total = await self.db[collection].count_documents(query)
        if total > 0 and page_size > 0:
            total_page = round(total / page_size) + 1
            for page in range(0, total_page):
                if fields:
                    cursor = self.db[collection].find(query, fields).skip(page_size * page).limit(page)
                else:
                    cursor = self.db[collection].find(query).skip(page_size * page).limit(page)
                async for document in cursor:
                    rows.append(document)
                await cursor.close()
        return rows

    # 插入或更新
    async def insert_or_update(self, collection, data, id_key='_id', update=None, upsert=True, multi=False):
        if not multi:
            if data and not update:
                result = await self.db[collection].update_one({id_key: data[id_key]}, {'$set': data}, upsert=upsert)
            elif not data and update:
                result = await self.db[collection].update_one({id_key: data[id_key]}, update, upsert=upsert)
            else:
                # all([data, update]) or not all([data, update])
                raise BizException("data和update不能同时存在或同时为空")
        else:
            if data and not update:
                result = await self.db[collection].update_many({id_key: data[id_key]}, {'$set': data}, upsert=upsert)
            elif not data and update:
                result = await self.db[collection].update_many({id_key: data[id_key]}, update, upsert=upsert)
            else:
                raise BizException("data和update不能同时存在或同时为空")

        return result

    # 插入
    async def insert(self, collection, data):
        return await self.db[collection].insert_one(data)

    # 更新
    async def update(self, collection, filter, data=None, update=None, multi=False):
        if multi:
            if data and not update:
                result = await self.db[collection].update_many(filter, {'$set': data})
            elif not data and update:
                result = await self.db[collection].update_many(filter, update)
            else:
                raise BizException("data和update不能同时存在或同时为空")
        else:
            if data and not update:
                result = await self.db[collection].update_one(filter, {'$set': data})
            elif not data and update:
                result = await self.db[collection].update_one(filter, update)
            else:
                raise BizException("data和update不能同时存在或同时为空")

        return result

    # 原生保存方法
    async def save(self, collection, filter: dict, save_data: dict, upsert=True):
        return await self.db[collection].update_one(filter, {'$set': save_data}, upsert=upsert)

    # 以主键更新
    async def update_by_pk(self, collection, pk_val, data=None, update=None, upsert=False):
        if data and not update:
            result = await self.db[collection].update_one({'_id': pk_val}, {'$set': data}, upsert=upsert)
        elif not data and update:
            result = await self.db[collection].update_one({'_id': pk_val}, update, upsert=upsert)
        else:
            raise BizException("data和update不能同时存在或同时为空")
        return result

    # 批量更新
    async def batch_update(self, collection, filter, datas=None, update=None, *args, **kwargs):
        if datas and not update:
            result = await self.db[collection].update_many(filter, {'$set': datas})
        elif not datas and update:
            result = await self.db[collection].update_many(filter, update)
        else:
            raise BizException("data和update不能同时存在或同时为空")
        return result

    # 删除
    async def delete(self, collection, filter):
        return await self.db[collection].delete_many(filter)

    # 插入或更新
    async def bulk_write(self, collection, bulk_list: list, batch_size: int = 1000):
        result = None
        if bulk_list:
            bulk_lists = [bulk_list[i: i + batch_size] for i in range(0, len(bulk_list), batch_size)]
            for _bulk_list in bulk_lists:
                result = await self.db[collection].bulk_write(_bulk_list, ordered=False, bypass_document_validation=True)
        return result

    # 创建索引
    async def create_index(self, collection, fields):
        return await self.db[collection].create_index(fields)

    def close(self):
        if self.client:
            try:
                self.client.close()
                print("close successful")
            except Exception as e:
                print("close mongo client catch err:", e)

