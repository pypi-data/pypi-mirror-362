"""
Time Utilities

fast approaches to commonly used time/date related functions
"""
import datetime
import math
import time
from typing import Optional

import pytz
from dateutil import tz


def now() -> datetime.datetime:
    """
    get datetime instance of time of now
    :return: time of now
    """
    return datetime.datetime.now(tz.gettz('Asia/Shanghai'))


def __get_t(t: Optional[datetime.datetime] = None) -> datetime.datetime:
    """
    get datetime instance
    :param t: optional datetime instance
    :return: datetime instance
    """
    return t if isinstance(t, datetime.datetime) else now()


def to_str(t: Optional[datetime.datetime] = None,
           fmt: str = '%Y-%m-%d %H:%M:%S.%f') -> str:
    """
    get string formatted time
    :param t: optional datetime instance
    :param fmt: string format
    :return:
    """
    return __get_t(t).strftime(fmt)


def to_seconds(t: Optional[datetime.datetime] = None) -> int:
    """
    datetime to seconds
    :param t: optional datetime instance
    :return: timestamp in seconds
    """
    return int(__get_t(t).timestamp())


def to_milliseconds(t: Optional[datetime.datetime] = None) -> int:
    """
    datetime to milliseconds
    :param t: datetime instance
    :return: timestamp in seconds
    """
    return int(__get_t(t).timestamp() * 10 ** 3)


def to_microseconds(t: Optional[datetime.datetime] = None) -> int:
    """
    datetime to microseconds
    :param t: datetime instance
    :return: timestamp in seconds
    """
    return int(__get_t(t).timestamp() * 10 ** 6)


def get_dt(start_t: datetime.datetime,
           end_t: Optional[datetime.datetime] = None) -> datetime.timedelta:
    """
    get delta time
    :param start_t: start time
    :param end_t: end time
    :return: timedelta instance
    """
    return __get_t(end_t) - start_t


def to_seconds_dt(dt: datetime.timedelta) -> int:
    """
    delta time to seconds
    :param dt: timedelta instance
    :return: seconds elapsed
    """
    return int(dt.total_seconds())


def to_milliseconds_dt(dt: datetime.timedelta) -> int:
    """
    delta time to milliseconds
    :param dt: timedelta instance
    :return: milliseconds elapsed
    """
    return int(dt.total_seconds() * 10 ** 3)


def to_microseconds_dt(dt: datetime.timedelta) -> int:
    """
    delta time to microseconds
    :param dt: timedelta instance
    :return: microseconds elapsed
    """
    return int(dt.total_seconds() * 10 ** 6)


def parse_timestamp(time_str, tz_str='Asia/Shanghai'):
    """
    将时间戳解析成本地时间(自动截断毫秒)
    :param time_str:
    :param tz_str:
    :return:
    """
    if time_str:
        # 1576839034000
        if len(str(time_str)) > 10:
            # 截取掉毫秒
            time_str = str(time_str)[0:10]
        return datetime.datetime.fromtimestamp(int(time_str)).astimezone(tz.gettz(tz_str))


def time_to_batch_no(dt, delta_hour=0, delta_day=0, err=''):
    """
    # 将采购时间转换为批次编号(delta为0时，时间应为iso时间)，delta为正则加为负则减
    """
    try:
        if dt and isinstance(dt, datetime.datetime):
            if delta_hour or delta_day:
                time_delta = datetime.timedelta(hours=int(delta_hour), days=int(delta_day))
                dt = dt + time_delta
            return int(dt.strftime("%Y%m%d"))
    except ValueError:
        return err


def parse_time(time_str, fmt='%Y-%m-%d %H:%M:%S', tz_str='Asia/Shanghai'):
    """
    将时间字符串解析成本地时间
    :param time_str:
    :param fmt:
    :param tz_str:
    :return:
    """
    if time_str:
        return datetime.datetime.strptime(time_str, fmt).astimezone(tz.gettz(tz_str))


def parse_date(time_str, fmt='%Y-%m-%d', tz_str='Asia/Shanghai'):
    """
    将日期字符串解析成本地日期
    :param time_str:
    :param fmt:
    :param tz_str:
    :return:
    """
    if time_str:
        return datetime.datetime.strptime(time_str, fmt).astimezone(tz.gettz(tz_str))


def format_timestamp(time_str, fmt='%Y-%m-%d %H:%M:%S', tz_str='Asia/Shanghai'):
    """
    将时间戳解析成本地时间(自动截断毫秒)
    :param time_str:
    :param tz_str:
    :return:
    """
    if time_str:
        # 1576839034000
        if len(str(time_str)) > 10:
            # 截取掉毫秒
            time_str = str(time_str)[0:10]
        dt = datetime.datetime.fromtimestamp(int(time_str)).astimezone(tz.gettz(tz_str))
        return dt.strftime(fmt)


def format_time(dt, fmt='%Y-%m-%d %H:%M:%S'):
    """
    将时间格式化为字符串
    :param dt:
    :param fmt:
    :return:
    """
    if dt:
        return dt.strftime(fmt)


