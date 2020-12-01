# -*- coding:utf-8 -*-
# 按照模块封装测试数据


def get_parameter(self, yaml_type):
    pass


class Basic(object):
    params = get_parameter('Basic')
    url = []
    data = []
    header = []
    for i in range(len(params)):
        url.append(params[i]['url'])
        data.append(params[i]['data'])
        header.append(params[i]['header'])


