# -*- coding: utf-8 -*-
class BizException(Exception):
    def __init__(self, message: str, code: int = -1):
        self.message = message
        self.code = code


class NoAuthException(Exception):
    def __init__(self, message: str = '权限不足'):
        self.message = message
        self.code = 401


# 系统错误类异常
class SystemException(Exception):
    def __init__(self, message: str = '系统异常，请联系管理员处理'):
        self.message = message
        self.code = 500


# 系统参数为配置
class NoConfigException(SystemException):
    def __init__(self, message: str = '系统参数配置异常'):
        self.message = message
        self.code = 500


class MQConnectionException(SystemException):
    """RabbitMQ连接异常"""
    def __init__(self, message="MQ connection failed"):
        super().__init__(message)

