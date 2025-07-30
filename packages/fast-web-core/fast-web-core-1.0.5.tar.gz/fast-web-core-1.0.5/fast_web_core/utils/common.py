# -*- coding: UTF-8 -*-
"""常用工具类"""
import math
import re
import random

import platform
import pprint
import typing
from typing import Any, Tuple, Optional

T = typing.TypeVar('T')

# global encoding
ENCODING = 'utf-8'


def as_int(o: Any) -> Tuple[int, Optional[Exception]]:
    """
    object to int
    :param o: object
    :return: int value, err
    """
    try:
        return int(o), None
    except Exception as e:
        return 0, e


def as_float(o: Any) -> Tuple[float, Optional[Exception]]:
    """
    object to float
    :param o: object
    :return: float value, err
    """
    try:
        return float(o), None
    except Exception as e:
        return 0.0, e


def is_win() -> bool:
    """
    is currently running on windows
    :return: if current system is of Windows family
    """
    return platform.system().lower().startswith('win')


def pfmt(o: Any, *args, **kwargs) -> str:
    """
    pretty format object
    :param o: object
    :return: object string
    """
    return pprint.pformat(o, *args, **kwargs)


def parse_number(s, err=0):
    """
    解析数字，如果解析失败返回默认值
    :param s:
    :param err:
    :return:
    """
    try:
        val = s
        if isinstance(s, str):
            s = s.replace('¥', '').replace('￥', '').replace(',', '').replace('元', '').strip()
            val = float(s)
        # 防止NaN值出现（如excel中）
        if math.isnan(val):
            return err
        return val
    except ValueError:
        return err
    except Exception:
        return err


def parse_int(s, err=0):
    """
    解析整型数字，如果解析失败返回默认值
    :param s:
    :param err:
    :return:
    """
    try:
        if isinstance(s, str):
            s = s.replace('¥', '').replace('￥', '').replace(',', '').replace('元', '').strip()
        return int(s)
    except ValueError:
        return err
    except TypeError:
        return err


def join_dict(kv):
    """
    将dict键值对拼接成字符串
    :param kv:
    :return:
    """
    s = ''
    for (k, v) in kv.items():
        s += k + ': ' + v + '\r\n'
    return s.strip()


def random_code(n=5, alpha=True):
    """
    生成验证码
    :param n:
    :param alpha:
    :return:
    """
    s = ''  # 创建字符串变量,存储生成的验证码
    for i in range(n):  # 通过for循环控制验证码位数
        num = random.randint(0, 9)  # 生成随机数字0-9
        if alpha:  # 需要字母验证码,不用传参,如果不需要字母的,关键字alpha=False
            upper_alpha = chr(random.randint(65, 90))
            lower_alpha = chr(random.randint(97, 122))
            num = random.choice([num, upper_alpha, lower_alpha])
        s = s + str(num)
    return s


def match_ip_port(txt):
    """
    解析IP和端口
    :param txt:
    :return:
    """
    # /frontBrands/getBrandsAndProductInfos.action?orderBy=normal&shopInfoId=1
    if txt:
        arr = re.findall(r'(?:(?:[0,1]?\d?\d|2[0-4]\d|25[0-5])\.){3}(?:[0,1]?\d?\d|2[0-4]\d|25[0-5]):\d{0,5}',
                         txt.strip())
        if len(arr):
            return arr[0].strip()
    return ''


def list_of_groups(init_list, childern_list_len):
    """
    列表分割成多个小列表
    :param init_list:
    :param childern_list_len:
    :return:
    """
    list_of_groups = zip(*(iter(init_list),) * childern_list_len)
    end_list = [list(i) for i in list_of_groups]
    count = len(init_list) % childern_list_len
    end_list.append(init_list[-count:]) if count != 0 else end_list
    return end_list


if __name__ == '__main__':
    # print(half_split_float_range(5, 8))
    # print(half_split_int_range(3, 6))
    # print(half_split_int_range(3, 5))
    # print(half_split_int_range(3, 4))
    # print(get_timestamp13())
    # print(format_timestamp(int(time.time() * 1000), fmt="%Y/%m/%d"))
    pass
