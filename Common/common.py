# -*- coding:utf-8 -*-
# @Author      : FangChao
# @File        : common.py
# @Date        : 2020/12/2 0002
# @Description : xjrw_chain_dashboard

import time
import pytz
import base58
from datetime import datetime
from . import consts


def current_time(time_format=consts.TIME_FORMAT):
    return time.strftime(time_format, time.localtime())


def current_time_iso(tz=None):
    # print(pytz.country_timezones('cn'))
    if tz is None:
        tz = pytz.timezone(consts.TIME_ZONE_CITY_CHONGQING)
    return datetime.now(tz=tz).isoformat('T')  # RFC 3339 ？


def isostr_to_datetime(str):
    return datetime.strptime(str, '%Y-%m-%dT%H:%M:%S.%f%z')
    # .timestamp()
    # datetime.strptime(str, '%Y-%m-%dT%H:%M:%S.%f%z')


def base58_encode(str):
    return bytes.decode(base58.b58encode(str))


def dict_key_exist(m_dict, m_key):
    try:
        test = m_dict[m_key]
        return True
    except:
        return False


def dict_key_not_exist(m_dict, m_key):
    try:
        test = m_dict[m_key]
        return False
    except:
        return True


def create_counter():
    count = 0
    def counter():
        nonlocal count
        count += 1
        return count
    return counter