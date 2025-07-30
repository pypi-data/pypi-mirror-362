# encoding:utf-8
from enum import Enum


class UserStatus(int, Enum):
    """
    batch status enum
    """
    # 正常
    NORMAL = 1
    # TODO 待确定 -> 锁定/冻结
    LOCKED = 2


class UserGender(int, Enum):
    """
    gender enum
    """
    # 男
    MALE = 1
    # 女
    FEMALE = 2
    # 保密
    SECRET = 3
