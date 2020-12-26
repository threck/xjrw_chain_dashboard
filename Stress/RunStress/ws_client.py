# -*- coding:utf-8 -*-
# @Author      : FangChao
# @File        : ws_client.py
# @Date        : 2020/12/14 0014
# @Description : xjrw_chain_dashboard

import asyncio
import threading
import websockets
import json
import time
import sys
import copy
from multiprocessing import Pool
from Common import common
from Common import mrequest
from Common import log
from Stress.Conf import config
from Stress.Common import consts
from Stress.Data import data
from Stress.Data import gen
from Stress.Data import templates
from Stress.HttpRequest import post

logger = log.Log()
B_NODE = int(sys.argv[1])
# B_NODE = 1
print(f"b node number:{B_NODE}")
print(f"b node number:{type(B_NODE)}")
uri = 'ws://%s:%s' % (config.IP, config.PORT)



#####################
# WS client
#####################
# R|S chains object
R_CHAINS = []
S_CHAINS = []
# R|S chain key
CHAIN_KEY_R = []
CHAIN_KEY_S = []
# R|S lock hash
LOCK_HASH_S = []
LOCK_HASH_R = []



def create_r_chain(r_chain_key):
    for i in range(len(r_chain_key)):
        x = r_chain_key[i]
        nodeId_r = '12D3KooWGKa86zkRz11uFp7kja4FujbQYnTt7qZQQMGfoBf00r%s' % x
        da_r = data.Data('R', x, nodeId_r)
        R_CHAINS.append(da_r)


def create_s_chain(s_chain_key):
    for i in range(len(s_chain_key)):
        x = s_chain_key[i]
        nodeId_s = '12D3KooWGKa86zkRz11uFp7kja4FujbQYnTt7qZQQMGfo00s%s' % x
        da_s = data.Data('S', x, nodeId_s)
        S_CHAINS.append(da_s)


def gen_data_shard_chain(lock_hash_r, s_chain_key):
    for data in S_CHAINS:
        for lock_ha in lock_hash_r:
            if lock_ha['chainkey'] == data.data['chainKey'][:2]:
                data.gen_data([lock_ha], s_chain_key)
                logger.info(f'Automatically generate post data:\n{data.data}')
                # every shard chain has one relay chain only. so do continue.
                continue


def gen_data_shard_chain_multi(lock_hash_r, s_chain_key):
    p = Pool(config.CPU_NUMBER)
    for data in S_CHAINS:
        for lock_ha in lock_hash_r:
            if lock_ha['chainkey'] == data.data['chainKey'][:2]:
                p.apply_async(data.gen_data, args=([lock_ha], s_chain_key))
                # logger.info(f'Automatically generate post data:\n{data.data}')
                # every shard chain has one relay chain only. so do continue.
                continue
    p.close()
    p.join()


def gen_data_relay_chain_multi(lock_hash_s, lock_hash_b):
    p = Pool(config.CPU_NUMBER)
    for data in R_CHAINS:
        lock_hash = []
        if lock_hash_s != []:
            for lock_ha in lock_hash_s:
                if lock_ha['chainkey'][:2] == data.data['chainKey']:
                    lock_hash.append(lock_ha)
            lock_hash.extend(lock_hash_b)
        else:
            lock_hash = lock_hash_b
        p.apply_async(data.gen_data, args=(lock_hash,))
        # logger.info(f'R_CHAINS now:\n{R_CHAINS}')
        # logger.info(f'lock_hash now:\n{lock_hash}')
        del lock_hash
    p.close()
    p.join()


def gen_data_relay_chain(lock_hash_s, lock_hash_b):
    for data in R_CHAINS:
        lock_hash = []
        if lock_hash_s != []:
            for lock_ha in lock_hash_s:
                if lock_ha['chainkey'][:2] == data.data['chainKey']:
                    lock_hash.append(lock_ha)
            lock_hash.extend(lock_hash_b)
        else:
            lock_hash = lock_hash_b
        data.gen_data(lock_hash)
        logger.debug(f'R_CHAINS now:\n{R_CHAINS}')
        logger.debug(f'lock_hash now:\n{lock_hash}')
        del lock_hash
        # logger.info(f'Automatically generate post data:\n{data.data}')
        # clear lock_hash


