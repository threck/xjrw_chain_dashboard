# -*- coding:utf-8 -*-
# @Author      : FangChao
# @File        : gen_data.py
# @Date        : 2020/12/22 0022
# @Description : xjrw_chain_dashboard

import asyncio
import threading
import websockets
import json
import time
import copy
from multiprocessing import Pool
from Common import common
from Common import mrequest
from Common import log
from Stress.Conf import config
from Stress.Common import consts
from Stress.Data import data
from Stress.Data import templates
from Stress.HttpRequest import post

logger = log.Log()


# create r chain key
def create_r_and_s_chain_key(chain_nu_local):
    chain_nu_r_local = chain_nu_local["R"]
    chain_key_r_local = []
    chain_key_s_local = []
    s = len(consts.CHAIN_KEYS_R)
    for x in range(s, s+chain_nu_r_local):
        chain_key_r = hex(x).split('x')[1].upper().rjust(2, '0')
        chain_key_r_local.append(chain_key_r)
        consts.CHAIN_KEYS_R.append(chain_key_r)
        s_chain_key = create_s_chain_key(chain_nu_local, chain_key_r)
        chain_key_s_local.extend(s_chain_key)
    return (chain_key_r_local, chain_key_s_local)


def create_s_chain_key(chain_nu_local, chain_key_r):
    chain_key_s_local = []
    r_total = chain_nu_local["R"]
    s_total = chain_nu_local["S"]
    s_nodes_nu = int(s_total / r_total)
    for i in range(s_nodes_nu):
        chainKey_s = '%s%s' % (chain_key_r, hex(i).split('x')[1].upper().rjust(2, '0'))
        chain_key_s_local.append(chainKey_s)
        consts.CHAIN_KEYS_S.append(chain_key_r)
    return chain_key_s_local





