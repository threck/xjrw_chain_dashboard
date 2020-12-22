# -*- coding:utf-8 -*-
# @Author      : FangChao
# @File        : ws_server.py
# @Date        : 2020/12/14 0014
# @Description : xjrw_chain_dashboard

import asyncio
import websockets
import socket
import time
import sys
import random
import json

from datetime import datetime

from Common import common
from Common import mrequest
from Common import log

from Stress.Data import templates
from Stress.Data import data
from Stress.Data import gen
from Stress.Conf import config
from Stress.Common import consts
from Stress.HttpRequest import post



logger = log.Log()
USERS = list()
da_b = data.Data('B', '', '12D3KooWGKa86zkRz11uFp7kja4FujbQYnTt7qZQQMGfoBfBqb01')

time_start = ''
time_end = ''
time_mark = ''


async def notify_users():
    if USERS:  # asyncio.wait doesn't accept an empty list
        msg = json.dumps({"signal": "notify", "type": "users", "count": len(USERS)})
        # print(f'notify users info realtime: {msg}')
        await asyncio.wait([user.send(msg) for user in USERS])
        logger.info(f'server notify msg: {msg}')


async def notify_msg(msg):
    if USERS:  # asyncio.wait doesn't accept an empty list
        # print(f'notify msg : {msg} to {USERS}')
        msg = json.dumps(msg).encode('utf-8')
        await asyncio.wait([user.send(msg) for user in USERS])
        logger.info(f'server notify msg: {msg}')


async def register(ws):
    USERS.append(ws)
    # print(f'new ws conn registration: {ws}')
    await notify_users()


async def unregister(ws):
    USERS.remove(ws)
    # print(f'remove ws conn registration: {ws}')
    await notify_users()


async def recv_msg(ws):
    msg = await ws.recv()
    msg = json.loads(msg)
    logger.info(f'server recv msg: {msg}')
    return msg


async def send_msg(ws, msg):
    # print(f'send msg: {msg}')
    msg = json.dumps(msg).encode('utf-8')
    await ws.send(msg)
    logger.info(f"server send msg:{msg}")
    return True

def count_interval_time():
    global time_start
    if time_start == '':
        time_start = datetime.now()
        time_start_tmp = time_start.strftime('%Y-%m-%d %H:%M:%S')
        logger.info(f'=====> start time: [ {time_start_tmp} ]')
        interval_time = config.STRESS_LOOP_INTERVAL
    else:
        time_end = datetime.now()
        time_end_tmp = time_end.strftime('%Y-%m-%d %H:%M:%S')
        interval = time_end - time_start
        interval_time = interval.seconds + interval.microseconds*0.000001
        time_start = time_end
        logger.info(f'=====> end time: [ {time_end_tmp} ]')
        logger.info(f'=====> interval time: [ {interval_time} ]')
    return interval_time

async def wait_for_a_interval_time():
    global time_start
    interval_time = count_interval_time()
    wait_time = config.STRESS_LOOP_INTERVAL - interval_time
    if wait_time >= 0:
        logger.info(f'wait {wait_time}s to start next post wave ...')
        await asyncio.sleep(wait_time)
    time_start = datetime.now()  # set beacon start time

