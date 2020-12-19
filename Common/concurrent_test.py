# -*- coding:utf-8 -*-
# @Author      : FangChao
# @File        : concurrent_test
# @Date        : 2020/12/10 0010
# @Description : xjrw_chain_dashboard

import asyncio
import time
import websocket
import json


# async def test():
#     print(f"test1")
#     # time.sleep(2)
#     r = await asyncio.sleep(2)
#     print(f"test1 again")
#
# async def test2():
#     print(f"test2")
#     # time.sleep(2)
#     r = await asyncio.sleep(5)
#     print(f"test2 again")
#
# loop = asyncio.get_event_loop()
# tasks = [test(), test2()]
# print('over1')
# loop.run_until_complete(asyncio.wait(tasks))
# print('over2')
# loop.close()
# print('over3')


async def test_websocket():
    uri = "ws://192.168.0.164:8888/api/v1.0/wsConn"
    async with websockets.connect(uri) as websocket:
        # await ws.send("asd")
        print('start to recv ...')
        await websocket.recv()
    print('end to recv ...')


async def create_subscription():
    uri = "ws://192.168.0.164:8888/api/v1.0/wsConn"
    data = {"event": "block", "body": {}}
    print('wait before start to send data ...')
    time.sleep(10)
    async with websockets.connect(uri) as websocket:
        print('start to send data ...')
        await websocket.send(json.dumps(data))
    print('end to send data ...')

# ========================== 协程 ======================
# async def start_master(ws):
#     print('start master')
#     await ws_recv(ws)
#     print('end master')
# 
# async def wait_send(ws):
#     print('start wait_send')
#     await ws_send()
#     print('end wait_send')
# 
# async def ws_recv(ws):
#     print('start ws_recv ...')
#     # uri = "ws://192.168.0.164:8888/api/v1.0/wsConn"
#     # ws = websocket.create_connection(uri)
#     r = ws.recv()
#     # time.sleep(3)
#     print(f'==get ws response: {r}')
#     print('end ws_recv ...')
# 
# async def ws_send(ws):
#     # uri = "ws://192.168.0.164:8888/api/v1.0/wsConn"
#     # ws = websocket.create_connection(uri)
#     data = {"event": "block", "body": {}}
#     print('start ws_send ...')
#     ws.send(json.dumps(data))
# 
# 
# 
# uri = "ws://192.168.0.164:8888/api/v1.0/wsConn"
# ws = websocket.create_connection(uri)
# 
# loop = asyncio.get_event_loop()
# tasks = [asyncio.ensure_future(start_master(ws)), asyncio.ensure_future(wait_send(ws))]
# loop.run_until_complete(asyncio.wait(tasks))
# # loop.run_until_complete(start_master(ws))

#  ========================== 协程 ======================


# ========================== 线程 ======================
import threading
count = 0
spendtime = 0
ws_recv_data = ""

def ws_recv(ws):
    global spendtime
    global ws_recv_data
    print('start ws_recv ...')
    ws_data = ws.recv()
    spendtime = count
    ws_recv_data = ws_data
    print('end ws_recv ...')


def ws_send(ws):
    data = {"event": "block", "body": {}}
    print('start ws_send ...')
    time.sleep(10)
    ws.send(json.dumps(data))
    print('end ws_send ...')
    return 'ok'


def ws_count():
    for i in range(12):
        global count
        count += 1
        time.sleep(1)
        # print(count)

uri = "ws://192.168.0.164:8888/api/v1.0/wsConn"
ws = websocket.create_connection(uri)
count = 0
t1 = threading.Thread(target=ws_recv, name='ws_recv', args=(ws,))
t2 = threading.Thread(target=ws_send, name='ws_send', args=(ws,))
t3 = threading.Thread(target=ws_count, name='ws_count')
t1.start()
t2.start()
t3.start()
t1.join()
t2.join()
t3.join()
print(f'===total spendtime: {spendtime}')
print(f'===get ws response: {ws_recv_data}')

# ========================== 线程 ======================
