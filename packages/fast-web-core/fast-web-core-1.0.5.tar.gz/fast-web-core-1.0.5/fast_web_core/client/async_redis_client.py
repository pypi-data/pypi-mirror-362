# encoding: utf-8
# version: redis==5.0.7

from ..lib import cfg, logger
from ..exception.exceptions import NoConfigException

LOGGER = logger.get("AsyncRedisClient")


class AsyncRedis(object):

    def __init__(self, redis_uri=None, redis_db=None, decode_responses=True):
        from redis import asyncio as aioredis
        self.redis_uri = redis_uri
        self.redis_db = redis_db
        if not self.redis_uri:
            self.redis_uri = cfg.get("REDIS_URL")
        if not self.redis_db:
            self.redis_db = cfg.get("REDIS_DB")

        if not self.redis_uri:
            raise NoConfigException("redis_uri not config!")
        if not self.redis_db:
            raise NoConfigException("redis_db not config!")

        self.client = aioredis.Redis.from_url(url=self.redis_uri, db=self.redis_db, decode_responses=decode_responses)
        LOGGER.info(f'init async redis client: uri={self.redis_uri}, db={self.redis_db}')

    def __str__(self):
        return f"AsyncRedis client at: {self.redis_uri}/{self.redis_db}"

    async def close(self):
        if self.client:
            try:
                await self.client.aclose()
            except Exception as e:
                print(e)
