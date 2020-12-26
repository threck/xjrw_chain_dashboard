# -*- coding:utf-8 -*-
# @Author      : FangChao
# @File        : gen_data.py
# @Date        : 2020/12/12 0012
# @Description : xjrw_chain_dashboard

import math
import sys
import copy
import random
from datetime import datetime
from Config import config as c
from Common import mongo
from Common import log
from Common import common
from Common import consts
from Stress.Conf import config
from Stress.Data import templates


logger = log.Log()


class MongoDataBase(object):

    def clear_mongo_database(self):
        conf = c.Config()
        mg_url = conf.mongodb_test
        mg_sslsj = mongo.Mongo(mg_url, consts.MGDB, consts.MGDB_SSLSJ)
        mg_lslqksj = mongo.Mongo(mg_url, consts.MGDB, consts.MGDB_LSLQKSJ)
        mg_kfpjyzsj = mongo.Mongo(mg_url, consts.MGDB, consts.MGDB_KFPJYZSJ)
        mg_jysj = mongo.Mongo(mg_url, consts.MGDB, consts.MGDB_JYSJ)
        mg_sslsj.clear_col_data()
        mg_lslqksj.clear_col_data()
        mg_kfpjyzsj.clear_col_data()
        mg_jysj.clear_col_data()

class Data(object):
    def __init__(self, type, chainKey, nodeId):
        self.data = copy.deepcopy(templates.block_post_data)
        self.data['type'] = type
        self.data['chainKey'] = chainKey
        self.data['nodeId'] = nodeId
        self.lock_hash = []
        self._count = self._create_counter()
        self._wallet_count = self._create_counter()
        self._height_count = self._create_counter()
        self.shard_list = []
        self.shard_list_tmp = []

    def _create_counter(self):
        count = -1
        def counter():
            nonlocal count
            count += 1
            return count
        return counter

    def _gen_hash(self):
        return '0x%s%s%059d' % (self.data['type'], self.data['chainKey'], self._count())

    def _gen_wallet(self):
        return '0xwallet%058d' % self._wallet_count()

    def _gen_ss_trans_nu_list(self):
        ss_trans_nu_list = []
        trade_nu_left = self.data['trans']
        while trade_nu_left != 0:
            trade_nu_thistime = random.randint(1, trade_nu_left)
            trade_nu_left = trade_nu_left - trade_nu_thistime
            ss_trans_nu_list.append(trade_nu_thistime)
            if len(ss_trans_nu_list) == len(self.shard_list) - 1:
                ss_trans_nu_list.append(trade_nu_left)
                break
        return ss_trans_nu_list

    def _gen_ss_trans(self):
        t_hash = self._gen_hash()
        t_from = self._gen_wallet()
        t_to = self._gen_wallet()
        t_amount = 1
        return {'hash': t_hash, 'from': t_from, 'to': t_to, 'amount': t_amount}

    def _gen_ss_detail(self, trans_nu):
        # gen from_shard
        from_shard = 'S%s' % self.data['chainKey']
        # gen to_shard
        # logger.info(f'shard_list_tmp: {self.shard_list_tmp}')
        # logger.info(f'len of shard_list_tmp: {len(self.shard_list_tmp)}')
        if len(self.shard_list_tmp) == 1:
            shard_list_index = 0
        else:
            shard_list_index = random.randint(0, len(self.shard_list_tmp) - 1)
        to_shard = 'S%s' % self.shard_list_tmp[shard_list_index]
        self.shard_list_tmp.pop(shard_list_index)
        # gen from_relay
        from_relay = 'R%s' % self.data['chainKey'][:2]
        # gen to_relay
        to_relay = 'R%s' % to_shard[1:3]
        # gen hash
        hash = self._gen_hash()
        # gen trans
        trans = [self._gen_ss_trans() for i in range(trans_nu)]
        return dict(fromShard=from_shard, toShard=to_shard,
                    fromRelay=from_relay, toRelay=to_relay,
                    hash=hash, trans=trans)

    def _gen_ss_data(self):
        self.shard_list_tmp = self.shard_list
        return [self._gen_ss_detail(trans_nu) for trans_nu in self._gen_ss_trans_nu_list()]

    def _gen_ss_up_info(self, ss):
        from_key = [ss['fromShard'], ss['fromRelay']]
        to_key = [ss['toShard'], ss['toRelay']]
        dict1 = dict(fromkey=from_key[0], tokey=to_key[1])
        return dict1

    def _gen_upstream_s(self):
        up_stream = []
        for ss in self.data['detail']['ss']:
            if ss not in up_stream:
                up_stream.append(self._gen_ss_up_info(ss))
        for s in up_stream:
            s['hash'] = self._gen_hash()
        return up_stream

    def _gen_upstream_r(self, chain_keys_r):
        trade_nu = 20
        rr_trans = []
        from_relay = '%s%s' % (self.data['type'], self.data['chainKey'])
        for i in range(trade_nu):
            to_relay_nu = random.randint(0, len(chain_keys_r) - 1)
            to_relay = chain_keys_r[to_relay_nu]
            tr = dict(fromkey='%s' % from_relay, tokey='R%s' % to_relay)
            if tr not in rr_trans:
                rr_trans.append(dict(fromkey='%s' % from_relay, tokey='R%s' % to_relay))
        for tr in rr_trans:
            tr['hash'] = self._gen_hash()
        return rr_trans

    def _gen_downstream_r(self, chain_keys_s):
        trade_nu = 20
        rs_trans = []
        from_relay = '%s%s' % (self.data['type'], self.data['chainKey'])
        for i in range(trade_nu):
            to_shard_nu = random.randint(0, len(chain_keys_s) - 1)
            to_shard = chain_keys_s[to_shard_nu]
            tr = dict(fromkey='%s' % from_relay, tokey='S%s' % to_shard)
            if tr not in rs_trans:
                rs_trans.append(dict(fromkey='%s' % from_relay, tokey='S%s' % to_shard))
        for tr in rs_trans:
            tr['hash'] = self._gen_hash()
        return rs_trans


    def _gen_downstream_b(self, chain_keys_r):
        trade_nu = 20
        r_trans = []
        for i in range(trade_nu):
            from_relay_nu = random.randint(0, len(chain_keys_r) - 1)
            to_relay_nu = random.randint(0, len(chain_keys_r) - 1)
            from_relay = chain_keys_r[from_relay_nu]
            to_relay = chain_keys_r[to_relay_nu]
            tr = dict(fromkey='R%s' % from_relay, tokey='R%s' % to_relay)
            if tr not in r_trans:
                r_trans.append(dict(fromkey='R%s' % from_relay, tokey='R%s' % to_relay))
        for tr in r_trans:
            tr['hash'] = self._gen_hash()
        return r_trans

    def _gen_data_public(self, lock_hash):
        if self.data['hash'] == '':
            self.data['father'] = ''
        else:
            self.data['father'] = self.data['hash']
        self.data['hash'] = self._gen_hash()
        self.data['height'] = self._height_count()
        if self.data['time'] == '':
            self.data['interval'] = 0
            self.data['time'] = common.current_time_iso()
        else:
            now = common.current_time_iso()
            interval = common.isostr_to_datetime(now) - common.isostr_to_datetime(self.data['time'])
            # self.data['interval'] = (interval.days * 24 * 3600 + interval.seconds) * 1000000 + interval.microseconds
            self.data['interval'] = float('%.3f' % float(interval.days * 24 * 3600 + interval.seconds + interval.microseconds * 0.000001))
            # self.data['interval'] = interval.days * 24 * 3600 + interval.seconds + interval.microseconds * 0.000001
            self.data['time'] = now
        self.data['lockHash'] = lock_hash

    def _gen_data_b(self, chain_keys_r):
        # generated dynamically(get from config file)
        if self.data['height'] == 0:
            self.data['trans'] = 0
        else:
            self.data['trans'] = config.SS_TRADE_NU * config.CHAIN_NU_TOTAL["S"]
        # upStream and downStream:
        self.data['detail']['upStream'] = []
        self.data['detail']['downStream'] = self._gen_downstream_b(chain_keys_r)
        self.data['detail']['ss'] = []
        # B|R: have downHash, don't have upHash
        self.data['downHash'] = self._gen_hash()
        # B: don't have upHash
        self.data['upHash'] = ""
        # gen size after all
        self.data['size'] = sys.getsizeof(str(self.data)) + 1024 * 3

    def _gen_data_r(self, chain_keys_r, chain_keys_s):
        # generated dynamically(get from config file)
        if self.data['height'] == 0:
            self.data['trans'] = 0
        else:
            self.data['trans'] = config.SS_TRADE_NU * int(config.CHAIN_NU_LOCAL["S"] / config.CHAIN_NU_LOCAL["R"])
        self.data['detail']['ss'] = []
        self.data['detail']['upStream'] = self._gen_upstream_r(chain_keys_r)
        self.data['detail']['downStream'] = self._gen_downstream_r(chain_keys_s)
        self.data['upHash'] = self._gen_hash()
        self.data['downHash'] = self._gen_hash()
        self.data['size'] = sys.getsizeof(str(self.data)) + 1024 * 3

    def _gen_data_s(self, s_chain_key):
        self.shard_list = copy.deepcopy(s_chain_key)
        # generated dynamically(get from config file)
        self.data['trans'] = config.SS_TRADE_NU

        # upStream and downStream:
        # S: generated dynamically; don't have downStream
        self.data['detail']['ss'] = self._gen_ss_data()
        self.data['detail']['upStream'] = self._gen_upstream_s()
        self.data['detail']['downStream'] = []

        # S|R: have upHash
        self.data['upHash'] = self._gen_hash()
        # S: don't have downHash
        self.data['downHash'] = ""
        self.data['size'] = sys.getsizeof(str(self.data)) + 1024 * 3

    def gen_data(self, lock_hash, chain_keys_r=None, chain_keys_s=None, chain_key_s=None):
        self._gen_data_public(lock_hash)
        if self.data['type'] == 'B':
            self._gen_data_b(chain_keys_r)
        elif self.data['type'] == 'R':
            self._gen_data_r(chain_keys_r, chain_keys_s)
        elif self.data['type'] == 'S':
            self._gen_data_s(chain_key_s)
        logger.debug(f'Automatically generate data:\n{self.data}')

    async def gen_lock_hash(self):
        data = self.data
        self.lock_hash = dict(type=data['type'], chainkey=data['chainKey'], height=data['height'])
        # logger.info(f'Automatically generate lockHash:\n{self.lock_hash}')
