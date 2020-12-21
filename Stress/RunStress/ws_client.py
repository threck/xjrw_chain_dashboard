# -*- coding:utf-8 -*-
# @Author      : FangChao
# @File        : ws_client.py
# @Date        : 2020/12/14 0014
# @Description : xjrw_chain_dashboard

import asyncio
import websockets
import json
import time
from Stress.Conf import config
from Common import common
from Common import mrequest
from Common import log
from Stress.Data import data
from Stress.Data import templates


logger = log.Log()

uri = 'ws://%s:%s' % (config.IP, config.PORT)
R_CHAIN_KEY = []
S_CHAIN_KEY = []
R_CHAINS = []
S_CHAINS = []
LOCK_HASH_S = []
LOCK_HASH_R = []


def create_relay_and_shard_chain(r_chain_key):
    chainNu_r_local = config.CHAIN_NU_LOCAL['R']
    chainNu_s_node = int(config.CHAIN_NU_LOCAL['S'] / chainNu_r_local)
    s = len(r_chain_key)
    for x in range(s, s+chainNu_r_local):
        # create relay chain
        chainKey_r = hex(x).split('x')[1].upper().rjust(2, '0')
        nodeId_r = '12D3KooWGKa86zkRz11uFp7kja4FujbQYnTt7qZQQMGfoBf00r%s' % chainKey_r
        da_r = data.Data('R', chainKey_r, nodeId_r)
        R_CHAINS.append(da_r)
        R_CHAIN_KEY.append(da_r.data['chainKey'])
        # create shard chain
        create_shard_chain(chainKey_r, chainNu_s_node)


def create_shard_chain(chainKey_r, chainNu_s_node):
    for x in range(chainNu_s_node):
        chainKey_s = '%s%s' % (chainKey_r, hex(x).split('x')[1].upper().rjust(2, '0'))
        nodeId_s = '12D3KooWGKa86zkRz11uFp7kja4FujbQYnTt7qZQQMGfo00s%s' % chainKey_s
        da_s = data.Data('S', chainKey_s, nodeId_s)
        S_CHAINS.append(da_s)
        S_CHAIN_KEY.append(da_s.data['chainKey'])


def gen_data_shard_chain(lock_hash_r, s_chain_key):
    for data in S_CHAINS:
        for lock_ha in lock_hash_r:
            if lock_ha['chainkey'] == data.data['chainKey'][:2]:
                data.gen_data([lock_ha], s_chain_key)
                # logger.info(f'Automatically generate post data:\n{data.data}')
                # every shard chain has one relay chain only. so do continue.
                continue


def gen_data_relay_chain(lock_hash_s, lock_hash_b):
    for data in R_CHAINS:
        lock_hash = []
        if lock_hash_s != []:
            for lock_ha in lock_hash_s:
                if lock_ha['chainkey'][:2] == data.data['chainKey']:
                    lock_hash.append(lock_ha)
            lock_hash.append(lock_hash_b)
        else:
            lock_hash = [lock_hash_b]
        data.gen_data(lock_hash)
        logger.info(f'R_CHAINS now:\n{R_CHAINS}')
        logger.info(f'lock_hash now:\n{lock_hash}')
        del lock_hash
        # logger.info(f'Automatically generate post data:\n{data.data}')
           # clear lock_hash


async def send_msg(ws, msg):
    # print(f'send msg: {msg}')
    msg = json.dumps(msg).encode('utf-8')
    await ws.send(msg)
    return True


async def recv_msg(ws):
    msg = await ws.recv()
    msg = json.loads(msg)
    # print(f'client 2 recv : {msg}')
    return msg


async def gen_data(chains, lock_hash):
    if chains:  # asyncio.wait doesn't accept an empty list
        await asyncio.wait([da.gen_data(lock_hash) for da in chains])

async def send_post(req_data):
    logger.info('running %s_post ...' % req_data['type'])
    api_url = config.POST_URL
    header = templates.header
    request = mrequest.Request()
    # logger.info(f'post request data: {req_data}')
    resp = request.post_request(api_url, req_data, header)
    logger.info(f'post response data: {resp}')
    logger.info(f"post response time: {resp['time_consuming']}")
    logger.info('running %s_post over ...' % req_data['type'])

async def send_post_request(chains):
    if chains:  # asyncio.wait doesn't accept an empty list
        await asyncio.wait([send_post(da_r.data) for da_r in chains])


