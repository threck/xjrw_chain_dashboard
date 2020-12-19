# -*- coding:utf-8 -*-
# @Author      : FangChao
# @File        : test_api
# @Date        : 2020/12/2 0002
# @Description : xjrw_chain_dashboard

import pytest
import allure
import time
import random
import json
import sys
import requests
import copy
import pytz
from Config import config
from Common import mrequest
from Common import consts
from Common import common
from Common import massert
from Common import log
from Common import mongo

from Param.req_resp_data import http_heart_beat
from Param.req_resp_data import http_block_reported

conf = config.Config()
request = mrequest.Request()
test = massert.Assertions()


def http_assert(response, data_resp):
    assert test.assert_code(response['code'], 200)
    assert test.assert_body(response['body'], 'code', data_resp['code'])
    assert test.assert_body(response['body'], 'message', data_resp['message'])
    assert test.assert_body(response['body'], 'data', data_resp['data'])
    assert test.assert_time(response['time_consuming'], 100)


def db_jdxx_assert(mg_data, data_req, logger, db_counts=1):
    logger.info(f'data base info: {mg_data}')
    assert test.assert_db_counts(mg_data, db_counts)
    assert test.assert_db_text(mg_data[0]['type'], data_req['type'])
    assert test.assert_db_text(mg_data[0]['chainKey'], data_req['chainKey'])
    assert test.assert_db_text(mg_data[0]['nodeId'], data_req['nodeId'])
    assert test.assert_value_not_None(mg_data[0]['lastTime'])
    # mongo_time = mg_data[0]['lastTime'].astimezone(pytz.utc)
    # request_time = common.isostr_to_datetime(data_req['time']).astimezone(pytz.utc)
    # mongo_time_iso = mongo_time.isoformat('T')
    # request_time_iso = request_time.isoformat('T')
    # logger.info(f'mongo time:{mongo_time}, request_time : {request_time}')
    # logger.info(f'mongo time iso:{mongo_time_iso}, request_time iso: {request_time_iso}')
    # logger.info(f'mongo time timestamp:{mongo_time.timestamp()}, request_time timestamp: {request_time.timestamp()}')
    # assert test.assert_db_text(mongo_time.timestamp(), request_time.timestamp())


def db_lslqksj_assert(mg_data, data_req, logger, db_counts=1):
    logger.info(f'data base info: {mg_data}')
    assert test.assert_db_counts(mg_data, db_counts)
    assert test.assert_db_text(mg_data[0]['type'], data_req['type'])
    assert test.assert_db_text(mg_data[0]['chainKey'], data_req['chainKey'])
    assert test.assert_db_text(mg_data[0]['miner'], data_req['nodeId'])
    assert test.assert_db_text(mg_data[0]['height'], data_req['height'])
    assert test.assert_db_text(mg_data[0]['father'], data_req['father'])
    assert test.assert_db_text(mg_data[0]['gas'], data_req['gas'])
    assert test.assert_db_text(mg_data[0]['hash'], data_req['hash'])
    assert test.assert_db_text(mg_data[0]['vrf'], data_req['vrf'])
    assert test.assert_db_text(mg_data[0]['interval'], data_req['interval'])
    assert test.assert_db_text(mg_data[0]['trans'], data_req['trans'])
    assert test.assert_db_text(mg_data[0]['size'], data_req['size'])
    assert test.assert_db_text(mg_data[0]['upHash'], data_req['upHash'])
    assert test.assert_db_text(mg_data[0]['downHash'], data_req['downHash'])
    assert test.assert_db_text(mg_data[0]['lockHash'], data_req['lockHash'])
    assert test.assert_db_text(mg_data[0]['detail']['upStream'], data_req['detail']['upStream'])
    assert test.assert_db_text(mg_data[0]['detail']['downStream'], data_req['detail']['downStream'])


def db_sslsj_assert(mg_data, data_req, logger, db_counts=1):
    logger.info(f'data base info: {mg_data}')
    assert test.assert_db_counts(mg_data, db_counts)
    assert test.assert_db_text(mg_data[0]['chainKey'], data_req['chainKey'])
    assert test.assert_db_text(mg_data[0]['height'], data_req['height'])
    assert test.assert_db_text(mg_data[0]['interval'], data_req['interval'])
    assert test.assert_db_text(mg_data[0]['size'], data_req['size'])
    assert test.assert_db_text(mg_data[0]['trans'], data_req['trans'])
    assert test.assert_db_text(mg_data[0]['type'], data_req['type'])
    assert test.assert_db_text(mg_data[0]['tps'], data_req['trans'] / data_req['interval'])


