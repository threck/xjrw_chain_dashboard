# -*- coding:utf-8 -*-
# @Author      : FangChao
# @File        : post.py
# @Date        : 2020/12/22 0022
# @Description : xjrw_chain_dashboard

import asyncio
import threading
import websockets
import json
import time
import copy
from Stress.Conf import config
from Common import common
from Common import mrequest
from Common import log
from Stress.Data import data
from Stress.Data import templates
from multiprocessing import Pool

logger = log.Log()


def send_post(req_data):
    logger.info('running %s_post ...' % req_data['type'])
    api_url = config.POST_URL
    header = templates.header
    request = mrequest.Request()
    # logger.info(f'post request data: {req_data}')
    resp = request.post_request(api_url, req_data, header)
    logger.info(f'post response data: {resp}')
    # logger.info(f"post response time: {resp['time_consuming']}")
    logger.info('running %s_post over ...' % req_data['type'])



def send_post_request_threading(chains):
    th = []
    if chains:
        for da_r in chains:
            th.append(threading.Thread(target=send_post, args=(da_r.data,)))
        for t in th:
            t.start()
        for t in th:
            t.join()



def get_muti_threading_chains(chains, group):
    int_number = len(chains) // group
    chains_list = []
    for i in range(group):
        chains_list_tmp = []
        for j in range(int_number):
            chains_list_tmp.append(chains[j])
        chains = chains[int_number:]
        chains_list.append(chains_list_tmp)
    if chains != []:
        for i in range(len(chains)):
            chains_list[i].append(chains[i])
    return chains_list


def send_post_request_multi_threading(chains):
    p = Pool(config.CPU_NUMBER)
    if len(chains) <= config.CPU_NUMBER:
        for da_r in chains:
            p.apply_async(send_post, args=(da_r.data,))
    else:
        chains_tmp = get_muti_threading_chains(copy.deepcopy(chains), config.CPU_NUMBER)
        for da_r in chains_tmp:
            p.apply_async(send_post_request_threading, args=(da_r,))
    logger.info('Waiting for all post request done...')
    p.close()
    p.join()
    logger.info('All post request done.')

async def send_post_request(chains):
    if chains:  # asyncio.wait doesn't accept an empty list
        await asyncio.wait([send_post(da_r.data) for da_r in chains])

def send_post_request_multi(chains):
    p = Pool(config.CPU_NUMBER)
    for da_r in chains:
        p.apply_async(send_post, args=(da_r.data,))
    print('Waiting for all post request done...')
    p.close()
    p.join()
    print('All post request done.')