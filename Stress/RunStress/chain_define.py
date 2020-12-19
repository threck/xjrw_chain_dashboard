# -*- coding:utf-8 -*-
# @Author      : FangChao
# @File        : demon.py
# @Date        : 2020/12/14 0014
# @Description : xjrw_chain_dashboard


class Nodes(object):
    B = 1
    R = 2
    S = 4
    distribution = ['192.168.0.30', '192.168.0.30']
    ws_addr = 'ws://192.168.0.30:5678'


class B(object):
    Type = 'B'
    ChainKey = 'B'
    NodeId = '12D3KooWGKa86zkRz11uFp7kja4FujbQYnTt7qZQQMGfo000000B'
    Hash = '0x9fe109fec8b1751e4fae65e2bbaa6a31c580bac257436c43800a12f4217b010b'

    def send_post(self):
        print(f'{B.Type} post request send over')


class R(object):
    Type = 'R'
    ChainKey = 'R00'
    NodeId = '12D3KooWGKa86zkRz11uFp7kja4FujbQYnTt7qZQQMGfo0000R00'
    Hash = '0x9fe109fec8b1751e4fae65e2bbaa6a31c580bac257436c43800a12f4217b010b'

    def send_post(self):
        print(f'{R.Type} post request send over')


class S(object):
    Type = 'R'
    ChainKey = 'S0000'
    NodeId = '12D3KooWGKa86zkRz11uFp7kja4FujbQYnTt7qZQQMGfo00S0000'

    def send_post(self):
        print(f'{S.Type} post request send over')

