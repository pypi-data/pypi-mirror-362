import uuid
import traceback
from typing import List
from starlette.requests import Request
from starlette.responses import StreamingResponse, JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from ..auth.share_auth import ShareAuth
from ..exception.exceptions import NoAuthException
from ..lib import logger
from ..model.handler import ErrCode
from ..context.context_vars import tenant_context

# 固定白名单
WHITELIST = [
]

LOGGER = logger.get('鉴权中间件')
share_auth = ShareAuth()


class AuthMiddleware(BaseHTTPMiddleware):
    """ 鉴权中间件 """

    def __init__(self, app, whitelist: List[str] = None):
        self.FASTAPI_APP = app.app
        if whitelist:
            WHITELIST.extend(whitelist)
        super().__init__(app)

    async def dispatch(self, request: Request, next_func) -> Response:
        """
        接口鉴权
        :param request:
        :param next_func:
        :return:
        """
        try:
            rs = share_auth.reload(self.FASTAPI_APP.routes, WHITELIST).auth_check(request)
            if rs:
                # 挂载
                tenant_context.set(share_auth.get_auth_team_sn(request))
                # 执行
                resp: StreamingResponse = await next_func(request)
                return resp
            return JSONResponse({'success': False, 'msg': '无权访问', 'code': ErrCode.ERROR}, status_code=403)
        except NoAuthException as na_ex:
            return JSONResponse({'success': False, 'msg': na_ex.message, 'code': ErrCode.ERROR}, status_code=401)
        except Exception as ex:
            req_id = str(uuid.uuid4())
            LOGGER.error(f'[requestId={req_id}] {traceback.format_exc()}')
            return JSONResponse({'success': False, 'msg': f'服务异常[requestId={req_id}]', 'code': ErrCode.ERROR}, status_code=500)
        finally:
            # 清理
            tenant_context.set(None)