async def send_message(chains):
    if chains:  # asyncio.wait doesn't accept an empty list
        await asyncio.wait([send_post(da.data) for da in chains])


async def gen_lock_hash(chains):
    if chains:  # asyncio.wait doesn't accept an empty list
        await asyncio.wait([da.gen_lock_hash() for da in chains])


# 客户端主逻辑
async def main_logic():
    async with websockets.connect(uri) as ws:
        # get r_chain_key info
        msg_tmp = dict(signal='chain_info', r_chain_key=R_CHAIN_KEY, s_chain_key=S_CHAIN_KEY)
        await send_msg(ws, msg_tmp)
        while True:
            msg = await recv_msg(ws)
            if msg['signal'] == 'chain_info':
                r_chain_key = msg['r_chain_key']
                break
        logger.info(f'get chain_info from ws, content is:\n{msg} ...')

        # create r_chain and s_chain according r_chain_key now
        logger.info('create r_chain and s_chain according r_chain_key now ...')
        create_relay_and_shard_chain(r_chain_key)

        # send r_chain_key to ws server
        msg_tmp = dict(signal='chain_info', r_chain_key=R_CHAIN_KEY, s_chain_key=S_CHAIN_KEY)
        logger.info(f'send chain_info to ws, content is:\n{msg_tmp} ...')
        await send_msg(ws, msg_tmp)
        await recv_msg(ws)

        # send b_start signal ...
        logger.info('send b_start signal ...')
        msg_tmp = dict(signal='b_start', s_number=config.CHAIN_NU_LOCAL['S'])
        await send_msg(ws, msg_tmp)
        while True:
            print('into while loop...')
            msg = await recv_msg(ws)
            # print(common.current_time_iso())
            if msg['signal'] == 'notify':
                pass
            if msg['signal'] == 'r_start':
                # prepare RELAY chain post request data
                logger.info('prepare RELAY chain post request data ...')
                lock_hash_b = msg['lockHash']
                if 'LOCK_HASH_S' not in locals():
                    LOCK_HASH_S = []
                logger.info(f'lock_hash_b content:\n{lock_hash_b}')
                logger.info(f'lock_hash_s content:\n{LOCK_HASH_S}')
                logger.info(f"gen relay chain start:{time.strftime('%X')}")
                gen_data_relay_chain(LOCK_HASH_S, lock_hash_b)
                logger.info(f"gen relay chain end:{time.strftime('%X')}")
                # # await gen_data(R_CHAINS, lock_hash)

                # send post request
                logger.info('send r post request ...')
                await send_post_request(R_CHAINS)
                LOCK_HASH_S.clear()
                lock_hash_b.clear()

                # gen all lock hash of relay chain
                logger.info('gen all lock hash of relay chain ...')
                await gen_lock_hash(R_CHAINS)

                # send ws request with [msg_tmp]
                logger.info('send message for telling R over ...')
                LOCK_HASH_R = [da.lock_hash for da in R_CHAINS]
                msg_tmp = dict(signal=config.R_READY_MARK, r_number=config.CHAIN_NU_LOCAL['R'], lockHash=LOCK_HASH_R)
                logger.info(f'message content:\n{msg_tmp}')
                await send_msg(ws, msg_tmp)

            if msg['signal'] == 's_start':
                # prepare SHARD chain post request data
                logger.info('prepare SHARD chain post request data ...')
                logger.info(f'lock_hash_r content:\n{LOCK_HASH_R}')
                logger.info(f"gen shard chain start:{time.strftime('%X')}")
                gen_data_shard_chain(LOCK_HASH_R, msg['s_chain_key'])
                logger.info(f"gen shard chain end:{time.strftime('%X')}")

                # send post request
                logger.info('send s post request ...')
                await send_post_request(S_CHAINS)
                LOCK_HASH_R.clear()

                # gen all lock hash of shard chain
                logger.info('gen all lock hash of shard chain ...')
                await gen_lock_hash(S_CHAINS)

                # send ws request with [msg_tmp]
                logger.info('send message for telling S over ...')
                LOCK_HASH_S = [da.lock_hash for da in S_CHAINS]
                msg_tmp = dict(signal=config.S_READY_MARK, s_number=config.CHAIN_NU_LOCAL['S'])
                logger.info(f'message content:\n{msg_tmp}')
                await send_msg(ws, msg_tmp)


asyncio.get_event_loop().run_until_complete(main_logic())