async def gen_data(chains, lock_hash):
    if chains:  # asyncio.wait doesn't accept an empty list
        await asyncio.wait([da.gen_data(lock_hash) for da in chains])


async def gen_lock_hash(chains):
    if chains:  # asyncio.wait doesn't accept an empty list
        await asyncio.wait([da.gen_lock_hash() for da in chains])


async def send_msg(ws, msg):
    # print(f'send msg: {msg}')
    msg = json.dumps(msg).encode('utf-8')
    await ws.send(msg)
    logger.info(f"client send msg:{msg}")
    return True


async def recv_msg(ws):
    msg = await ws.recv()
    msg = json.loads(msg)
    logger.info(f'client recv msg: {msg}')
    return msg

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
    logger.info(f'chain threading group: {chains}')
    th = []
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


def send_post_request_multi_threading_tmp(chains, type):
    p = Pool(config.CPU_NUMBER)
    logger.info(f'prepare {type} chain muti process')
    if len(chains) <= config.CPU_NUMBER:
        logger.info(f'-- {type} chain process group: {chains}')
        for da_r in chains:
            p.apply_async(send_post, args=(da_r.data,))
    else:
        chains_tmp = get_muti_threading_chains(chains, config.CPU_NUMBER)
        logger.info(f'{type} chain process pool: {chains_tmp}')
        for da_r in chains_tmp:
            logger.info(f'create {type} chain process group: {da_r}')
            p.apply_async(send_post_request_threading, args=(da_r,))
            logger.info(f'create {type} chain process group over: {da_r}')
    logger.info(f'Waiting for all {type} post request done... nu: {len(chains)}')
    p.close()
    p.join()
    logger.info(f'All {type} post request done.')

def send_post_request_multi_threading(chains, type):
    p = Pool(config.CPU_NUMBER)
    logger.info(f'prepare {type} chain muti process')
    logger.info(f'-- {type} chain process group: {chains}')
    for da_r in chains:
        p.apply_async(send_post, args=(da_r.data,))
    logger.info(f'Waiting for all {type} post request done... nu: {len(chains)}')
    p.close()
    p.join()
    logger.info(f'All {type} post request done.')