def db_kfpjyzsj_assert(mg_data, data_req, logger):
    logger.info(f'data base info: {mg_data}')

    data_req_height = data_req['height']
    data_req_ss = data_req['detail']['ss']
    for req in data_req_ss:
        req['trans'] = len(req['trans'])
        req['height'] = data_req_height

    logger.info(f'data_req info: {data_req}')
    db_counts = len(data_req_ss)
    assert test.assert_db_counts(mg_data, db_counts)

    for req in data_req_ss:
        if req in mg_data:
            logger.info("Case Assert success : request data %s in %s" % (req, mg_data))
        else:
            logger.error("Case Assert failed : request data %s not in %s" % (req, mg_data))
            raise


def db_jysj_assert(mg_data, data_req, logger):
    logger.info(f'data base info: {mg_data}')

    data_req_height = data_req['height']
    data_req_ss = data_req['detail']['ss']
    new_data_list = []
    for req in data_req_ss:
        for trans_tmp in req['trans']:
            trans_tmp['fromShard'] = req['fromShard']
            trans_tmp['toShard'] = req['toShard']
            trans_tmp['height'] = data_req_height
            new_data_list.append(trans_tmp)

    logger.info(f'data_req info: {new_data_list}')
    db_counts = len(new_data_list)
    assert test.assert_db_counts(mg_data, db_counts)

    for req in new_data_list:
        if req in mg_data:
            logger.info("Case Assert success : request data %s in %s" % (req, mg_data))
        else:
            logger.error("Case Assert failed : request data %s not in %s" % (req, mg_data))
            raise


