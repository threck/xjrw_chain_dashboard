# -*- coding:utf-8 -*-
# @Author      : FangChao
# @File        : test_api
# @Date        : 2020/12/2 0002
# @Description : xjrw_chain_dashboard

import pytest
import allure
import random
import time
import json
import sys
import threading
import copy
from Config import config
from Common import mrequest
from Common import consts
from Common import massert
from Common import log
from Common import mwebsocket
from Common import mongo
from Common import common
from Param.req_resp_data import ws_generate_cmd
from Param.req_resp_data import http_heart_beat
from Param.req_resp_data import http_block_reported
from Param.req_resp_data import ws_get_block_info_realtime

conf = config.Config()
request = mrequest.Request()
test = massert.Assertions()

@pytest.mark.websocket
class TestWSAPITest:

    count = 0
    spendtime = 0
    ws_recv_data = ""
    ws_recv_data1 = ""
    ws_recv_data2 = ""

    def ws_recv(self, ws, wait_time=0):
        logger = log.Log()
        logger.info('ws_recv stand by...')
        TestWSAPITest.spendtime = 0
        TestWSAPITest.ws_recv_data = ""
        if wait_time == 0:
            ws_data = ws.receive()
        else:
            time.sleep(wait_time)
            ws_data = ws.receive()
        TestWSAPITest.spendtime = TestWSAPITest.count
        TestWSAPITest.ws_recv_data = ws_data
        logger.info(f'ws_recv got a response. spend time is :{TestWSAPITest.spendtime}, recv_data is :{TestWSAPITest.ws_recv_data}')

    def ws_recv_multi(self, ws, wait_time=0):
        logger = log.Log()
        logger.info('ws_recv stand by...')
        TestWSAPITest.spendtime = 0
        TestWSAPITest.ws_recv_data = ""
        TestWSAPITest.ws_recv_data1 = ""
        TestWSAPITest.ws_recv_data2 = ""
        if wait_time == 0:
            ws_data0 = ws.receive()
            ws_data1 = ws.receive()
            ws_data2 = ws.receive()
        else:
            time.sleep(wait_time)
            ws_data0 = ws.receive()
            ws_data1 = ws.receive()
            ws_data2 = ws.receive()
        TestWSAPITest.spendtime = TestWSAPITest.count
        TestWSAPITest.ws_recv_data = ws_data0
        TestWSAPITest.ws_recv_data1 = ws_data1
        TestWSAPITest.ws_recv_data2 = ws_data2
        logger.info(f'ws_recv got a response. spend time is :{TestWSAPITest.spendtime}, recv_data is :{TestWSAPITest.ws_recv_data}')

    def ws_send_for_subscription(self, ws, data, t):
        logger = log.Log()
        logger.info(f'ws_send stand by. and ws_send request will send in {t}s...')
        time.sleep(t)
        ws.send(data)
        logger.info(f'ws_send over! send data: {data}...')
        return 'ok'

    def ws_count(self, t):
        logger = log.Log()
        TestWSAPITest.count = 0
        for i in range(t+2):
            TestWSAPITest.count += 1
            time.sleep(1)
            logger.info(f'{i}s ...')

    def http_post_request(self, api_url, data_req, header, wait_time):
        logger = log.Log()
        logger.info(f'post request stand by. and post request will send in {wait_time}s...')
        time.sleep(wait_time)
        resp = request.post_request(api_url, data_req, header)
        logger.info(f'post request send over! send data: {data_req}...')
        logger.info(f'post request send over! resp data: {resp}...')

    @allure.feature('websocket接口')
    @allure.story('命令生成')
    @pytest.mark.gen_cmd
    def test_generate_cmd_single_request_shard_chain(self, prepare_mongo_heart_report):
        logger = log.Log(sys._getframe().f_code.co_name)
        logger.info("test begining")

        # 1.prepare mongo data (send post request: heart_beat_shard_chain)
        # prepare mongo
        mg = prepare_mongo_heart_report

        # send 2 post request
        req_url = 'http://%s' % conf.apihost_test
        api_url = '%s%s' % (req_url, http_heart_beat.data["url"])
        header = http_heart_beat.data["header"]
        root_data = copy.deepcopy(ws_generate_cmd.data["generate_cmd_single_request_shard_chain"])
        data_req0 = root_data["post_request"][0]
        data_req1 = root_data["post_request"][1]
        data_req0['time'] = common.current_time_iso()
        data_req1['time'] = common.current_time_iso()
        request.post_request(api_url, data_req0, header)
        request.post_request(api_url, data_req1, header)

        # assert db has 2 collections
        assert test.assert_db_counts(mg.find(), 2)

        # 2.send ws request and receive
        ws_url = 'ws://%s' % conf.wshost_test
        ws = mwebsocket.WebSocket(ws_url)
        ws_send_data = root_data['ws_request']
        ws_expc_data_resp = root_data['ws_response']
        ws.send(ws_send_data)
        time.sleep(3)
        ws_resp_data = ws.receive()

        # 3.assert response info
        assert test.assert_text(ws_resp_data['uri'], ws_expc_data_resp['uri'])
        assert common.dict_key_not_exist(ws_resp_data, 'error')
        assert test.assert_text(ws_resp_data['body'], {})
        assert test.assert_text(ws_resp_data['msgId'], ws_expc_data_resp['msgId'])

        # 4.assert mongo data
        mg_data = mg.find()
        ws_expc_data_db = ws_send_data
        ws_expc_data_db['body']['cmd']['params']['amount'] = ws_expc_data_db['body']['cmd']['params']['amount'] / len(mg_data)
        assert test.assert_text(mg_data[0]['cmd'], ws_expc_data_db['body']['cmd'])
        assert test.assert_text(mg_data[1]['cmd'], ws_expc_data_db['body']['cmd'])

    @allure.feature('websocket接口')
    @allure.story('命令生成')
    @pytest.mark.gen_cmd
    def test_generate_cmd_single_request_then_send_post_request(self, prepare_mongo_heart_report):
        logger = log.Log(sys._getframe().f_code.co_name)
        logger.info("test begining")

        # 1.prepare mongo data (send post request: heart_beat_shard_chain)
        # prepare mongo
        mg = prepare_mongo_heart_report

        # 2.send 1 shard chain post request
        req_url = 'http://%s' % conf.apihost_test
        api_url = '%s%s' % (req_url, http_heart_beat.data["url"])
        header = http_heart_beat.data["header"]
        root_data = copy.deepcopy(ws_generate_cmd.data["generate_cmd_single_request_shard_chain"])
        data_req0 = root_data["post_request"][0]
        data_req0['time'] = common.current_time_iso()
        request.post_request(api_url, data_req0, header)

        # 3.send ws request and receive
        ws_url = 'ws://%s' % conf.wshost_test
        ws = mwebsocket.WebSocket(ws_url)
        ws_send_data = root_data['ws_request']
        ws_expc_data_resp = root_data['ws_response']
        ws.send(ws_send_data)
        time.sleep(3)
        ws_resp_data = ws.receive()

        # 4.send 1 shard chain post request again
        http_resp_data = request.post_request(api_url, data_req0, header)

        assert test.assert_code(http_resp_data['code'], 200)
        assert test.assert_body(http_resp_data['body'], 'code', 200)
        assert test.assert_body(http_resp_data['body'], 'message', 'OK')
        assert test.assert_body(http_resp_data['body'], 'data', ws_send_data['body']['cmd'])
        assert test.assert_time(http_resp_data['time_consuming'], 100)

    @allure.feature('websocket接口')
    @allure.story('命令生成')
    @pytest.mark.gen_cmd
    def test_generate_cmd_multi_request_in_15s_shard_chain(self, prepare_mongo_heart_report):
        logger = log.Log(sys._getframe().f_code.co_name)
        logger.info("test begining")

        # 1.prepare mongo data (send post request: heart_beat_shard_chain)
        # prepare mongo
        mg = prepare_mongo_heart_report

        # send 1 post request
        req_url = 'http://%s' % conf.apihost_test
        api_url = '%s%s' % (req_url, http_heart_beat.data["url"])
        header = http_heart_beat.data["header"]
        data_req0 = ws_generate_cmd.data["generate_cmd_multi_request_in_15s_shard_chain"]["post_request"][0]
        data_req0['time'] = common.current_time_iso()
        request.post_request(api_url, data_req0, header)

        # assert db has 1 collections
        assert test.assert_db_counts(mg.find(), 1)

        # 2.send ws request and receive
        ws_url = 'ws://%s' % conf.wshost_test
        ws = mwebsocket.WebSocket(ws_url)
        data = ws_generate_cmd.data['generate_cmd_multi_request_in_15s_shard_chain']
        ws_send_data0 = data['ws_request'][0]
        ws_expc_data_resp0 = data['ws_response'][0]
        ws_send_data1 = data['ws_request'][1]
        ws_expc_data_resp1 = data['ws_response'][1]

        # 3. ws send and receive
        # first time
        ws.send(ws_send_data0)
        time.sleep(3)
        ws_resp_data0 = ws.receive()
        # second time
        ws.send(ws_send_data1)
        time.sleep(3)
        ws_resp_data1 = ws.receive()
        # third time
        ws.send(ws_send_data1)
        time.sleep(3)
        ws_resp_data2 = ws.receive()

        # 3_1.assert response info
        assert test.assert_text(ws_resp_data0['uri'], ws_expc_data_resp0['uri'])
        assert test.assert_text(ws_resp_data0['body'], {})
        assert common.dict_key_not_exist(ws_resp_data0, 'error')
        assert test.assert_text(ws_resp_data0['msgId'], ws_expc_data_resp0['msgId'])

        assert test.assert_text(ws_resp_data1['uri'], ws_expc_data_resp1['uri'])
        assert test.assert_text(ws_resp_data1['body'], {})
        assert common.dict_key_exist(ws_resp_data1, 'error')
        assert test.assert_body_code_ge(ws_resp_data1['error'], ws_expc_data_resp1['error']["code"])
        assert test.assert_text(ws_resp_data1['msgId'], ws_expc_data_resp1['msgId'])

        assert test.assert_text(ws_resp_data2['uri'], ws_expc_data_resp1['uri'])
        assert test.assert_text(ws_resp_data2['body'], {})
        assert common.dict_key_exist(ws_resp_data2, 'error')
        assert test.assert_body_code_ge(ws_resp_data1['error'], ws_expc_data_resp1['error']["code"])
        assert test.assert_text(ws_resp_data2['msgId'], ws_expc_data_resp1['msgId'])

        # 4.assert mongo data
        mg_data = mg.find()
        ws_expc_data_db = ws_send_data0
        assert test.assert_text(mg_data[0]['cmd'], ws_expc_data_db['body']['cmd'])

    @allure.feature('websocket接口')
    @allure.story('命令生成')
    @pytest.mark.gen_cmd
    def test_generate_cmd_multi_request_after_15s_shard_chain(self, prepare_mongo_heart_report):
        logger = log.Log(sys._getframe().f_code.co_name)
        logger.info("test begining")

        # 1.prepare mongo data (send post request: heart_beat_shard_chain)
        # prepare mongo
        mg = prepare_mongo_heart_report

        # send 1 post request
        req_url = 'http://%s' % conf.apihost_test
        api_url = '%s%s' % (req_url, http_heart_beat.data["url"])
        header = http_heart_beat.data["header"]
        data_req0 = ws_generate_cmd.data["generate_cmd_multi_request_after_15s_shard_chain"]["post_request"][0]
        data_req0['time'] = common.current_time_iso()
        request.post_request(api_url, data_req0, header)

        # assert db has 1 collections
        assert test.assert_db_counts(mg.find(), 1)

        # 2.send ws request and receive
        ws_url = 'ws://%s' % conf.wshost_test
        ws = mwebsocket.WebSocket(ws_url)
        data = ws_generate_cmd.data['generate_cmd_multi_request_after_15s_shard_chain']
        ws_send_data0 = data['ws_request'][0]
        ws_expc_data_resp0 = data['ws_response'][0]
        ws_send_data1 = data['ws_request'][1]
        ws_expc_data_resp1 = data['ws_response'][1]

        # 3. ws send and receive
        # first time
        ws.send(ws_send_data0)
        time.sleep(3)
        ws_resp_data0 = ws.receive()
        # second time
        time.sleep(13)
        ws.send(ws_send_data1)
        time.sleep(3)
        ws_resp_data1 = ws.receive()

        # 3_1.assert response info
        assert test.assert_text(ws_resp_data0['uri'], ws_expc_data_resp0['uri'])
        assert test.assert_text(ws_resp_data0['body'], {})
        assert common.dict_key_not_exist(ws_resp_data0, 'error')
        assert test.assert_text(ws_resp_data0['msgId'], ws_expc_data_resp0['msgId'])

        assert test.assert_text(ws_resp_data1['uri'], ws_expc_data_resp1['uri'])
        assert test.assert_text(ws_resp_data1['body'], {})
        assert common.dict_key_not_exist(ws_resp_data1, 'error')
        assert test.assert_text(ws_resp_data1['msgId'], ws_expc_data_resp1['msgId'])

        # 4.assert mongo data
        mg_data = mg.find()
        ws_expc_data_db = ws_send_data0
        assert test.assert_text(mg_data[0]['cmd'], ws_expc_data_db['body']['cmd'])

    @allure.feature('websocket接口')
    @allure.story('命令生成')
    @pytest.mark.gen_cmd
    def test_generate_cmd_with_no_nodes(self, prepare_mongo_heart_report):
        logger = log.Log(sys._getframe().f_code.co_name)
        logger.info("test begining")

        # 1.prepare mongo data (send post request: heart_beat_shard_chain)
        # prepare mongo
        prepare_mongo_heart_report

        root_data = copy.deepcopy(ws_generate_cmd.data["generate_cmd_with_no_nodes"])

        # 2.send ws request and receive
        ws_url = 'ws://%s' % conf.wshost_test
        ws = mwebsocket.WebSocket(ws_url)
        ws_send_data = root_data['ws_request']
        ws_expc_data_resp = root_data['ws_response']
        ws.send(ws_send_data)
        time.sleep(3)
        ws_resp_data = ws.receive()

        # 3.assert response info
        assert test.assert_text(ws_resp_data['uri'], ws_expc_data_resp['uri'])
        assert common.dict_key_exist(ws_resp_data, 'error')
        assert test.assert_body_code_ge(ws_resp_data['error'], ws_expc_data_resp['error']['code'])
        assert test.assert_text(ws_resp_data['body'], {})
        assert test.assert_text(ws_resp_data['msgId'], ws_expc_data_resp['msgId'])

    @allure.feature('websocket接口')
    @allure.story('实时区块信息(订阅)')
    @pytest.mark.block_realtime
    def test_get_real_chain_block_info_with_no_sub(self):
        logger = log.Log(sys._getframe().f_code.co_name)
        logger.info("test begining")

        # 1.creat websocket collection
        ws_url = 'ws://%s' % conf.wshost_test
        ws = mwebsocket.WebSocket(ws_url)

        # 2.send 1 post request before subscription
        req_url = 'http://%s' % conf.apihost_test
        api_url = '%s%s' % (req_url, http_block_reported.data["url"])
        header = http_block_reported.data["header"]
        root_data = copy.deepcopy(ws_get_block_info_realtime.data["get_real_chain_block_info"])
        data_req = root_data["post_request"]
        data_req0 = data_req[0]
        data_req0['time'] = common.current_time_iso()
        # for no subscription
        ws_wait_time = 10
        post_wait_time = 6
        ws_send_data = root_data['ws_request'][0]
        t1 = threading.Thread(target=self.ws_recv, name='ws_recv', args=(ws,))
        t2 = threading.Thread(target=self.ws_send_for_subscription, name='ws_send', args=(ws, ws_send_data, ws_wait_time))
        t3 = threading.Thread(target=self.ws_count, name='ws_count', args=(ws_wait_time,))
        t4 = threading.Thread(target=self.http_post_request, name='post_request', args=(api_url, data_req0, header, post_wait_time))
        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t1.join()
        t2.join()
        t3.join()
        t4.join()
        logger.info(f'===ws_recv spendtime: {TestWSAPITest.spendtime}')
        logger.info(f'===ws_recv get response: {TestWSAPITest.ws_recv_data}')
        assert test.assert_text(TestWSAPITest.spendtime, ws_wait_time)
        assert test.assert_key_not_exist(TestWSAPITest.ws_recv_data, 'error')
        assert test.assert_text(TestWSAPITest.ws_recv_data, root_data['ws_response'][-1])
        # assert TestWSAPITest.ws_recv_data == data['ws_response'][-1]

    @allure.feature('websocket接口')
    @allure.story('实时区块信息(订阅)')
    @pytest.mark.block_realtime
    def test_get_real_chain_block_info_with_sub(self, prepare_mongo_block_report):
        logger = log.Log(sys._getframe().f_code.co_name)
        logger.info("test begining")

        # 1.creat websocket collection
        ws_url = 'ws://%s' % conf.wshost_test
        ws = mwebsocket.WebSocket(ws_url)

        # 2.clear mongo database
        mgdbs = prepare_mongo_block_report

        # 3.news subscription
        root_data = copy.deepcopy(ws_get_block_info_realtime.data['get_real_chain_block_info'])
        ws_send_data = root_data['ws_request'][0]
        ws_expc_data_resp_tmp = root_data['ws_response']
        ws.send(ws_send_data)
        ws.receive()
        time.sleep(3)

        # 4.send post request after subscription
        req_url = 'http://%s' % conf.apihost_test
        api_url = '%s%s' % (req_url, http_block_reported.data["url"])
        header = http_block_reported.data["header"]
        data_req = ws_get_block_info_realtime.data["get_real_chain_block_info"]["post_request"]
        logger.info(f'debug data_req: {data_req}')
        data_req0 = data_req[0]
        data_req0['time'] = common.current_time_iso()
        data_req1 = data_req[1]
        data_req1['time'] = common.current_time_iso()
        data_req2 = data_req[2]
        data_req2['time'] = common.current_time_iso()

        ws_wait_time = 12
        ws_recv_wait_time = 9
        ws_send_data = root_data['ws_request'][0]
        t1 = threading.Thread(target=self.ws_recv_multi, name='ws_recv', args=(ws, ws_recv_wait_time))
        t2 = threading.Thread(target=self.ws_send_for_subscription, name='ws_send', args=(ws, ws_send_data, ws_wait_time))
        t3 = threading.Thread(target=self.ws_count, name='ws_count', args=(ws_wait_time,))
        t4 = threading.Thread(target=self.http_post_request, name='post_request', args=(api_url, data_req0, header, 2))
        t5 = threading.Thread(target=self.http_post_request, name='post_request', args=(api_url, data_req1, header, 2))
        t6 = threading.Thread(target=self.http_post_request, name='post_request', args=(api_url, data_req2, header, 5))
        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t5.start()
        t6.start()
        t1.join()
        t2.join()
        t3.join()
        t4.join()
        t5.join()
        t6.join()
        logger.info(f'===ws_recv spendtime: {TestWSAPITest.spendtime}')
        logger.info(f'===ws_recv get response: {TestWSAPITest.ws_recv_data}')
        logger.info(f'===ws_recv get response: {TestWSAPITest.ws_recv_data1}')
        logger.info(f'===ws_recv get response: {TestWSAPITest.ws_recv_data2}')
        # websocket server change send time to 1/5pers，so cancel this check(wait time must be the same as spend time)
        # assert test.assert_text(TestWSAPITest.spendtime, ws_recv_wait_time)
        assert test.assert_text(TestWSAPITest.ws_recv_data['event'], ws_send_data['event'])

        # 5.check ws recv
        time.sleep(3)
        ws_resp_data = TestWSAPITest.ws_recv_data['body']
        logger.info(f'ws_resp_data :{ws_resp_data}')

        # 6.assert response info
        ws_expc_data_resp = []
        for i in ws_expc_data_resp_tmp[0:-1]:
            ws_expc_data_resp.append(i['body'][0])
        # 响应体中信息 与 post 请求的信息一致
        assert test.assert_db_counts(ws_resp_data, 1)
        for i in ws_expc_data_resp:  # clear dict key (time)
            logger.info(i)
            i.pop('time')

        for ws_resp_data_i in ws_resp_data:
            ws_resp_data_i.pop('time')
            if ws_resp_data_i in ws_expc_data_resp:
                logger.info("Case Assert success : response data -> %s <- in %s" % (ws_resp_data_i, ws_expc_data_resp))
            else:
                logger.error("Case Assert failed : response data -> \n%s \n<- not in \n%s" % (ws_resp_data_i, ws_expc_data_resp))
                raise

        # 7.assert mongo data
        # 数据库中信息 与 post 请求的信息一致
        mg_data = mgdbs['lslqksj'].find()
        ws_expc_data_db = data_req
        logger.info(f'debug data_req: {data_req}')
        assert test.assert_db_counts(mg_data, len(ws_expc_data_db))
        for i in ws_expc_data_db:  # clear dict key (time)
            logger.info(i)
            i.pop('time')
            i['miner'] = i['nodeId']  # change key name: 'nodeId' to 'miner'
            i.pop('nodeId')
        for mg_data_tmp in mg_data:
            mg_data_tmp.pop('time')
            mg_data_tmp.pop('updateTime')
            for i in range(len(ws_expc_data_db)):
                if ws_expc_data_db[i]['hash'] == mg_data_tmp['hash']:
                    if mg_data_tmp == ws_expc_data_db[i]:
                        logger.info("Case Assert success : database info: %s == ws_expc_data_resp: %s" % (mg_data_tmp, ws_expc_data_db[i]))
                    elif i ==  len(ws_expc_data_db) - 1:
                        logger.info("Case Assert failed : database info: \n%s \n!= \nws_expc_data_resp: \n%s" % (mg_data_tmp, ws_expc_data_db[i]))
                        raise

    @allure.feature('websocket接口')
    @allure.story('实时区块信息(订阅)')
    @pytest.mark.block_realtime
    def test_get_real_chain_block_info_with_wrong_post_request(self, prepare_mongo_block_report):
        logger = log.Log(sys._getframe().f_code.co_name)
        logger.info("test begining")

        # 1.creat websocket collection
        ws_url = 'ws://%s' % conf.wshost_test
        ws = mwebsocket.WebSocket(ws_url)

        # 2.book news subscription
        root_data = copy.deepcopy(ws_get_block_info_realtime.data['get_real_chain_block_info_with_wrong_post_request'])
        ws_send_data = root_data['ws_request'][0]
        ws_expc_data_resp = root_data['ws_response'][0]['body']
        ws.send(ws_send_data)
        ws.receive()
        time.sleep(3)

        # 3.send wrong post request after subscription
        # prepare mongo
        mgdbs = prepare_mongo_block_report

        # 3_2.send post request
        req_url = 'http://%s' % conf.apihost_test
        api_url = '%s%s' % (req_url, http_block_reported.data["url"])
        header = http_block_reported.data["header"]
        data_req = root_data["post_request"]
        data_req0 = data_req[0]
        data_req0['time'] = common.current_time_iso()

        ws_wait_time = 15
        post_wait_time = 6
        # ws_send_data = data['ws_request'][0]
        t1 = threading.Thread(target=self.ws_recv, name='ws_recv', args=(ws,))
        t2 = threading.Thread(target=self.ws_send_for_subscription, name='ws_send', args=(ws, ws_send_data, ws_wait_time))
        t3 = threading.Thread(target=self.ws_count, name='ws_count', args=(ws_wait_time,))
        t4 = threading.Thread(target=self.http_post_request, name='post_request', args=(api_url, data_req0, header, post_wait_time))
        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t1.join()
        t2.join()
        t3.join()
        t4.join()
        logger.info(f'===ws_recv spendtime: {TestWSAPITest.spendtime}')
        logger.info(f'===ws_recv get response: {TestWSAPITest.ws_recv_data}')
        assert test.assert_text(TestWSAPITest.spendtime, ws_wait_time)
        assert test.assert_text(TestWSAPITest.ws_recv_data, root_data['ws_response'][0])

    @allure.feature('websocket接口')
    @allure.story('实时区块信息(订阅)')
    @pytest.mark.block_realtime
    def test_get_real_chain_block_info_with_wrong_ws_book_event(self):
        logger = log.Log(sys._getframe().f_code.co_name)
        logger.info("test begining")

        # 1.creat websocket collection
        ws_url = 'ws://%s' % conf.wshost_test
        ws = mwebsocket.WebSocket(ws_url)

        # 2.book news subscription
        data = ws_get_block_info_realtime.data['get_real_chain_block_info_with_wrong_ws_book_event']
        ws_send_data = data['ws_request'][0]
        ws_expc_data_resp = data['ws_response'][0]

        # 3.send wrong ws book subscription
        ws_wait_time = 10
        t1 = threading.Thread(target=self.ws_recv, name='ws_recv', args=(ws,))
        t2 = threading.Thread(target=self.ws_send_for_subscription, name='ws_send', args=(ws, ws_send_data, ws_wait_time))
        t3 = threading.Thread(target=self.ws_count, name='ws_count', args=(ws_wait_time,))
        t1.start()
        t2.start()
        t3.start()
        t1.join()
        t2.join()
        t3.join()
        logger.info(f'===ws_recv spendtime: {TestWSAPITest.spendtime}')
        logger.info(f'===ws_recv get response: {TestWSAPITest.ws_recv_data}')
        assert test.assert_text(TestWSAPITest.spendtime, ws_wait_time)
        assert test.assert_key_exist(TestWSAPITest.ws_recv_data, 'error')
        assert test.assert_body_code_ge(TestWSAPITest.ws_recv_data['error'], ws_expc_data_resp['error']['code'])




    # @allure.feature('websocket接口')
    # @allure.story('单区块信息获取')
    # def test_get_block_info_of_shard_chain(self, prepare_mongo_block_report):
    #     logger = log.Log(sys._getframe().f_code.co_name)
    #     logger.info("test begining")
    #     # 1.clear mongo
    #     mgdbs = prepare_mongo_block_report
    #
    #     # 2.send post request
    #     req_url = 'http://%s' % conf.apihost_test
    #     api_url = '%s%s' % (req_url, http_block_reported.data["url"])
    #     header = http_block_reported.data["header"]
    #     data_req = http_block_reported.data["block_reported_shard_chain"]["request"]
    #     # data_resp = http_block_reported.data["block_reported_shard_chain"]["response"]
    #     data_req['time'] = common.current_time_iso()
    #     request.post_request(api_url, data_req, header)
    #     # assert db has 1 collections
    #     assert test.assert_db_counts(mgdbs['lslqksj'].find(), 1)
    #
    #     # 3.send ws request and receive
    #     ws_url = 'ws://%s' % conf.wshost_test
    #     ws = mwebsocket.WebSocket(ws_url)
    #     data = ws_generate_cmd.data['get_block_info_of_shard_chain']
    #     req = data['ws_request']
    #     resp_exp = data['ws_response']
    #     ws.send(req)
    #     time.sleep(3)
    #     ws_resp = ws.receive()
    #
    #     # 4.assert response info
    #     assert test.assert_text(ws_resp['uri'], 'blockInfo')
    #     assert test.assert_text(ws_resp['body'], resp_exp['body'])
    #     assert test.assert_text(ws_resp['msgId'], resp_exp['msgId'])
    #
    #     # 5.assert mongo data
    #     mg_data = mgdbs['lslqksj'].find()
    #     assert test.assert_db_text(mg_data[0]['type'], resp_exp['type'])
    #     assert test.assert_db_text(mg_data[0]['chainKey'], resp_exp['chainKey'])
    #     assert test.assert_db_text(mg_data[0]['nodeId'], resp_exp['nodeId'])
    #     assert test.assert_db_text(mg_data[0]['height'], resp_exp['height'])
    #     assert test.assert_db_text(mg_data[0]['father'], resp_exp['father'])
    #     assert test.assert_db_text(mg_data[0]['hash'], resp_exp['hash'])
    #     assert test.assert_db_text(mg_data[0]['vrf'], resp_exp['vrf'])
    #     assert test.assert_db_text(mg_data[0]['interval'], resp_exp['interval'])
    #     assert test.assert_db_text(mg_data[0]['trans'], resp_exp['trans'])
    #     assert test.assert_db_text(mg_data[0]['size'], resp_exp['size'])
    #     assert test.assert_db_text(mg_data[0]['detail']['upStream'], resp_exp['detail']['upStream'])
    #     assert test.assert_db_text(mg_data[0]['detail']['downStream'], resp_exp['detail']['downStream'])

