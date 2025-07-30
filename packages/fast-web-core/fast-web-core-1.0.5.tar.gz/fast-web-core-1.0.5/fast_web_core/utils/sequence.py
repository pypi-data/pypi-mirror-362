# -*- coding: UTF-8 -*-
"""常用工具类"""
import random
import uuid
from datetime import datetime


# 生成批次编号
def gen_batch_id():
    # 时间(3位毫秒)+随机数(3位)
    # return f"{datetime.now().strftime('%y%m%d%H%M%S%f')[0:10]}{random.randint(1000, 9999)}"
    return f"{datetime.now().strftime('%y%m%d%H%M%S')}{random.randint(1000, 9999)}"


# 生成消息编号
def gen_msg_id():
    # 时间(3位毫秒)+随机数(3位)
    # return f"{datetime.now().strftime('%y%m%d%H%M%S%f')[0:10]}{random.randint(1000, 9999)}"
    # return f"{datetime.now().strftime('%y%m%d%H%M%S%f')}{random.randint(1000, 9999)}"
    return uuid.uuid4().hex


def gen_random_code(n=8, alpha=True):
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


# 测试
if __name__ == '__main__':
    while True:
        print(gen_msg_id())
