# -*- coding: utf-8 -*-
import aio_pika
from tenacity import retry, wait_exponential, stop_after_attempt
from ..exception.exceptions import NoConfigException
from ..lib import cfg, logger

LOGGER = logger.get('AsyncRabbitClient')


class AsyncRabbitClient:
    def __init__(self, connection_uri: str = None):
        self.connection_uri = connection_uri or cfg.get('RABBITMQ_URI')
        if not self.connection_uri:
            raise NoConfigException('RABBITMQ_URI not configured!')
        self.connection = None
        self.channel = None
        self.reconnect_max_retries = 5
        self.reconnect_wait_base = 2

    @retry(
        wait=wait_exponential(multiplier=1, max=10),
        stop=stop_after_attempt(5),
        reraise=True
    )
    async def connect(self):
        """建立带有自动重连的RabbitMQ连接"""
        LOGGER.info(f'Connecting to RabbitMQ: {self.connection_uri}')
        try:
            self.connection = await aio_pika.connect_robust(
                self.connection_uri,
                timeout=10
            )
            self.channel = await self.connection.channel()
            await self.channel.set_qos(prefetch_count=10)
            LOGGER.info('RabbitMQ connection established')
        except Exception as e:
            LOGGER.error(f'Connection failed: {str(e)}')
            raise

    async def get_channel(self):
        """获取有效通道（带健康检查）"""
        if not self.connection or self.connection.is_closed:
            await self.reconnect()
        return self.channel

    async def reconnect(self):
        """自动重连机制"""
        LOGGER.warning('Attempting to reconnect...')
        print(f'---------------> reconnect.....')
        try:
            if self.connection and not self.connection.is_closed:
                await self.connection.close()
            await self.connect()
        except Exception as e:
            LOGGER.error(f'Reconnect failed: {str(e)}')
            raise

    async def close(self):
        """安全关闭连接"""
        if self.connection and not self.connection.is_closed:
            await self.connection.close()
            LOGGER.info('Connection closed gracefully')

    async def __aenter__(self):
        """异步上下文管理器入口"""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        """异步上下文管理器出口"""
        await self.close()
