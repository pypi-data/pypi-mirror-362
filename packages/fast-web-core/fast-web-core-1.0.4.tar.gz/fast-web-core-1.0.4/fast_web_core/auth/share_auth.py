# -*- coding: utf-8 -*-
import logging
import re
import json
import threading
from typing import Optional, List
from starlette.routing import BaseRoute
from fastapi.routing import APIRoute
from starlette.requests import Request

from ..lib import cfg
from ..auth import auth_cache_pool
from ..client.redis_client import Redis
from ..exception.exceptions import NoAuthException
from ..model.items import AuthUser, AuthApp
from ..context.context_vars import tenant_context

logger = logging.getLogger(__name__)

FIX_WHITELIST = [
]


class ShareAuth(object):
    _instance_lock = threading.Lock()
    _biz_inited = False
    _routes_inited = False

    def __new__(cls, *args, **kwargs):
        if not hasattr(ShareAuth, "_instance"):
            with ShareAuth._instance_lock:
                if not hasattr(ShareAuth, "_instance"):
                    ShareAuth._instance = object.__new__(cls)
        return ShareAuth._instance

    def __init__(self):
        if not self._biz_inited:
            self._biz_inited = True
            self.rds = Redis(redis_uri=cfg.get('AUTH_REDIS_URL', None), redis_db=cfg.get('AUTH_REDIS_DB', None)).client
            # route path regex -> tags
            self.regex_to_tags_map = dict()
            # no auth path whitelist
            self.auth_whitelist = []

    def get_access_token(self, request: Request):
        """
        解析请求头鉴权信息
        :param request:
        :return:
        """
        if request and (request.headers or request.query_params):
            access_token = request.headers.get('Authorization', '').replace('Bearer ', '')
            if not access_token:
                access_token = request.cookies.get('access_token')
            if not access_token:
                access_token = request.query_params.get('access_token')
            return access_token

        return ''

    def reload(self, routes: Optional[List[BaseRoute]], white_list=[], force: bool = False):
        if not force and self._routes_inited:
            return self
        # 构造路由匹配正则与权限颗粒(tags)映射
        _tmp_regex_to_tags_map = dict()
        for route in routes:
            if isinstance(route, APIRoute) and route.path_regex:
                _tmp_regex_to_tags_map[route.path_regex] = route.tags
        self.regex_to_tags_map.clear()
        self.regex_to_tags_map = _tmp_regex_to_tags_map
        logger.info(f'reload path to tags map: {len(self.regex_to_tags_map)}')

        # 构造权限白名单
        _auth_whitelist = list()
        for row in FIX_WHITELIST:
            _auth_whitelist.append(re.compile(row))
        for row in white_list:
            _auth_whitelist.append(re.compile(row))
        self.auth_whitelist.clear()
        self.auth_whitelist = _auth_whitelist
        logger.info(f'reload no auth whitelist: {len(self.auth_whitelist)}')
        #
        self._routes_inited = True

        return self

    def access_check(self, request: Request):
        """
        登录校验
        :param request:
        :return:
        """
        access_token = self.get_access_token(request)
        if not access_token:
            raise NoAuthException('请先登录')

        if not auth_cache_pool.has_access(access_token):
            raise NoAuthException('登录信息已失效')

        return access_token

    def auth_check(self, request: Request):
        """
        权限校验
        :param request:
        :return:
        """
        if not self.regex_to_tags_map:
            logger.debug(f'no path to tags map')
            return False
        # 优先处理白名单
        for white_regex in self.auth_whitelist:
            if white_regex.match(request.url.path):
                return True
        # 先校验登录
        access_token = self.access_check(request)
        for regex in self.regex_to_tags_map.keys():
            if regex.match(request.url.path):
                # 匹配到路由
                tags = self.regex_to_tags_map.get(regex)
                if tags:
                    # 需要登录且需要鉴权
                    auth_rs = self._rds_permissions_check(tags, access_token)
                    if not auth_rs:
                        raise NoAuthException('权限不足')
                    return True
                else:
                    # 仅登录无需鉴权
                    return True

        return False

    def _rds_permissions_check(self, tags, access_token) -> bool:
        # redis权限查询
        for tag in tags:
            # 新权限颗粒 xx.xx.xx.xx
            has = auth_cache_pool.has_permission(access_token, tag)
            if not has:
                # 兼容Java版权限颗粒 "xx.xx.xx.xx"
                has = auth_cache_pool.has_permission(access_token, json.dumps(tag))
                if not has:
                    return False

        return True

    def get_auth_user(self, request: Request) -> Optional[AuthUser]:
        """
        获取当前登录的用户信息
        :param request:
        :return:
        """
        access_token = self.get_access_token(request)
        if not access_token:
            raise NoAuthException('请先登录')
        if not auth_cache_pool.has_access(access_token):
            raise NoAuthException('登录信息已失效')

        auth_user = auth_cache_pool.get_cached_user(access_token)

        # 设置租户上下文
        if auth_user and auth_user.team_id:
            tenant_context.set(auth_user.team_id)

        return auth_user

    def get_auth_app(self, request: Request) -> Optional[AuthApp]:
        """
        获取当前登录的应用信息
        :param request:
        :return:
        """
        access_token = self.get_access_token(request)
        if not access_token:
            raise NoAuthException('请先登录')
        if not auth_cache_pool.has_app_access(access_token):
            raise NoAuthException('登录信息已失效')

        auth_app = auth_cache_pool.get_cached_app(access_token)

        return auth_app

    def get_auth_team_sn(self, request: Request) -> Optional[str]:
        """
        获取授权用户所属租户
        :param request:
        :return:
        """
        access_token = self.get_access_token(request)
        if access_token:
            access_item = auth_cache_pool.get_cached_access_dict(access_token)
            if access_item:
                # 仅超级管理员可以切换租户
                team_sn = access_item.get('team_sn', None)
                if team_sn:
                    return team_sn

        return ''


# 用于handler来Depends，获取授权用户
async def authed_user(request: Request) -> Optional[AuthUser]:
    return ShareAuth().get_auth_user(request)


# 用于handler来Depends，获取授权APP信息
async def authed_app(request: Request) -> Optional[AuthApp]:
    return ShareAuth().get_auth_app(request)


# 用于handler来Depends，获取授权用户
async def access_token(request: Request) -> Optional[str]:
    return ShareAuth().get_access_token(request)




