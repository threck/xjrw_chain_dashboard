# -*- coding:utf-8 -*-
# @Author      : FangChao
# @File        : ws_server.py
# @Date        : 2020/12/14 0014
# @Description : xjrw_chain_dashboard

import asyncio
import websockets
import time
import json

from datetime import datetime
from Common import log
from Stress.Data import gen
from Stress.Data import data
from Stress.Conf import config
from Stress.Common import consts



logger = log.Log()
USERS = list()
# da_b = data.Data('B', '', '12D3KooWGKa86zkRz11uFp7kja4FujbQYnTt7qZQQMGfoBfBqb01')

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
        logger.info(f'=====> all interval time: [ {interval_time} ]')
    return interval_time

async def wait_for_a_interval_time(interval_time):
    global time_start
    wait_time = config.STRESS_LOOP_INTERVAL - interval_time
    if wait_time >= 0:
        logger.info(f'wait {wait_time}s to start next post wave ...')
        await asyncio.sleep(wait_time)
    time_start = datetime.now()  # set beacon start time

# 服务器端主逻辑
async def main_logic(ws, path):
    await register(ws)
    global s_start_time
    global s_end_time
    try:
        while True:
            msg = await recv_msg(ws)
            # await asyncio.sleep(1)
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
                    s_start_time = time.time()
                    await notify_msg(msg_tmp)
                    consts.R_OVER_NU = 0

            # 收到 s 结束信号
            elif msg['signal'] == config.S_OVER_MARK:
                consts.S_OVER_NU += msg['s_number']
                if consts.S_OVER_NU == config.CHAIN_NU_TOTAL['S']:
                    s_end_time = time.time()
                    logger.info(f"all s post nu:{config.CHAIN_NU_TOTAL['S']}")
                    logger.info(f"all s post spend time:{s_end_time - s_start_time}")
                    msg_notify = dict(signal=config.B_START_MARK, lockHash=consts.LOCK_HASH_R_WS)
                    await notify_msg(msg_notify)
                    consts.LOCK_HASH_R_WS.clear()
                    consts.S_OVER_NU = 0

                    # 配置 B->R->S 运行轮次数
                    config.STRESS_LOOP_TIME -= 1
                    if config.STRESS_LOOP_TIME == 0:
                        logger.info(f'=====> STRESS LOOP : over')
                        break
                    elif config.STRESS_LOOP_TIME == -1:
                        logger.info(f'=====> STRESS LOOP :[run forever]')
                    else:
                        logger.info(f'=====> STRESS LOOP LEFT:[{config.STRESS_LOOP_TIME} times]')
                    # 计算每轮发送耗时
                    interval = count_interval_time()
                    if config.STRESS_LOOP_INTERVAL != 0:
                        await wait_for_a_interval_time(interval)

    except Exception as e:
        logger.error(e)
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