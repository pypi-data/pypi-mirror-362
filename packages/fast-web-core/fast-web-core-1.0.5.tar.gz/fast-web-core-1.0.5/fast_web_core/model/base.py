"""
Basic models
"""
from typing import Tuple, Any
from pydantic import BaseModel

# basic function call return value, with only success flag and err msg
PCallRet = Tuple[bool, str]


class ExecRet(BaseModel):
    """
    basic ret value for executing a specific task
    """
    success: bool = True
    msg: str = ''
    data: Any = None

    @classmethod
    def ok(cls, **kwargs):
        return cls(success=True, **kwargs)

    @classmethod
    def err(cls, **kwargs):
        return cls(success=False, **kwargs)
