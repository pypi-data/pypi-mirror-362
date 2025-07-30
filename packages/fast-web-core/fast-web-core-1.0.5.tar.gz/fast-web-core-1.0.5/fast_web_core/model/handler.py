from enum import IntEnum
from typing import Dict, Any, List

from ..model.base import ExecRet


class ErrCode(IntEnum):
    """
    error codes
    """
    SUCCESS = 0
    ERROR = -1


class Resp(ExecRet):
    """
    response body
    """
    code: IntEnum = ErrCode.SUCCESS

    @classmethod
    def ok(cls, data: Any = None, msg: str = '操作成功') -> Dict[str, Any]:
        """
        generate success response body
        :param data: data
        :param msg: msg
        :return: json dict resp body
        """
        return cls(
            success=True,
            data=data,
            msg=msg,
            code=ErrCode.SUCCESS
        ).dict()

    @classmethod
    def err(cls, data: Any = None, msg: str = '操作失败', code: IntEnum = ErrCode.ERROR) -> Dict[str, Any]:
        """
        generate error response body with external status code 200
        :param data: data
        :param msg: msg
        :param code: user defined (not http) status code
        :return: json dict resp body
        """
        if code == ErrCode.SUCCESS:
            code = ErrCode.ERROR
        return cls(
            success=False,
            data=data,
            msg=msg,
            code=code
        ).dict()

    @classmethod
    def page(cls, rows: List = [], total_count: int = 0, msg: str = '操作成功') -> \
            Dict[
                str, Any]:
        """
        generate page response body
        :param rows:
        :param total:
        :param msg:
        :return:
        """
        return cls(
            success=True,
            data={'list': rows, 'total': total_count},
            msg=msg,
            code=ErrCode.SUCCESS
        ).dict()

    @staticmethod
    def is_success(result: Dict) -> bool:
        """
        判断响应是否为成功
        :param result:
        :return:
        """
        if not result or not result.get('success', False):
            return False

        return True

    @staticmethod
    def get_data(result: dict, force: bool = False) -> object:
        """
        判断响应是否为成功
        :param result: 响应结果
        :param force: 是否跳过响应状态验证
        :return:
        """
        if not force:
            if not Resp.is_success(result):
                return None

        return result.get('data', None)
