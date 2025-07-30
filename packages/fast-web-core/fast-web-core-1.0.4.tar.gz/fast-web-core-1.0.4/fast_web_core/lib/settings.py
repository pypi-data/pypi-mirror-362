import asyncio
import copy
from ..client.async_mongo_client import AsyncMongo
from ..lib import logger
from ..exception.exceptions import SystemException


class DynamicSettings(object):
    """
    简易配置管理器
    """
    # 主键索引
    row_map = {}
    # 组索引
    group_map = {}

    def __init__(self, collection: str, primary_field: str = '_id', group_field: str = None, value_field: str = None, mongo: AsyncMongo = None, name: str = None, entity_class=None):
        self.logger = logger.get(name or '配置')
        self.collection = collection
        self.primary_field = primary_field or '_id'
        self.value_field = value_field
        self.group_field = group_field
        self.entity_class = entity_class

        if not self.collection:
            raise SystemException(f'[collection]集合未指定: id={id}, collection={self.collection}, primary_field={self.primary_field}, group_field={self.group_field}, value_field={self.value_field}')

        self.mongo = mongo or AsyncMongo()
        asyncio.create_task(self.reload())

    async def get_value(self, key):
        if not self.value_field:
            self.logger.error(f'[value_field]字段未指定: collection={self.collection}, primary_field={self.primary_field}, group_field={self.group_field}, value_field={self.value_field}')
            return None

        row = self.row_map.get(key)
        if row:
            val = row.get(self.value_field, None)
            return copy.deepcopy(val)

        return None

    async def get_row(self, key):
        row = self.row_map.get(key, None)

        return copy.deepcopy(row)

    async def get_all(self):
        rows = [*self.row_map.values()]

        return copy.deepcopy(rows)

    async def get_rows_by_group(self, group_key):
        if not self.group_field:
            self.logger.error(f'[group_field]字段未指定: collection={self.collection}, primary_field={self.primary_field}, group_field={self.group_field}, value_field={self.value_field}')
            return None

        rows = self.group_map.get(group_key, None)

        return copy.deepcopy(rows)

    async def reload(self):
        items = await self._fetch_items()
        hot_row_map = {}
        hot_group_map = {}
        for item in items:
            item_obj = item
            if self.entity_class:
                item_obj = self.entity_class(**item)
            id = item.get(self.primary_field, None)
            # 增加禁用功能（可选）
            if 'enable' in item and item.get('enable', None) != 1:
                self.logger.warning(f'禁用配置: id={id}, collection={self.collection}, primary_field={self.primary_field}, value_field={self.value_field}')
                continue

            # 主键索引
            if id:
                hot_row_map[id] = item_obj
            else:
                self.logger.warning(f'异常配置: id={id}, collection={self.collection}, primary_field={self.primary_field}, value_field={self.value_field}')

            # 分组索引
            if self.group_field:
                group_key = item.get(self.group_field, None)
                if group_key:
                    if group_key not in hot_group_map:
                        hot_group_map[group_key] = list()
                    rows = hot_group_map.get(group_key)
                    rows.append(item_obj)

        self.row_map = hot_row_map
        self.group_map = hot_group_map

        self.logger.info(f'更新配置: row={len(self.row_map.keys())}条 group={len(self.group_map.keys())}条, collection={self.collection}, primary_field={self.primary_field}, value_field={self.value_field}, group_field={self.group_field}')

    async def _fetch_items(self):
        try:
            rs = await self.mongo.list(collection=self.collection, query={})
            return rs
        except Exception as e:
            self.logger.error(e)

        return []