# 客户端主逻辑
async def main_logic():
    global LOCK_HASH_R
    global LOCK_HASH_S
    global B_NODE

    async with websockets.connect(uri) as ws:
        # 发送本地 R|S 数量
        msg_tmp = dict(signal='chain_info', chain_nu_local=config.CHAIN_NU_LOCAL)
        await send_msg(ws, msg_tmp)

        # 接收 ws 返回的 chainkey
        while True:
            msg = await recv_msg(ws)
            if msg['signal'] == 'chain_info':
                CHAIN_KEY_R = msg['chain_key_r']
                CHAIN_KEY_S = msg['chain_key_s']
                break
        logger.info(f'get chain_info from ws, content is:\n{msg} ...')
        # 生成 R|S 初始链数据
        logger.info('create r_chain and s_chain according r_chain_key now ...')
        create_r_chain(CHAIN_KEY_R)
        create_s_chain(CHAIN_KEY_S)

        # 如果配置了B，则生成B post数据; 发送post; 生成b_lock_hash; 发送 b_over, lock_hash_b
        # if config.CHAIN_NU_LOCAL['B'] == 1:
        if B_NODE == 1:
            logger.info('prepare BEACON chain post request data ...')
            da_b = data.Data('B', '', '12D3KooWGKa86zkRz11uFp7kja4FujbQYnTt7qZQQMGfoBfBqb01')
            da_b.gen_data(LOCK_HASH_R)
            post.send_post(da_b.data)
            await da_b.gen_lock_hash()
            msg_tmp = dict(signal=config.B_OVER_MARK, lockHash=[da_b.lock_hash])
            await send_msg(ws, msg_tmp)
        else:
            msg_tmp = dict(signal=config.B_OVER_MARK, lockHash=[])
            await send_msg(ws, msg_tmp)

        # 开始接收 ws 广播的msg
        while True:
            print('into while loop...')
            msg = await recv_msg(ws)
            # print(common.current_time_iso())
            if msg['signal'] == config.B_START_MARK:
                # if config.CHAIN_NU_LOCAL['B'] == 1:
                if B_NODE == 1:
                    logger.info('prepare BEACON chain post request data ...')
                    da_b.gen_data(msg['lockHash'])
                    post.send_post(da_b.data)
                    await da_b.gen_lock_hash()
                    msg_tmp = dict(signal=config.B_OVER_MARK, lockHash=[da_b.lock_hash])
                    await send_msg(ws, msg_tmp)

            if msg['signal'] == config.R_START_MARK:
                # prepare RELAY chain post request data
                logger.info('prepare RELAY chain post request data ...')
                lock_hash_b = msg['lockHash']
                logger.info(f"gen relay chain start:{time.strftime('%X')}")
                start_time = time.time()
                gen_data_relay_chain(LOCK_HASH_S, lock_hash_b)
                end_time = time.time()
                logger.info(f"====> R gen spend time:{end_time - start_time}")
                logger.info(f"gen relay chain end:{time.strftime('%X')}")
                # # await gen_data(R_CHAINS, lock_hash)

                # send post request
                logger.info('send r post request ...')
                logger.debug(f"R_CHAINS: {R_CHAINS}")
                start_time = time.time()
                send_post_request_multi_threading(R_CHAINS, 'R')
                end_time = time.time()
                logger.info(f"====> R post spend time:{end_time - start_time}")
                LOCK_HASH_S.clear()
                lock_hash_b.clear()

                # gen all lock hash of relay chain
                logger.info('gen all lock hash of relay chain ...')
                await gen_lock_hash(R_CHAINS)

                # send ws request with [msg_tmp]
                logger.info('send message for telling R over ...')
                LOCK_HASH_R = [da.lock_hash for da in R_CHAINS]
                msg_tmp = dict(signal=config.R_OVER_MARK, r_number=config.CHAIN_NU_LOCAL['R'], lockHash=LOCK_HASH_R)
                logger.info(f'message content:\n{msg_tmp}')
                await send_msg(ws, msg_tmp)

            if msg['signal'] == config.S_START_MARK:
                # prepare SHARD chain post request data
                logger.info('prepare SHARD chain post request data ...')
                # logger.info(f'lock_hash_r content:\n{LOCK_HASH_R}')
                logger.info(f"gen shard chain start:{time.strftime('%X')}")
                start_time = time.time()
                gen_data_shard_chain(LOCK_HASH_R, CHAIN_KEY_S)  # chain_key
                end_time = time.time()
                logger.info(f"=====> S gen spend time:{end_time - start_time}")
                logger.info(f"gen shard chain end:{time.strftime('%X')}")

                # send post request
                logger.info('send s post request ...')
                start_time = time.time()
                send_post_request_multi_threading(S_CHAINS, 'S')
                end_time = time.time()
                logger.info(f"=====> S post spend time:{end_time - start_time}")
                s_number = len(S_CHAINS)
                logger.info(f'all s post nu:{s_number}')
                LOCK_HASH_R.clear()

                # gen all lock hash of shard chain
                logger.info('gen all lock hash of shard chain ...')
                await gen_lock_hash(S_CHAINS)

                # send ws request with [msg_tmp]
                logger.info('send message for telling S over ...')
                LOCK_HASH_S = [da.lock_hash for da in S_CHAINS]
                msg_tmp = dict(signal=config.S_OVER_MARK, s_number=config.CHAIN_NU_LOCAL['S'])
                logger.info(f'message content:\n{msg_tmp}')
                await send_msg(ws, msg_tmp)


asyncio.get_event_loop().run_until_complete(main_logic())