# 服务器端主逻辑
async def main_logic(ws, path):
    await register(ws)
    global r_ready_number
    global s_ready_number
    global time_start
    try:
        while True:
            msg = await recv_msg(ws)
            if msg['signal'] == 'chain_info':
                R_CHAIN_KEYS.extend(msg['r_chain_key'])
                msg_tmp = dict(signal='chain_info', r_chain_key=R_CHAIN_KEYS)
                await notify_msg(msg_tmp)
            if msg['signal'] == 'b_start' or msg['signal'] == config.S_OVER_MARK:
                s_ready_number += msg['s_number']
                if s_ready_number == s_number:
                    # loop time control logic.
                    config.STRESS_LOOP_TIME -= 1
                    if config.STRESS_LOOP_TIME == 0:
                        logger.info(f'=====> STRESS LOOP : over')
                        break
                    elif config.STRESS_LOOP_TIME == -1:
                        logger.info(f'=====> STRESS LOOP :[run forever]')
                    else:
                        logger.info(f'=====> STRESS LOOP LEFT:[{config.STRESS_LOOP_TIME} times]')
                    logger.info(f'detect -> s_ready_number[{s_ready_number}] = s_number[{s_number}]')
                    # prepare BEACON chain post request data
                    logger.info('prepare BEACON chain post request data ...')
                    da_b.gen_data(lock_hash_r)
                    logger.info(f'Automatically generate post data:{da_b.data}')

                    # send post request
                    logger.info(f'send b post request ...')
                    print(f'detect S chain {s_ready_number} post over')
                    if config.STRESS_LOOP_INTERVAL != 0:
                        await wait_for_a_interval_time()
                    #post.send_post(da_b.data)
                    lock_hash_r.clear()

                    # send notify for running R post request (contains B_chain's and S_chain's lock_hash)
                    await da_b.gen_lock_hash()
                    msg_tmp = dict(signal='r_start', lockHash=da_b.lock_hash)
                    await notify_msg(msg_tmp)
                    r_ready_number, s_ready_number = 0, 0
            elif msg['signal'] == config.B_OVER_MARK:
                msg_tmp = dict(signal='r_start', lockHash='')
                msg_tmp = json.dumps(msg_tmp).encode('utf-8')
                await notify_msg(msg_tmp)
            elif msg['signal'] == config.R_OVER_MARK:
                r_ready_number += msg['r_number']
                # collect lock_hash for next post data of B chain
                logger.info(f"r ready, recv lockHash_r: {msg['lockHash']}")
                lock_hash_r.extend(msg['lockHash'])
                logger.info(f"create new lockHash_r: {lock_hash_r}")

                if r_ready_number == r_number:
                    logger.info(f'detect -> r_ready_number[{r_ready_number}] = r_number[{r_number}]')
                    # send notify for running S post request
                    msg_tmp = dict(signal='s_start')
                    await notify_msg(msg_tmp)
                    r_ready_number, s_ready_number = 0, 0
    except Exception as e:
        logger.error(e)
    finally:
        await unregister(ws)



async def main_logic_tmp(ws, path):
    await register(ws)
    try:
        while True:
            msg = await recv_msg(ws)
            # 收到生成 R chain key 的指令, 生成 R|S chain key; 并返回 R|S chain key
            if msg['signal'] == 'chain_info':
                chain_nu_local = msg['chain_nu_local']
                gen_r_chain_key, gen_s_chain_key = gen.create_r_and_s_chain_key(chain_nu_local)
                msg_send = dict(signal='chain_info', chain_key_r=gen_r_chain_key, chain_key_s=gen_s_chain_key)
                await send_msg(ws, msg_send)
            # 收到 b 结束信号
            elif msg['signal'] == config.B_OVER_MARK:
                consts.LOCK_HASH_B_WS.extend(msg['lockHash'])
                if len(consts.CHAIN_KEYS_R) == config.CHAIN_NU_TOTAL['R']:
                    msg_notify = dict(signal=config.R_START_MARK, lockHash=consts.LOCK_HASH_B_WS)
                    await notify_msg(msg_notify)
                    consts.LOCK_HASH_B_WS.clear()
            # 收到 r 结束信号
            elif msg['signal'] == config.R_OVER_MARK:
                consts.R_OVER_NU += msg['r_number']
                consts.LOCK_HASH_R_WS.extend(msg['lockHash'])
                if consts.R_OVER_NU == config.CHAIN_NU_TOTAL['R']:
                    logger.info(f"detect -> r_ready_number[{consts.R_OVER_NU}] = r_number[{config.CHAIN_NU_TOTAL['R']}]")
                    # send notify for running S post request
                    msg_tmp = dict(signal=config.S_START_MARK)
                    await notify_msg(msg_tmp)
                    consts.R_OVER_NU = 0
            # 收到 s 结束信号
            elif msg['signal'] == config.S_OVER_MARK:
                consts.S_OVER_NU += msg['s_number']
                if consts.S_OVER_NU == config.CHAIN_NU_TOTAL['S']:
                    msg_notify = dict(signal=config.B_START_MARK, lockHash=consts.LOCK_HASH_R_WS)
                    await notify_msg(msg_notify)
                    consts.LOCK_HASH_R_WS.clear()
                    consts.S_OVER_NU = 0

    except Exception as e:
        logger.error(e)
    finally:
        await unregister(ws)


def main():
    # clear mongo database
    # mg = data.MongoDataBase()
    # mg.clear_mongo_database()

    # start websocket server
    start_server = websockets.serve(main_logic_tmp, config.IP, config.PORT)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    main()