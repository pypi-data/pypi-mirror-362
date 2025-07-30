# -*- coding: utf-8 -*-
import contextvars

# 租户环境变量
tenant_context = contextvars.ContextVar('tenant')

# # 当前登录用户环境变量
# auth_user_context = contextvars.ContextVar('auth_user')

# 非主线程的事件循环环境变量
event_loop_context = contextvars.ContextVar('event_loop')
