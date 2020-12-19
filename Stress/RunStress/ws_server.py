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
from Stress.Data import templates
from Stress.Data import data
from Stress.Conf import config
from Common import common
from Common import mrequest
from Common import log
from datetime import datetime

logger = log.Log()
USERS = list()
s_ready_number = 0
r_ready_number = 0
r_number = config.CHAIN_NU_TOTAL['R']
s_number = config.CHAIN_NU_TOTAL['S']
da_b = data.Data('B', '', '12D3KooWGKa86zkRz11uFp7kja4FujbQYnTt7qZQQMGfoBfBqb01')
R_CHAIN_KEYS = []
S_CHAIN_KEYS = []
lock_hash_r = []

time_start = ''
time_end = ''
time_mark = ''

async def notify_users():
    if USERS:  # asyncio.wait doesn't accept an empty list
        msg = json.dumps({"signal": "notify", "type": "users", "count": len(USERS)})
        print(f'notify users info realtime: {msg}')
        await asyncio.wait([user.send(msg) for user in USERS])


async def notify_msg(msg):
    if USERS:  # asyncio.wait doesn't accept an empty list
        print(f'notify msg : {msg} to {USERS}')
        msg = json.dumps(msg).encode('utf-8')
        await asyncio.wait([user.send(msg) for user in USERS])


async def register(ws):
    USERS.append(ws)
    print(f'new ws conn registration: {ws}')
    await notify_users()


async def unregister(ws):
    USERS.remove(ws)
    print(f'remove ws conn registration: {ws}')
    await notify_users()


def send_post(req_data):
    print('running %s_post ...' % req_data['type'])
    api_url = config.POST_URL
    header = templates.header
    request = mrequest.Request()
    print(f'post request data: {req_data}')
    resp = request.post_request(api_url, req_data, header)
    print(f'post response data: {resp}')
    print('running %s_post over ...' % req_data['type'])


async def recv_msg(ws):
    msg = await ws.recv()
    msg = json.loads(msg)
    return msg


async def send_msg(ws, msg):
    print(f'send msg: {msg}')
    await ws.send(msg)
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
            print(f'recv msg: {msg}')
            # await asyncio.sleep(1)
            if msg['signal'] == 'chain_info':
                logger.info(f'recv chain_info from client, content is:\n{msg} ...')
                R_CHAIN_KEYS.extend(msg['r_chain_key'])
                S_CHAIN_KEYS.extend(msg['s_chain_key'])
                msg_tmp = dict(signal='chain_info', r_chain_key=R_CHAIN_KEYS)
                logger.info(f'save chain_info, content now is:\n{msg_tmp} ...')
                await notify_msg(msg_tmp)
            if msg['signal'] == 'b_start' or msg['signal'] == config.S_READY_MARK:
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
                    logger.info(f'lock_hash_r content:\n{lock_hash_r}')
                    da_b.gen_data(lock_hash_r)
                    logger.info(f'Automatically generate post data:{da_b.data}')

                    # send post request
                    logger.info(f'send b post request ...')
                    print(f'detect S chain {s_ready_number} post over')
                    await wait_for_a_interval_time()
                    send_post(da_b.data)
                    lock_hash_r.clear()

                    # send notify for running R post request (contains B_chain's and S_chain's lock_hash)
                    await da_b.gen_lock_hash()
                    msg_tmp = dict(signal='r_start', lockHash=da_b.lock_hash)
                    logger.info('send notify for running R post request ...')
                    logger.info(f'notify content:\n{msg_tmp}')
                    await notify_msg(msg_tmp)
                    r_ready_number, s_ready_number = 0, 0
            elif msg['signal'] == config.R_READY_MARK:
                r_ready_number += msg['r_number']
                # collect lock_hash for next post data of B chain
                logger.info(f"r ready, recv lockHash_r: {msg['lockHash']}")
                lock_hash_r.extend(msg['lockHash'])
                logger.info(f"create new lockHash_r: {lock_hash_r}")

                if r_ready_number == r_number:
                    logger.info(f'detect -> r_ready_number[{r_ready_number}] = r_number[{r_number}]')
                    # send notify for running S post request
                    logger.info('send notify for running S post request ...')
                    msg_tmp = dict(signal='s_start', s_chain_key=S_CHAIN_KEYS)
                    logger.info(f'notify content:\n{msg_tmp}')
                    await notify_msg(msg_tmp)
                    r_ready_number, s_ready_number = 0, 0
    finally:
        await unregister(ws)


def main():
    # clear mongo database
    mg = data.MongoDataBase()
    mg.clear_mongo_database()

    # start websocket server
    start_server = websockets.serve(main_logic, config.IP, config.PORT)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    main()