def format_date(dt, fmt='%Y-%m-%d'):
    """
    将时间格式化为字符串
    :param dt:
    :param fmt:
    :return:
    """
    if dt:
        return dt.strftime(fmt)


def get_timestamp13() -> int:
    """
    获取当前时间的时间戳 13位
    """
    # 生成13时间戳   eg:1540281250399895
    datetime_now = now()

    # 10位，时间点相当于从UNIX TIME的纪元时间开始的当年时间编号
    date_stamp = str(int(time.mktime(datetime_now.timetuple())))

    # 3位，微秒
    data_microsecond = str("%06d" % datetime_now.microsecond)[0:3]

    date_stamp = date_stamp + data_microsecond
    return int(date_stamp)


def add_time(start_time: Optional[datetime.datetime] = None, delta_hour: float = 0,
             delta_day: float = 0) -> datetime.datetime:
    """
    时间计算
    start_time: 起始时间 默认当前时间
    delta_hour: 偏移小时，正数为加，负数为减
    delta_day: 偏移天数，正数为加，负数为减
    """
    if not start_time:
        start_time = now()
    return start_time + datetime.timedelta(hours=delta_hour, days=delta_day)


def calc_range_seconds(start_time: datetime.datetime, end_time: datetime.datetime) -> int:
    """
    时间起止时间之间相差的总秒数
    start_time: 起始时间
    end_time: 结束时间
    """
    if start_time and end_time:
        total_seconds = (end_time - start_time).total_seconds()
        return int(total_seconds)


def calc_range_hour(start_time: datetime.datetime, end_time: datetime.datetime) -> float:
    """
    时间起止时间之间相差的总小时数
    start_time: 起始时间
    end_time: 结束时间
    """
    if start_time and end_time:
        total_seconds = (end_time - start_time).total_seconds()
        return float(int(total_seconds) / 3600)


def calc_range_day(start_time: datetime.datetime, end_time: datetime.datetime) -> int:
    """
    时间起止时间之间相差的总天数，不足一天的舍掉
    start_time: 起始时间
    end_time: 结束时间
    """
    if start_time and end_time:
        return (end_time - start_time).days


def current_timestamp13():
    """
    13位当前时间时间戳（毫秒级时间戳）
    :return:
    """
    return int(round(time.time() * 1000))


def current_timestamp10():
    """
    10位当前时间时间戳（秒级时间戳）
    :return:
    """
    return int(time.time())


def current_time_str(fmt: str = '%Y-%m-%d %H:%M:%S'):
    """
    10位当前时间时间戳（秒级时间戳）
    :return:
    """
    return format_time(now(), fmt)


def format_timestamp10(t: int, fmt: str = '%Y-%m-%d %H:%M:%S'):
    """
    10位当前时间时间戳（秒级时间戳）
    :return:
    """
    dt = parse_timestamp(t)
    return format_time(dt, fmt)


# 将时间转换成时间戳
def time_to_timestamp(time_str, fmt="%Y-%m-%d %H:%M:%S"):
    if time_str:
        timestamp = int(time.mktime((time.strptime(time_str, fmt))))

        return timestamp

    return ''


def get_time_stamp(result):
    '''
    tz时间格式字符串转换为时间戳
    :param result:
    :return:
    '''
    utct_date1 = datetime.datetime.strptime(result, "%Y-%m-%dT%H:%M:%S.%f%z")
    utct_date2 = time.strptime(result, "%Y-%m-%dT%H:%M:%S.%f%z")  # time.struct_time(tm_year=2020, tm_mon=12, tm_mday=1, tm_hour=3, tm_min=21, tm_sec=57, tm_wday=1, tm_yday=336, tm_isdst=-1)
    # print(utct_date1)
    # print(utct_date2)
    # 加上时区
    local_date = utct_date1 + datetime.timedelta(hours=8)
    local_date_srt = datetime.datetime.strftime(local_date, "%Y-%m-%d %H:%M:%S.%f")
    # print(local_date_srt)
    time_array1 = time.mktime(time.strptime(local_date_srt, "%Y-%m-%d %H:%M:%S.%f"))
    time_array2 = int(time.mktime(utct_date2))  # 1606764117
    # print(time_array1)
    # print(time_array2)
    return time_array2


# 获取当前时间到目标时间之间的秒数（用于做过期时间）
def get_second_from_now(end_time):
    if end_time and isinstance(end_time, datetime.datetime):
        if not end_time.tzinfo:
            end_time = end_time.astimezone(pytz.timezone('Asia/Shanghai'))
        total_seconds = (end_time - datetime.datetime.now(pytz.timezone('Asia/Shanghai'))).total_seconds()
        return math.floor(total_seconds)

    return 0


if __name__ == '__main__':
    print(time_to_timestamp('2023-06-27 00:00:00'))
    # print(get_time_stamp("2023-06-29T16:00:00.000Z"))
    # time_str = '2021-05-17'
    # print(time_to_timestamp(time_str))
    # print(parse_timestamp(str(int(now().timestamp()))))
    # print(str(1650591873000)[0:10])
    # print(time_to_timestamp("2023-06-29T16:00:00.000Z"))