@pytest.mark.http
class TestHTTPAPITest:
    @allure.feature('http_接口')
    @allure.story('节点上报接口_心跳上报')
    @pytest.mark.heart_report
    def test_heart_beat_shard_chain(self, prepare_mongo_heart_report):
        logger = log.Log(sys._getframe().f_code.co_name)
        logger.info("test begining")
        # 1.clear mongo
        mg = prepare_mongo_heart_report

        # 2.send post request
        req_url = 'http://%s' % conf.apihost_test
        api_url = '%s%s' % (req_url, http_heart_beat.data["url"])
        header = http_heart_beat.data["header"]
        data_req = http_heart_beat.data["heart_beat_shard_chain"]["request"]
        data_resp = http_heart_beat.data["heart_beat_shard_chain"]["response"]
        data_req['time'] = common.current_time_iso()
        response = request.post_request(api_url, data_req, header)

        # 3.assert response info
        http_assert(response, data_resp)

        # 4.assert mongo data
        mg_data = mg.find()
        db_jdxx_assert(mg_data, data_req, logger, db_counts=1)

    @allure.feature('http_接口')
    @allure.story('节点上报接口_心跳上报')
    @pytest.mark.heart_report
    def test_heart_beat_duplicated_data(self, prepare_mongo_heart_report):
        logger = log.Log(sys._getframe().f_code.co_name)
        logger.info("test begining")
        # 1.clear mongo
        mg = prepare_mongo_heart_report

        # 2.send post request two times with duplicated data
        req_url = 'http://%s' % conf.apihost_test
        api_url = '%s%s' % (req_url, http_heart_beat.data["url"])
        header = http_heart_beat.data["header"]
        data_req = http_heart_beat.data["heart_beat_duplicated_data"]["request"]
        data_resp = http_heart_beat.data["heart_beat_duplicated_data"]["response"]
        data_req['time'] = common.current_time_iso()
        response_tmp = request.post_request(api_url, data_req, header)
        response = request.post_request(api_url, data_req, header)

        # 3.assert response info
        http_assert(response, data_resp)

        # 4.assert mongo data
        mg_data = mg.find()
        db_jdxx_assert(mg_data, data_req, logger, db_counts=1)

    @allure.feature('http_接口')
    @allure.story('节点上报接口_心跳上报')
    @pytest.mark.heart_report
    def test_heart_beat_update_data(self, prepare_mongo_heart_report):
        logger = log.Log(sys._getframe().f_code.co_name)
        logger.info("test begining")
        # 1.clear mongo
        mg = prepare_mongo_heart_report

        # 2.send post request two times with different data
        req_url = 'http://%s' % conf.apihost_test
        api_url = '%s%s' % (req_url, http_heart_beat.data["url"])
        header = http_heart_beat.data["header"]
        data_req1 = http_heart_beat.data["heart_beat_update_data"]["request"][0]
        data_req2 = http_heart_beat.data["heart_beat_update_data"]["request"][1]
        data_resp = http_heart_beat.data["heart_beat_update_data"]["response"]
        data_req1['time'] = common.current_time_iso()
        data_req2['time'] = common.current_time_iso()
        response_tmp = request.post_request(api_url, data_req1, header)
        response = request.post_request(api_url, data_req2, header)

        # 3.assert response info
        http_assert(response, data_resp)

        # 4.assert mongo data
        mg_data = mg.find()
        db_jdxx_assert(mg_data, data_req2, logger, db_counts=1)

    @allure.feature('http_接口')
    @allure.story('节点上报接口_心跳上报')
    @pytest.mark.heart_report
    def test_heart_beat_wrong_value_chain_type(self, prepare_mongo_heart_report):
        logger = log.Log(sys._getframe().f_code.co_name)
        logger.info("test begining")
        # 1.clear mongo
        mg = prepare_mongo_heart_report

        # 2.send post request
        req_url = 'http://%s' % conf.apihost_test
        api_url = '%s%s' % (req_url, http_heart_beat.data["url"])
        header = http_heart_beat.data["header"]
        data_req = http_heart_beat.data["heart_beat_wrong_value_chain_type"]["request"]
        data_resp = http_heart_beat.data["heart_beat_wrong_value_chain_type"]["response"]
        data_req['time'] = common.current_time_iso()
        response = request.post_request(api_url, data_req, header)

        # 3.assert response info
        assert test.assert_code(response['code'], 200)
        assert test.assert_body_code_ge(response['body'], data_resp['code'])
        assert test.assert_time(response['time_consuming'], 100)

        # 4.assert mongo data
        mg_data = mg.find()
        assert test.assert_db_counts(mg_data, 0)

    @allure.feature('http_接口')
    @allure.story('节点上报接口_心跳上报')
    @pytest.mark.heart_report
    def test_heart_beat_null_value_chain_type(self, prepare_mongo_heart_report):
        logger = log.Log(sys._getframe().f_code.co_name)
        logger.info("test begining")
        # 1.clear mongo
        mg = prepare_mongo_heart_report

        # 2.send post request
        req_url = 'http://%s' % conf.apihost_test
        api_url = '%s%s' % (req_url, http_heart_beat.data["url"])
        header = http_heart_beat.data["header"]
        data_req = http_heart_beat.data["heart_beat_null_value_chain_type"]["request"]
        data_resp = http_heart_beat.data["heart_beat_null_value_chain_type"]["response"]
        data_req['time'] = common.current_time_iso()
        response = request.post_request(api_url, data_req, header)

        # 3.assert response info
        assert test.assert_code(response['code'], 200)
        assert test.assert_body_code_ge(response['body'], data_resp['code'])
        assert test.assert_time(response['time_consuming'], 100)

        # 4.assert mongo data
        mg_data = mg.find()
        assert test.assert_db_counts(mg_data, 0)


    @allure.feature('http_接口')
    @allure.story('节点上报接口_区块上报')
    @pytest.mark.block_report
    def test_block_reported_shard_chain(self, prepare_mongo_block_report):
        logger = log.Log(sys._getframe().f_code.co_name)
        logger.info("test begining")
        # 1.clear mongo
        mgdbs = prepare_mongo_block_report

        # 2.send post request
        req_url = 'http://%s' % conf.apihost_test
        api_url = '%s%s' % (req_url, http_block_reported.data["url"])
        header = http_block_reported.data["header"]
        data_req = http_block_reported.data["block_reported_shard_chain"]["request"]
        data_resp = http_block_reported.data["block_reported_shard_chain"]["response"]
        data_req['time'] = common.current_time_iso()
        response = request.post_request(api_url, data_req, header)

        # 3.assert response info
        http_assert(response, data_resp)

        # 4.assert mongo data
        mg_sslsj_data = mgdbs['sslsj'].find()
        mg_lslqksj_data = mgdbs['lslqksj'].find()
        mg_kfpjyzsj_data = mgdbs['kfpjyzsj'].find()
        mg_jysj_data = mgdbs['jysj'].find()
        db_sslsj_assert(mg_sslsj_data, copy.deepcopy(data_req), logger, db_counts=1)
        db_lslqksj_assert(mg_lslqksj_data, copy.deepcopy(data_req), logger, db_counts=1)
        db_kfpjyzsj_assert(mg_kfpjyzsj_data, copy.deepcopy(data_req), logger)
        db_jysj_assert(mg_jysj_data, copy.deepcopy(data_req), logger)


    @allure.feature('http_接口')
    @allure.story('节点上报接口_区块上报')
    @pytest.mark.block_report
    def test_block_reported_relay_chain(self, prepare_mongo_block_report):
        logger = log.Log(sys._getframe().f_code.co_name)
        logger.info("test begining")
        # 1.clear mongo
        mgdbs = prepare_mongo_block_report

        # 2.send post request
        req_url = 'http://%s' % conf.apihost_test
        api_url = '%s%s' % (req_url, http_block_reported.data["url"])
        header = http_block_reported.data["header"]
        data_req = http_block_reported.data["block_reported_relay_chain"]["request"]
        data_resp = http_block_reported.data["block_reported_relay_chain"]["response"]
        data_req['time'] = common.current_time_iso()
        response = request.post_request(api_url, data_req, header)

        # 3.assert response info
        http_assert(response, data_resp)

        # 4.assert mongo data
        mg_sslsj_data = mgdbs['sslsj'].find()
        mg_lslqksj_data = mgdbs['lslqksj'].find()
        db_sslsj_assert(mg_sslsj_data, copy.deepcopy(data_req), logger, db_counts=1)
        db_lslqksj_assert(mg_lslqksj_data, copy.deepcopy(data_req), logger, db_counts=1)


    @allure.feature('http_接口')
    @allure.story('节点上报接口_区块上报')
    @pytest.mark.block_report
    def test_block_reported_beacon_chain(self, prepare_mongo_block_report):
        logger = log.Log(sys._getframe().f_code.co_name)
        logger.info("test begining")
        # 1.clear mongo
        mgdbs = prepare_mongo_block_report

        # 2.send post request
        req_url = 'http://%s' % conf.apihost_test
        api_url = '%s%s' % (req_url, http_block_reported.data["url"])
        header = http_block_reported.data["header"]
        data_req = http_block_reported.data["block_reported_beacon_chain"]["request"]
        data_resp = http_block_reported.data["block_reported_beacon_chain"]["response"]
        data_req['time'] = common.current_time_iso()
        response = request.post_request(api_url, data_req, header)

        # 3.assert response info
        http_assert(response, data_resp)

        # 4.assert mongo data
        mg_sslsj_data = mgdbs['sslsj'].find()
        mg_lslqksj_data = mgdbs['lslqksj'].find()
        db_sslsj_assert(mg_sslsj_data, copy.deepcopy(data_req), logger, db_counts=1)
        db_lslqksj_assert(mg_lslqksj_data, copy.deepcopy(data_req), logger, db_counts=1)


    @allure.feature('http_接口')
    @allure.story('节点上报接口_区块上报')
    @pytest.mark.block_report
    def test_block_reported_relay_chain_duplicated_data(self, prepare_mongo_block_report):
        logger = log.Log(sys._getframe().f_code.co_name)
        logger.info("test begining")
        # 1.clear mongo
        mgdbs = prepare_mongo_block_report

        # 2.send post request
        req_url = 'http://%s' % conf.apihost_test
        api_url = '%s%s' % (req_url, http_block_reported.data["url"])
        header = http_block_reported.data["header"]
        data_req = http_block_reported.data["block_reported_duplicated_data"]["request"]
        data_resp = http_block_reported.data["block_reported_duplicated_data"]["response"]
        data_req['time'] = common.current_time_iso()

        logger.info(f'send post request 1st time: {api_url}')
        response_tmp = request.post_request(api_url, data_req, header)
        logger.info(f'send post request 1st time: {api_url}')
        response = request.post_request(api_url, data_req, header)

        # 3.assert response info
        http_assert(response, data_resp)

        # 4.assert mongo data
        mg_sslsj_data = mgdbs['sslsj'].find()
        mg_lslqksj_data = mgdbs['lslqksj'].find()
        db_sslsj_assert(mg_sslsj_data, copy.deepcopy(data_req), logger, db_counts=1)
        db_lslqksj_assert(mg_lslqksj_data, copy.deepcopy(data_req), logger, db_counts=1)


    @allure.feature('http_接口')
    @allure.story('节点上报接口_区块上报')
    @pytest.mark.block_report
    def test_block_reported_relay_chain_update_data(self, prepare_mongo_block_report):
        logger = log.Log(sys._getframe().f_code.co_name)
        logger.info("test begining")
        # 1.clear mongo
        mgdbs = prepare_mongo_block_report

        # 2.send post request
        req_url = 'http://%s' % conf.apihost_test
        api_url = '%s%s' % (req_url, http_block_reported.data["url"])
        header = http_block_reported.data["header"]
        data_req1 = http_block_reported.data["block_reported_update_data"]["request"][0]
        data_resp_expc = http_block_reported.data["block_reported_update_data"]["response"]
        data_req1['time'] = common.current_time_iso()
        # data_req1['nodeId'] = common.base58_encode(data_req1['nodeId'])
        data_req2 = http_block_reported.data["block_reported_update_data"]["request"][1]
        data_req2['time'] = common.current_time_iso()

        logger.info(f'send post request 1st time: {api_url}')
        response_tmp = request.post_request(api_url, data_req1, header)
        logger.info(f'send post request 2nd time: {api_url}')
        response = request.post_request(api_url, data_req2, header)

        # 3.assert response info
        http_assert(response, data_resp_expc)

        # 4.assert mongo data
        mg_sslsj_data = mgdbs['sslsj'].find()
        mg_lslqksj_data = mgdbs['lslqksj'].find()
        db_sslsj_assert(mg_sslsj_data, copy.deepcopy(data_req2), logger, db_counts=1)
        db_lslqksj_assert(mg_lslqksj_data, copy.deepcopy(data_req2), logger, db_counts=1)


    @allure.feature('http_接口')
    @allure.story('节点上报接口_区块上报')
    @pytest.mark.block_report
    def test_block_reported_relay_chain_wrong_value_chain_type(self, prepare_mongo_block_report):
        logger = log.Log(sys._getframe().f_code.co_name)
        logger.info("test begining")
        # 1.clear mongo
        mgdbs = prepare_mongo_block_report

        # 2.send post request
        req_url = 'http://%s' % conf.apihost_test
        api_url = '%s%s' % (req_url, http_block_reported.data["url"])
        header = http_block_reported.data["header"]
        data_req = http_block_reported.data["block_reported_wrong_value_chain_type"]["request"]
        data_resp = http_block_reported.data["block_reported_wrong_value_chain_type"]["response"]
        data_req['time'] = common.current_time_iso()
        response = request.post_request(api_url, data_req, header)

        # 3.assert response info
        assert test.assert_code(response['code'], 200)
        assert test.assert_body_code_ge(response['body'], data_resp['code'])
        # assert test.assert_body(response['body'], 'data', data_resp['data'])
        assert test.assert_time(response['time_consuming'], 100)

        # 4.assert mongo data
        mg_sslsj_data = mgdbs['sslsj'].find()
        mg_lslqksj_data = mgdbs['lslqksj'].find()
        mg_kfpjyzsj_data = mgdbs['kfpjyzsj'].find()
        mg_jysj_data = mgdbs['jysj'].find()
        assert len(mg_sslsj_data) == 0
        assert len(mg_lslqksj_data) == 0
        assert len(mg_kfpjyzsj_data) == 0
        assert len(mg_jysj_data) == 0

    @allure.feature('http_接口')
    @allure.story('节点上报接口_区块上报')
    @pytest.mark.block_report
    def test_block_reported_relay_chain_null_value_chain_type(self, prepare_mongo_block_report):
        logger = log.Log(sys._getframe().f_code.co_name)
        logger.info("test begining")
        # 1.clear mongo
        mgdbs = prepare_mongo_block_report

        # 2.send post request
        req_url = 'http://%s' % conf.apihost_test
        api_url = '%s%s' % (req_url, http_block_reported.data["url"])
        header = http_block_reported.data["header"]
        data_req = http_block_reported.data["block_reported_null_value_chain_type"]["request"]
        data_resp = http_block_reported.data["block_reported_null_value_chain_type"]["response"]
        data_req['time'] = common.current_time_iso()
        response = request.post_request(api_url, data_req, header)

        # 3.assert response info
        assert test.assert_code(response['code'], 200)
        assert test.assert_body_code_ge(response['body'], data_resp['code'])
        # assert test.assert_body(response['body'], 'data', data_resp['data'])
        assert test.assert_time(response['time_consuming'], 100)

        # 4.assert mongo data
        mg_sslsj_data = mgdbs['sslsj'].find()
        mg_lslqksj_data = mgdbs['lslqksj'].find()
        mg_kfpjyzsj_data = mgdbs['kfpjyzsj'].find()
        mg_jysj_data = mgdbs['jysj'].find()
        assert len(mg_sslsj_data) == 0
        assert len(mg_lslqksj_data) == 0
        assert len(mg_kfpjyzsj_data) == 0
        assert len(mg_jysj_data) == 0
